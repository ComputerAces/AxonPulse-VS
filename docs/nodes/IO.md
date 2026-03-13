# 🧩 IO Nodes

This document covers nodes within the **IO** core category.

## 📂 Documents

### Excel Provider

**Version**: `2.3.0`

Establishes an automation environment for Microsoft Excel workbooks.

This provider manages the lifecycle of an Excel application instance, 
allowing downstream 'Excel Commander' nodes to execute within a shared context.

Inputs:
- Flow: Open Excel and load the specified workbook.
- Provider End: Close the workbook and shut down Excel.
- File Path: The absolute path to the workbook (.xlsx, .xls).

Outputs:
- Provider Flow: Active while the spreadsheet is open.
- Provider ID: Identifier for automation node targeting.
- Flow: Pulse triggered after the scope is closed.

---

[Back to Node Index](Index.md)
