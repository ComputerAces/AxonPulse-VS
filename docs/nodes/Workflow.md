# 🧩 Workflow Nodes

This document covers nodes within the **Workflow** core category.

## 📂 General

### Project Metadata Get

**Version**: `2.1.0`

Retrieves project metadata (Name, Version, Category, Description) from the bridge.

### Outputs:
- Flow (flow): Pulse triggered after retrieval.
- Name (string): Project Name.
- Version (string): Project Version.
- Category (string): Project Category.
- Description (string): Project Description.

---

### Project Metadata Set

**Version**: `2.1.0`

Updates project metadata in the bridge.

### Inputs:
- Flow (flow): Trigger the update.
- Name (string): New Project Name.
- Version (string): New Project Version.
- Category (string): New Project Category.
- Description (string): New Project Description.

### Outputs:
- Flow (flow): Pulse triggered after the update.

---

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

### Global Var Get

**Version**: `2.1.0`

Retrieves a variable from the global (root) level.

### Inputs:
- Flow (flow): Trigger the retrieval.
- Var Name (string): The name of the variable.

### Outputs:
- Flow (flow): Pulse triggered after retrieval.
- Value (any): The current value of the global variable.

---

### Global Var Set

**Version**: `2.1.0`

Sets a variable at the global (root) level, accessible by any graph or subgraph.
If the variable doesn't exist, it is created.

### Inputs:
- Flow (flow): Trigger the update.
- Var Name (string): The name of the variable.
- Value (any): The value to set.

### Outputs:
- Flow (flow): Pulse triggered after the variable is set.

---

### Vault Get

**Version**: `2.1.0`

Retrieves and decrypts a secret from the local machine's Enterprise Vault.

### Inputs:
- Flow (flow): Trigger the retrieval action.
- Key (string): The alias/name for the secret used during Vault Set.

### Outputs:
- Flow (flow): Pulse triggered after retrieval.
- Value (string): The decrypted String payload, ready to be wired into API Providers.

---

### Vault Set

**Version**: `2.1.0`

Encrypts and stores a secret in the local machine's Enterprise Vault.
The secret is tied to this machine and will not be exported in the .syp JSON payload.

### Inputs:
- Flow (flow): Trigger the store action.
- Key (string): The alias/name for the secret (e.g., 'OPENAI_API_KEY').
- Secret (string): The plain text secret value to encrypt.

### Outputs:
- Flow (flow): Pulse triggered after the secret is stored securely.

---

[Back to Node Index](Index.md)
