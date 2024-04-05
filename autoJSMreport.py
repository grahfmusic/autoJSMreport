#!/usr/bin/python3

# AutoJSMReport v1.1
# Automatical Jira Report Generation Tool

import datetime
import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import argparse
import logging
import sys

class ApplicationInfo:
    @staticmethod
    def display_app_info():
        print("\n" + "\u2550" * 51)
        print("Automatic Jira Report Generation Tool - Version 1.0")
        print("Developed by Dean Thomson")
        print("Copyright 2024 © CCA Software Pty Ltd")
        print("\u2550" * 51 + "\n")

import logging

class DualLogger:
    def __init__(self, logfile='jira-report.log'):
        self.logger = logging.getLogger('JiraReportLogger')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            # File handler setup
            file_handler = logging.FileHandler(logfile)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            # Console handler setup
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def log(self, message, action='', complete=False):
        # Append the tick mark after the action if the action is complete
        action_message = f"{action}... {'✓' if complete else ''}"
        full_message = f":: {action_message} {message}"
        self.logger.info(full_message)


logger = DualLogger()

class ConfigValidator:
    @staticmethod
    def validate(config):
        logger.log(" Configuration Validating", action="", complete=False)
        required_settings = {
            'jira': ['server', 'jira_ticket_base_url', 'username', 'password'],
            'email': ['sender', 'smtp_server', 'smtp_port', 'smtp_username', 'smtp_password'],
            'assignee_recipients': []
        }
        missing_settings = []
        for section, keys in required_settings.items():
            if section not in config:
                missing_settings.append(f"Missing section: {section}")
                continue
            for key in keys:
                if key not in config[section]:
                    missing_settings.append(f"Missing setting: {section}/{key}")
        if missing_settings:
            raise ValueError("Configuration validation failed:\n" + "\n".join(missing_settings))
            logger.log(f"Configuration Validation Failed", complete=False)
        logger.log(f"Configuration Validated", "", complete=True)

class JiraApi:
    def __init__(self, config, assignee):
        self.config = config
        self.assignee = assignee

    def fetch_issues(self):
        logger.log(f" JIRA API Open Ticket Request for assignee '{self.assignee}'", "", complete=False)
        api_url = f"{self.config['jira']['server']}/rest/api/2/search"
        jql_query = f'assignee = "{self.assignee}" AND status != "Closed" AND status != "Resolved" AND status != "Done" ORDER BY created DESC'
        try:
            response = requests.get(api_url, auth=HTTPBasicAuth(self.config['jira']['username'], self.config['jira']['password']),
                                    params={'jql': jql_query, 'fields': 'key,summary,assignee,reporter,created,updated,priority,status'})
            response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
            issues = response.json()['issues']
            logger.log(f"Fetched {len(issues)} issues for assignee '{self.assignee}'", "", complete=True)
            return issues
        except requests.exceptions.HTTPError as http_err:
            logger.log(f"HTTP error occurred: {http_err}", "JIRA API Request", complete=False)
            # Re-raise the exception if you want to handle it further up the call stack
            raise
        except Exception as err:
            logger.log(f"An error occurred: {err}", "JIRA API Request", complete=False)
            # Re-raise the exception if you want to handle it further up the call stack
            raise

class EmailReport:
    def __init__(self, config, assignee, cc_emails):
        self.config = config
        self.assignee = assignee
        self.cc_emails = cc_emails
        self.current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.priority_colours = {
            "Blocker": "#FFADA9", "Critical": "#DB5856", "High": "#FFB380", 
            "Medium": "#FDFD96", "Low": "#DCD3DD", "Trivial": "#00FFFF", "Default": "#F2EEF2"
        }
        self.priority_order = {
            "Blocker": 1, "Critical": 2, "High": 3, "Medium": 4, 
            "Low": 5, "Trivial": 6, "Default": 999
        }

    def _get_priority_order(self, priority_name):
        return self.priority_order.get(priority_name, self.priority_order["Default"])

    def generate_email_body(self, issues):
        # Sort issues by their priority order before generating the HTML
        sorted_issues = sorted(issues, key=lambda issue: (self._get_priority_order(issue['fields'].get('priority', {}).get('name', 'Default')), datetime.datetime.strptime(issue['fields']['updated'], "%Y-%m-%dT%H:%M:%S.%f%z")))

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Consolas, 'Droid Sans Mono', monospace; font-size: 12px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ padding: 8px; text-align: left; border: 1px solid #2b3e50; }}
        th {{ background-color: cyan; }}
        .message {{ font-size: 14px; font-family: 'Ubuntu', 'DejaVu Sans', 'Calibri', 'Arial', 'Sans Serif'; }}
    </style>
</head>
<body>
    <h1>Outstanding CCA Software Jira Service Management Tickets as of {self.current_date}</h1>
    <h2>Assignee: {self.assignee}</h2>
    <h3>Date: {self.current_date}</h3>
    <br>
    <hr>
    <br>
    <p class="message">Hey {self.assignee},</p>
    <p></p>
    <p class="message">I hope this message finds you well. Attached is an overview of your open JIRA tickets for the date of {self.current_date}, prioritized from critical to lowest. Our goal is to swiftly address high-priority issues and maintain operational efficiency.</p>
    <p></p>
    <h2>Please Note:</h2>
    <ul class="message">
        <li><strong>Critical and High Priority:</strong> These need your immediate action. Update or escalate as needed.</li>
        <li><strong>Closure of Resolved Logs:</strong> If any tasks are completed, ensure they are closed in the system.</li>
        <li><strong>Review Completed Tasks:</strong> Confirm that all completed tasks are accurately reflected and updated.</li>
    </ul>
    <br>
    <p class="message">You can quickly visit any outstanding log by clicking on the ticket number for quick convenient navigation and access.</p>
    <br>
    <hr>
    <br><br>
    <table>
        <tr>
            <th>Ticket Number</th><th>Title</th><th>Assignee</th><th>Reporter</th><th>Created</th><th>Last Updated</th><th>Priority</th><th>Status</th>
        </tr>
        """
        
        for issue in sorted_issues:
            ticket_url = f"{self.config['jira']['jira_ticket_base_url']}{issue['key']}"
            created_datetime = datetime.datetime.strptime(issue['fields']['created'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M")
            updated_datetime = datetime.datetime.strptime(issue['fields']['updated'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M")
            priority_name = issue['fields'].get('priority', {}).get('name', 'Default')
            priority_colour = self.priority_colours.get(priority_name, self.priority_colours['Default'])
            html_body += f"""
    <tr bgcolor="{priority_colour}"><td><a href="{ticket_url}" target="_blank" style="color: #00008B;">{issue['key']}</a></td><td>{issue['fields']['summary']}</td>
    <td>{issue['fields'].get('assignee', {}).get('displayName', 'Unassigned')}</td>
    <td>{issue['fields'].get('reporter', {}).get('displayName', 'N/A')}</td>
    <td>{created_datetime}</td><td>{updated_datetime}</td>
    <td>{priority_name}</td><td>{issue['fields'].get('status', {}).get('name', 'N/A')}</td></tr>
    """
        
        html_body += "</table></body></html>"
        logger.log(f"Generated HTML Email Text and Tables for assignee '{self.assignee}'", "", complete=True)
        return html_body



    def send(self, issues):
        html_body = self.generate_email_body(issues)
        msg = MIMEMultipart('related')
        msg['Subject'] = f"ATT: {self.assignee} - Outstanding CCA Software JIRA Tickets Report - Date: {self.current_date}"
        msg['From'] = self.config['email']['sender']
        msg['To'] = self.config['assignee_recipients'].get(self.assignee, "default_recipient@example.com")
        if self.cc_emails:
            msg['Cc'] = ', '.join(self.cc_emails)
        msg.attach(MIMEText(html_body, 'html'))
        with smtplib.SMTP_SSL(self.config['email']['smtp_server'], self.config.getint('email', 'smtp_port')) as server:
            server.login(self.config['email']['smtp_username'], self.config['email']['smtp_password'])
            server.send_message(msg)
        logger.log(f"Sent email report to assignee '{self.assignee}'", "", complete=True)

def main():
    ApplicationInfo.display_app_info()
    parser = argparse.ArgumentParser(description="Generate and send a JIRA report for a specific assignee.")
    parser.add_argument("--assignee", required=True, help="The JIRA username of the assignee for which to generate the report.")
    parser.add_argument("--cc", help="Email addresses for CC, separated by commas.", default="")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')
    ConfigValidator.validate(config)

    jira_api = JiraApi(config, args.assignee)
    issues = jira_api.fetch_issues()

    email_report = EmailReport(config, args.assignee, args.cc.split(',') if args.cc else [])
    email_report.send(issues)

if __name__ == "__main__":
    main()