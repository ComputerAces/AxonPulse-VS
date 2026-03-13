# 🧩 File System Nodes

This document covers nodes within the **File System** core category.

## 📂 File Editing

### File Seek

**Version**: `2.3.0`

Adjusts the read/write pointer within an open file provider.

Use this to move the pointer forward, backward, or to a specific offset 
relative to the start, current position, or end of the file.

Inputs:
- Flow: Trigger the seek operation.
- Offset: Number of bytes to move the pointer.
- Whence: Reference point (0: Start, 1: Current, 2: End).

Outputs:
- Flow: Pulse triggered on successful movement.
- Error Flow: Pulse triggered if the seek is invalid or fails.

---

### File System Provider

**Version**: `2.3.0`

Managed service provider for low-level file system I/O.
Opens a persistent file handle and provides hijackable operations (read, write, seek, etc.)
for downstream nodes within its execution scope.

Inputs:
- Flow: Start the file provider scope.
- Provider End: Close the file handle and end the scope.
- File Path: The absolute path to the file.
- Mode: The file open mode (r, w, a, rb, wb, etc.).

Outputs:
- Provider Flow: Active while the file handle is open.
- Provider ID: Unique identifier for this provider.
- Flow: Triggered when the file is closed.

---

## 📂 Operations

### File Peek

**Version**: `2.3.0`

Reads data from a file without moving the active pointer position.

Peek allows investigating upcoming data in the stream without affecting 
subsequent Read operations within the same provider session.

Inputs:
- Flow: Trigger the peek operation.
- Size: Number of bytes/characters to peek.

Outputs:
- Flow: Pulse triggered on success.
- Error Flow: Pulse triggered if the operation fails.
- Data: The content read.

---

### File Position

**Version**: `2.3.0`

Retrieves the current byte offset of the file pointer.

Useful for tracking progress or saving locations for future Seek operations 
within a file provider scope.

Inputs:
- Flow: Trigger the position check.

Outputs:
- Flow: Pulse triggered on success.
- Error Flow: Pulse triggered if retrieval fails.
- Position: The current integer byte offset.

---

### File Read

**Version**: `2.3.0`

Reads data from an open file using an active FILE provider.

This node retrieves content from the file associated with the current provider 
session. It progresses the file pointer by the number of bytes read.

Inputs:
- Flow: Trigger the read operation.
- Size: Number of bytes/characters to read (-1 for until EOF).

Outputs:
- Flow: Pulse triggered on successful read.
- Error Flow: Pulse triggered if the read fails or no provider is active.
- Data: The resulting content (String or Bytes).

---

### File Write

**Version**: `2.3.0`

Writes data to an open file via an active FILE provider.

This node commits content to the file at the current pointer position. 
It is designed to work within a File Provider scope to handle persistent 
file handles across a logic sequence.

Inputs:
- Flow: Trigger the write operation.
- Data: The content to write (String or Bytes).

Outputs:
- Flow: Pulse triggered on successful write.
- Error Flow: Pulse triggered if the operation fails.

---

[Back to Node Index](Index.md)
