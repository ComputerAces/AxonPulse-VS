# 🧩 Enums Nodes

This document covers nodes within the **Enums** core category.

## 📂 General

### Compare Type

**Version**: `2.3.0`

Provides a selectable comparison operator (e.g., ==, !=, >, <) as a pulse-triggered output.
Essential for configuring conditional logic in nodes that require a comparison operator.

Inputs:
- Flow: Trigger the output of the selected comparison type.
- Value: Optionally set the comparison operator via a logic pulse.

Outputs:
- Flow: Pulse triggered after the value is processed.
- Result: The selected comparison operator string.

---

### Write Mode

**Version**: `2.3.0`

Standardizes file writing behaviors such as 'Overwrite' or 'Append'.

This node provides a UI dropdown for selecting how file operations should 
interact with existing files. 'Overwrite' replaces the entire file content, 
while 'Append' adds new data to the end of the file.

Inputs:
- Value: The selected write mode (Overwrite/Append).
- Value Options: The list of toggleable modes.
- Header Color: The UI accent color for this node.

Outputs:
- Result: The selected mode string (compatible with Write nodes).

---

[Back to Node Index](Index.md)
