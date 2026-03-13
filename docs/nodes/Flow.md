# 🧩 Flow Nodes

This document covers nodes within the **Flow** core category.

## 📂 Debug

### Debug Node

**Version**: `2.3.0`

Logs input data to the console for debugging purposes.

Inputs:
- Flow: Execution trigger.
- Data: The information to be logged.

Outputs:
- Flow: Triggered after logging.

---

## 📂 SubGraph

### SubGraph Node

**Version**: `2.3.0`

Executes a nested graph (subgraph) as a single node within the current context.

This node allows for hierarchical graph design and logic reuse. It dynamically 
generates input and output ports based on the 'Start' and 'Return' nodes found 
within the child graph file.

Inputs:
- Flow: Trigger execution of the subgraph.
- GraphPath: Path to the .syp graph file to load.
- [Dynamic Inputs]: Data variables passed into the subgraph's Start node.

Outputs:
- Flow: Pulse triggered when the subgraph reaches a Return node.
- Error Flow: Pulse triggered if the subgraph fails to load or execute.
- [Dynamic Outputs]: Data variables returned from the subgraph's Return node.

---

[Back to Node Index](Index.md)
