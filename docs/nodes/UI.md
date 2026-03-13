# 🧩 UI Nodes

This document covers nodes within the **UI** core category.

## 📂 Overlays

### Overlay Highlighter

**Version**: `2.3.0`

Spawns a temporary visual highlight on the screen at specified coordinates.
Useful for guiding user attention or debugging UI element positions.

Inputs:
- Flow: Trigger the overlay display.
- Rect: The [x, y, w, h] coordinates for the highlight.
- Color: The [r, g, b, a] color of the highlight.

Outputs:
- Flow: Pulse triggered after the overlay thread starts.

---

## 📂 Toasts

### Toast

**Version**: `2.3.0`

Displays a system-native toast notification.
On Windows, this uses win11toast for rich notifications. On other 
platforms, it falls back to desktop-notifier.

Inputs:
- Flow: Trigger the notification.
- Title: The bold header text of the toast.
- Message: The main body text of the notification.

Outputs:
- Flow: Pulse triggered after the toast is sent.
- OnClick: Pulse triggered if the user clicks on the notification.

---

### Toast Input

**Version**: `2.3.0`

Displays a toast notification with a text input field (Windows only).
Falls back to a standard PyQt input dialog on non-Windows platforms.

Inputs:
- Flow: Trigger the interactive notification.
- Title: The title of the input request.
- Message: Instructions or prompt text for the user.
- Value: Default text to populate the input field.

Outputs:
- Flow: Pulse triggered after the user submits or closes the dialog.
- Text: The string content entered by the user.
- OnClick: Pulse triggered upon successful submission.

---

### Toast Media

**Version**: `2.3.0`

Displays a system-native toast notification with an attached image.
Ideal for alerts that require visual context, such as security 
camera triggers or status updates with icons.

Inputs:
- Flow: Trigger the notification.
- Title: The bold header text of the toast.
- Message: The main body text of the notification.
- Path: The absolute or relative path to the image file to display.

Outputs:
- Flow: Pulse triggered after the toast is sent.
- OnClick: Pulse triggered if the user clicks on the notification.

---

[Back to Node Index](Index.md)
