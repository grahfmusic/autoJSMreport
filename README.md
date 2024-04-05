# Automatic Jira Report Generation Tool
<img style="width: 70%; display: block; margin-left: auto; margin-right: auto;" src="http://vilmos.ccasoftware.com.au:3000/CCA/jira-automatic-reports/raw/master/imgs/readme_img1.png" alt="Report Output"></img>

## Introduction

The Automatic Jira Report Generation Tool is a comprehensive Python script designed for automating the process of fetching JIRA issues and compiling them into an organized report that is then sent via email. This tool simplifies the monitoring and management of JIRA tickets by automatically generating and distributing reports, making it an invaluable resource for teams and individuals managing projects within JIRA.

## Features

The tool is packed with features aimed at enhancing efficiency, security, and usability. Here's what it offers:

### Command-Line Arguments
- **Assignee Specification**: Use `--assignee` to specify the report's focus on a particular JIRA user's tickets.
- **CC Emails**: The `--cc` argument allows adding one or more email addresses to receive a carbon copy of the report, facilitating broader communication.

### Configuration via `config.ini`
- Centralizes crucial settings, including JIRA API credentials, SMTP email settings, and more, in a single, easily editable file.

### Secure Credential Storage
- Keeps sensitive information such as API tokens and email passwords within a secure configuration file, away from the main script code.

### Dynamic Email Customization
- Generates email subjects dynamically, incorporating meaningful details like the assignee's name and current date.
- Supports HTML email formatting, including priority-based coloring for better readability and engagement.

### Prioritization and Sorting
- Issues in the report are sorted based on priority, ensuring that the most critical items are highlighted and addressed first.

### Adaptive Reporting
- The script adapts the email's font and style based on the operating system, ensuring consistency across different email clients.

### Logging and Error Handling
- Detailed logging to `/var/log/jira-report.log` helps track the script's operation and troubleshoot issues.
- Robust error handling prevents execution continuation in the case of critical failures, enhancing script reliability.

### JIRA Ticket Links
- Converts JIRA ticket numbers in the report into direct links, enabling quick access to ticket details within JIRA.

## Getting Started

This tool requires Python 3 and several dependencies, including `requests` for API interactions and `smtplib` for sending emails. Configuration is handled through the `config.ini` file, where users specify their JIRA instance, credentials, email settings, and preferences for report formatting.

To run the script, use the following command format, replacing `[assignee_username]` with the desired JIRA user's username:

```bash
python jira-automatic-reports.py --assignee [assignee_username]
```
---
# Configuration (`config.ini`) Documentation

The `config.ini` file serves as the backbone for configuring the Automatic Jira Report Generation Tool, allowing users to set up their JIRA instance, email settings, and more. Below is a breakdown of each section within the `config.ini` file:

## JIRA Configuration

- **`[jira]` Section**: Defines the JIRA server details and credentials for API access.
    - `server`: The base URL of your JIRA instance. Example: `https://support.ccasoftware.com`
    - `jira_ticket_base_url`: The base URL for accessing individual JIRA tickets. Example: `https://support.ccasoftware.com/browse/`
    - `username`: Your JIRA username.
    - `password`: Your JIRA password or API token.

## Email Configuration

- **`[email]` Section**: Sets up the email sending details.
    - `sender`: The email address from which the reports will be sent. Example: `reports@ccasoftware.com`
    - `recipient`: The default recipient email address for the reports. Example: `deant@ccasoftware.com.au`
    - `smtp_server`: The SMTP server used for sending emails. Example: `mail.ccasoftware.com`
    - `smtp_port`: The port used by the SMTP server. Commonly 465 for SSL. Example: `465`
    - `smtp_username`: The username for authenticating with the SMTP server.
    - `smtp_password`: The password for authenticating with the SMTP server.

## Assignee Recipients Configuration

- **`[assignee_recipients]` Section**: Maps specific JIRA assignees to email addresses, allowing for personalized report distribution.
    - Each entry under this section follows the format `jira_username = email_address`. This allows reports for specific JIRA users (assignees) to be sent to designated email addresses. For example:
        - `dean = deant@ccasoftware.com.au`
        - `karl = karl@ccasoftware.com.au`
        - `...`
---