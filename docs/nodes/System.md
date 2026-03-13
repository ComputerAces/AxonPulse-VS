# 🧩 System Nodes

This document covers nodes within the **System** core category.

## 📂 Debug

### Logging Provider

**Version**: `2.3.0`

Registers the primary logging service for the graph session.

Initializes a provider context that allows other 'Log' nodes to 
record messages to a centralized file or stream. It sets up 
rotations and file handles used throughout the execution.

Inputs:
- Flow: Trigger the provider initialization.
- File Path: The target log file for the session.

Outputs:
- Done: Pulse triggered once the service is ready.

---

## 📂 Hardware

### Resource Monitor

**Version**: `2.3.0`

Background service that periodically captures system performance metrics.
Monitors CPU, RAM, and primary drive usage on a fixed interval.

Inputs:
- Flow: Start the monitoring service.

Outputs:
- Tick: Pulse triggered on every monitoring interval update.
- CPU Usage: Current CPU utilization percentage.
- RAM Usage: Current RAM utilization percentage.
- Disk Usage: Current primary drive utilization percentage.

---

## 📂 Terminal

### Shell Command

**Version**: `2.3.0`

Executes shell commands on the host system.
Supports both synchronous execution and long-running service processes with 
standard I/O interaction.

Inputs:
- Flow: Execute the command.
- Command: The shell command string to run.
- EnvPath: Optional path to a virtual environment to activate.
- StdIn: Trigger to send 'TextIn' to the running process (Service mode).
- TextIn: String data to send to stdin.

Outputs:
- Started: Triggered when the process starts (Service mode).
- Finished: Triggered when the process exits.
- StdoutData: The full stdout output (Sync mode).
- StderrData: The full stderr output (Sync mode).
- ExitCode: The process exit return code.
- StdOut: Triggered for each line of stdout (Service mode).
- Flow: General pulse triggered after execution starts/finishes.
- TextOut: The most recent line from stdout/stderr (Service mode).
- EnvResult: The environment path that was actually used.

---

[Back to Node Index](Index.md)
