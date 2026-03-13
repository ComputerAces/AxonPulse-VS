# 🧩 Logic Nodes

This document covers nodes within the **Logic** core category.

## 📂 Control Flow

### For Node

**Version**: `2.3.0`

Executes a block of code a specific number of times based on a numeric range.

Inputs:
- Flow: Initialize the loop and start the first iteration.
- Continue: Trigger the next iteration of the loop.
- Break: Immediately terminate the loop.
- Start: The numeric value to begin counting from.
- Step: The amount to increment/decrement per iteration.
- Stop: The target value to compare the index against.
- CompareType: The operator used to check the stop condition (e.g., <, <=, ==).

Outputs:
- Flow: Pulse triggered once the loop completes or breaks.
- Body: Pulse triggered for each iteration while the condition is true.
- Index: The current numeric value of the counter.

---

### ForEach Node

**Version**: `2.3.0`

Iterates through a list of items, executing the 'Body' output for each element.

Inputs:
- Flow: Start the iteration from the first item.
- Continue: Move to the next item in the list.
- Break: Terminate the loop immediately.
- End: Terminate the iteration and kill all active parallel branches.
- List: The collection of items to iterate over.

Outputs:
- Flow: Triggered when the entire list has been processed or the loop is broken.
- Body: Triggered for each individual item in the list.
- Item: The current value from the list.
- Index: The zero-based position of the current item.

---

### Start Node

**Version**: `2.3.0`

The entry point for a graph or subgraph execution.

Initiates the flow and optionally injects global variables or provider 
contexts into the runtime. It acts as the primary data producer for 
the starting branch.

Inputs:
- None (Initiator node).

Outputs:
- Flow: The primary execution pulse.
- Error Flow: Pulse triggered if context initialization fails.

---

### While Node

**Version**: `2.3.0`

Repeatedly executes a block of code as long as a boolean condition remains true.

Inputs:
- Flow: Start the while loop evaluation.
- Continue: Trigger the next check of the loop.
- Break: Immediately terminate the loop.
- End: Terminate the loop and kill all active parallel branches.
- Condition: A boolean value determining if the loop should continue.

Outputs:
- Flow: Pulse triggered after the loop finishes.
- Body: Pulse triggered for each iteration while the condition is met.
- Index: The current iteration count (0-based).

---

## 📂 Fuzzy

### Fuzzy Search

**Version**: `2.3.0`

Performs fuzzy string matching and automated spell correction.

This node compares 'Raw Text' against 'Target' (string or list) using fuzzy 
logic. If the initial match is below 'Threshold', it attempts spell 
correction and re-scores. It routes the flow to 'Ambiguous' if no 
satisfactory match is found.

Inputs:
- Flow: Trigger the search.
- Raw Text: The string to be analyzed.
- Target: The reference string or list of candidates to match against.
- Threshold: Minimum score (0-100) to consider a match successful.

Outputs:
- Flow: Triggered if a match exceeds the threshold.
- Ambiguous: Triggered if match score is below the threshold.
- Best Text: The result (either original or spell-corrected).
- Confidence: Per-word match scores.
- Score: Overall fuzzy similarity score.
- Corrected: Boolean indicating if spell correction was applied and improved the score.

---

## 📂 General

### Compare

**Version**: `2.3.0`

Performs a comparison between two values (A and B) using a specified operator.
Supports numbers, strings, and formatted datetime strings.

Inputs:
- Flow: Trigger the comparison.
- Compare Type: The operator to use (==, !=, >, <, >=, <=).
- A: The first value.
- B: The second value.

Outputs:
- True: Triggered if the condition is met.
- False: Triggered if the condition is not met.
- Result: Numeric 1 (True) or 0 (False).
- Compare Result: Boolean result.

---

## 📂 Scripting

### Python Script

**Version**: `2.3.0`

Executes a Python script either synchronously or as a background service.

Allows for custom logic extension using the bridge API. Scripts can 
be loaded from a file or written directly in the node. Supports 
dynamic inputs and outputs, and automatic dependency installation 
via 'Requirements'.

Inputs:
- Flow: Trigger the script.
- Env: Optional path to a Python executable or virtual environment.
- Script Path: Path to a .py file to execute.
- Script Body: Inline Python code to execute.
- Requirements: New-line separated list of pip packages to ensure.
- Use Current Env: Whether to use the system environment if no 'Env' is provided.

Outputs:
- Flow: Pulse triggered immediately (Service) or after completion (Sync).
- Finished Flow: Pulse triggered after the script finishes execution.
- Error Flow: Pulse triggered if the script crashes or fails to start.
- Std Out: Pulse triggered for each printed line from the script.
- Text Out: The string content of the printed line.

---

[Back to Node Index](Index.md)
