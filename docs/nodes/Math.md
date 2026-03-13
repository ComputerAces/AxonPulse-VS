# 🧩 Math Nodes

This document covers nodes within the **Math** core category.

## 📂 Advanced

### Inverse Lerp

**Version**: `2.3.0`

Calculates the linear interpolant (t) of a value relative to a range [A, B].

This is the inverse of the Lerp operation. It returns a normalized value (typically 0.0 to 1.0) 
representing where 'Value' sits between 'A' and 'B'. If Value is at A, result is 0. If at B, result is 1.

Inputs:
- Flow: Trigger the calculation.
- A: The start of the range (maps to 0.0).
- B: The end of the range (maps to 1.0).
- Value: The current value to normalize.

Outputs:
- Flow: Triggered after calculation.
- T: The calculated interpolant.

---

[Back to Node Index](Index.md)
