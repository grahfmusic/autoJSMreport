# Automatic Jira Report Generation Tool
![image](https://github.com/automatic-jira-report-generation-tool/automatic-jira-report-generation-tool.github.io/raw/master/images/jira-logo.png)

## Introduction
The Automatic Jira Report Generation Tool is a comprehensive Python script designed to automate the process of fetching Jira issues and compiling them into an organised report that's then sent via email. This tool simplifies the monitoring and management of Jira tickets by automatically generating and distributing reports, making it an invaluable resource for teams and individuals managing projects within Jira.

## Features
The tool is packed with features aimed at enhancing efficiency, security, and usability. Here's what it offers:
### Command-Line Arguments

* `--assignee`: Use to specify the report's focus on a particular Jira user's tickets.
* `--cc`: Add one or more email addresses to receive a carbon copy of the report, facilitating broader communication.

### Configuration via `config.ini`

Centralises crucial settings, including Jira API credentials, SMTP email settings, and more, in a single, easily editable file.

### Secure Credential Storage

Keeps sensitive information such as API tokens and email passwords within a secure configuration file, away from the main script code.

### Dynamic Email Customization

Generates email subjects dynamically, incorporating meaningful details like the assignee's name and current date.
Supports HTML email formatting, including priority-based coloring for better readability and engagement.

### Prioritization and Sorting

Issues in the report are sorted based on priority, ensuring that the most critical items are highlighted and addressed first.

### Adaptive Reporting

The script adapts the email's font and style based on the operating system, ensuring consistency across different email clients.

### Logging and Error Handling

Detailed logging to `/var/log/jira-report.log` helps track the script's operation and troubleshoot issues.
Robust error handling prevents execution continuation in the case of critical failures, enhancing script reliability.

### Jira Ticket Links

Converts Jira ticket numbers in the report into direct links, enabling quick access to ticket details within Jira.

## Getting Started
This tool requires Python 3 and several dependencies, including `requests` for API interactions and `smtplib` for sending emails. Configuration is handled through the `config.ini` file, where users specify their Jira instance, credentials, email settings, and preferences for report formatting.

To run the script, use the following command format, replacing `[assignee_username]` with the desired Jira user's username:
```bash
python jira-automatic-reports.py --assignee [assignee_username]
```

# Configuration (`config.ini`) Documentation
The `config.ini` file serves as the backbone for configuring the Automatic Jira Report Generation Tool, allowing users to set up their Jira instance, email settings, and more. Below is a breakdown of each section within the `config.ini` file:

## Jira Configuration

* `[jira]`: Defines the Jira server details and credentials for API access.
	+ `server`: The base URL of your Jira instance. Example: `https://jira.satan.com`
	+ `jira_ticket_base_url`: The base URL for accessing individual Jira tickets. Example: `https://jira.satan.com/browse/`
	+ `username`: Your Jira username.
	+ `password`: Your Jira password or API token.

## Email Configuration

* `[email]`: Sets up the email sending details.
	+ `sender`: The email address from which the reports will be sent. Example: `reports@blah.com`
	+ `recipient`: The default recipient email address for the reports. Example: `satan@blah.com`
	+ `smtp_server`: The SMTP server used for sending emails. Example: `mail.blah.com`
	+ `smtp_port`: The port used by the SMTP server. Commonly 465 for SSL. Example: `465`
	+ `smtp_username`: The username for authenticating with the SMTP server.
	+ `smtp_password`: The password for authenticating with the SMTP server.

## Assignee Recipients Configuration

* `[assignee_recipients]`: Maps specific Jira assignees to email addresses, allowing for personalised report distribution.
	+ Each entry under this section follows the format `jira_username = email_address`. This allows reports for specific Jira users (assignees) to be sent to designated email addresses. For example:

```
dean = blah@blah.com
karl = blah@blah.com
...
```
