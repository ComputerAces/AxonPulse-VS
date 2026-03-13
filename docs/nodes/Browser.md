# 🧩 Browser Nodes

This document covers nodes within the **Browser** core category.

## 📂 General

### Browser Provider

**Version**: `2.3.0`

Launches and manages a headless or windowed web browser instance (Chromium, Firefox, WebKit).
Establishes a context for all subsequent browser-based actions.

Inputs:
- Flow: Trigger to launch the browser and enter the scope.
- App ID: Optional unique identifier for the browser session.
- Browser Type: The browser engine to use (Chromium, Firefox, WebKit).
- Headless: If True, runs the browser without a visible window.
- Devtools: If True, opens the browser with developer tools enabled.

Outputs:
- Done: Triggered upon closing the browser and exiting the scope.
- Provider Flow: Active while the browser is running.

---

[Back to Node Index](Index.md)
