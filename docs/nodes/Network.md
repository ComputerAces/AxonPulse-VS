# 🧩 Network Nodes

This document covers nodes within the **Network** core category.

## 📂 Email

### Email Provider

**Version**: `2.3.0`

Provides SMTP server configuration for sending emails.

Inputs:
- Flow: Execution trigger.
- Host: SMTP server hostname (e.g., smtp.gmail.com).
- User: Username for authentication.
- Password: Password for authentication.
- Port: Connection port (default 465).

Outputs:
- Flow: Triggered when the provider is initialized.

---

### IMAP Listener

**Version**: `2.3.0`

Monitors an IMAP email account for new incoming messages.

This node runs as a background service, polling the specified folder 
(default: INBOX) for unread emails. When a new email matches the filter criteria, 
it triggers the 'New Email' flow and outputs message metadata.

Inputs:
- Flow: Start the monitoring service.
- Host: IMAP server address (e.g., imap.gmail.com).
- User: Email address or username.
- Password: Account password or app-specific password.
- Filter: IMAP search criteria (e.g., UNSEEN, FROM "boss@work.com").

Outputs:
- New Email: Pulse triggered for each matching message found.
- Subject: The subject line of the most recent email.
- Sender: The 'From' address of the email.
- Body: A snippet of the email's plain-text content.

---

## 📂 Ingress

### Flask Host

**Version**: `2.3.0`

HTTP Server Provider (Flask). Launches a local web server to handle incoming network requests.

This node acts as a service provider, allowing other 'Flask Route' nodes to register endpoints 
within its scope. It is the foundation for creating local REST APIs, webhooks, or simple 
web interfaces directly within a AxonPulse graph.

Inputs:
- Flow: Trigger to start the server.
- Provider End: Signal to stop the server (Cleanup).
- Host: The address to bind to (e.g., '127.0.0.1' for local, '0.0.0.0' for all interfaces).
- Port: The TCP port to listen on (Default: 5000).

Outputs:
- Provider Flow: Active pulse while the server is running.
- Service ID: Unique identifier for this Flask service.
- Flow: Triggered after the server scope is closed.

---

## 📂 Providers

### Network Provider

**Version**: `2.3.0`

Service provider for base network configurations.
Registers global settings like Base URL and Proxy in a scope for child 
nodes like HTTP Request to discover and use.

Inputs:
- Flow: Start the network provider service and enter the configuration scope.
- Base URL: The default API endpoint prefix.
- Proxy: The proxy server URL for outgoing requests.
- Headers: A dictionary of default HTTP headers.

Outputs:
- Provider Flow: Active while the configuration scope is open.
- Flow: Triggered when the service is stopped.

---

## 📂 SSH

### SSH Provider

**Version**: `2.3.0`

Service provider for SSH (Secure Shell) connections.
Registers connection parameters in a scope for child nodes like 
SSH Command and SFTP Transfer to discover and use.

Inputs:
- Flow: Start the SSH provider service and enter the connection scope.
- Host: The remote hostname or IP address (default: 127.0.0.1).
- Port: The SSH port (default: 22).
- User: The username for authentication.
- Password: The password for authentication.
- Key Path: Path to a private key file for key-based authentication.

Outputs:
- Provider Flow: Active while the connection scope is open.
- Flow: Triggered when the service is stopped.

---

[Back to Node Index](Index.md)
