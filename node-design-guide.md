# AxonPulse VS Node Design Guide

This guide outlines the strict standards for building nodes in AxonPulse VS.

## 1. Strict Naming Conventions & Uniqueness
- **CamelCase / TitleCase Mandate**: All input, output, and property names defined in the schema must use Camel Case (with space) or Title Case (e.g., "Data", "Image Path", "User Context"). Lowercase variables or Grouped Names (e.g. "ImagePath") are strictly forbidden in schema definitions.
- **Absolute Uniqueness**: Variable names must be unique across inputs, outputs, and properties (case-insensitive).

## 2. The Universal "Flow" Standard
- Every standard node must include primary "Flow" input and output connectors.
- Execution logic must be registered to the "Flow" input trigger.

## 3. Structural Exceptions
- **Start Nodes (Initiators)**: Forbidden from having Input Flow or Input Data variables.
- **Return/End Nodes (Terminators)**: Forbidden from having Output Flow or Output Data variables.

## 4. The SuperNode Base Imperative
- Every node must inherit from `SuperNode` (or `ProviderNode`).
- **Define Schema**: Interface defined in `define_schema()`.
- **Register Handlers**: Triggers bound in `register_handlers()`.
- **The Execution Signal**: Logic handlers must return a boolean (True/False). Returning `None` is forbidden.

## 5. Defensive Data Resolution
- Execution handlers must proactively check both incoming dynamic arguments (wires) and internal properties (typed values) before failing.

---

## 6. Decorative Node Authoring (v2.8.0+)
For simple logic and processing nodes, you can bypass `SuperNode` boilerplate using the `@axon_node` decorator.

### Usage
```python
from axonpulse.nodes.decorators import axon_node

@axon_node(category="Math/Arithmetic", version="2.3.0")
def Add(A: int = 0, B: int = 0) -> int:
    """
    Optional docstring describing the node.
    """
    return A + B
```

### How it Works
1. **Dynamic Schema**: The engine inspects function parameters and type hints to build the `input_schema` and `output_schema`.
2. **Ports**: Input ports match parameter names. The default output is named **Result**.
3. **Typing**: Python hints (`int`, `str`, `list`, `bool`) are automatically mapped to AxonPulse `DataType` enums.
4. **Properties**: Parameters with default values in Python are automatically registered as static node properties in the GUI.
5. **Flow Trigger**: The "Flow" input is automatically bound to the function's execution.
