# 🧩 Workflow Nodes

This document covers nodes within the **Workflow** core category.

## 📂 General

### Project Var Get

**Version**: `2.1.0`

Retrieves a global project variable from the bridge.
Project variables persist across different graphs within the same project.

Inputs:
- Flow: Trigger the retrieval.
- Var Name: The name of the project variable to get.

Outputs:
- Flow: Pulse triggered after retrieval.
- Value: The current value of the project variable.

---

### Project Var Set

**Version**: `2.1.0`

Sets a global project variable in the bridge.
Project variables persist across different graphs within the same project.

Inputs:
- Flow: Trigger the update.
- Var Name: The name of the project variable to set.
- Value: The new value to assign to the variable.

Outputs:
- Flow: Pulse triggered after the variable is updated.

---

## 📂 Variables

### Global Get Var

**Version**: `1.0.1`

Retrieves a variable from the global (root) level.

Inputs:
- Flow: Trigger the retrieval.
- Var Name: The name of the variable.

Outputs:
- Flow: Pulse triggered after retrieval.
- Value: The current value of the global variable.

---

### Global Set Var

**Version**: `1.0.1`

Sets a variable at the global (root) level, accessible by any graph or subgraph.
If the variable doesn't exist, it is created.

Inputs:
- Flow: Trigger the update.
- Var Name: The name of the variable.
- Value: The value to set.

Outputs:
- Flow: Pulse triggered after the variable is set.

---

### Project Get Var

**Version**: `1.0.1`

Retrieves a variable local to the current graph or subgraph instance.

Inputs:
- Flow: Trigger the retrieval.
- Var Name: The name of the variable.

Outputs:
- Flow: Pulse triggered after retrieval.
- Value: The current value of the project variable.

---

### Project Set Var

**Version**: `1.0.1`

Sets a variable local to the current graph or subgraph instance.
Acts like a function-level variable.

Inputs:
- Flow: Trigger the update.
- Var Name: The name of the variable.
- Value: The value to set.

Outputs:
- Flow: Pulse triggered after the variable is set.

---

### Vault Get

**Version**: `1.0.0`

Retrieves and decrypts a secret from the local machine's Enterprise Vault.

Inputs:
- Flow: Trigger the retrieval action.
- Key: The alias/name for the secret used during Vault Set.

Outputs:
- Flow: Pulse triggered after retrieval.
- Value: The decrypted String payload, ready to be wired into API Providers.

---

### Vault Set

**Version**: `1.0.0`

Encrypts and stores a secret in the local machine's Enterprise Vault.
The secret is tied to this machine and will not be exported in the .syp JSON payload.

Inputs:
- Flow: Trigger the store action.
- Key: The alias/name for the secret (e.g., 'OPENAI_API_KEY').
- Secret: The plain text secret value to encrypt.

Outputs:
- Flow: Pulse triggered after the secret is stored securely.

---

[Back to Node Index](Index.md)
