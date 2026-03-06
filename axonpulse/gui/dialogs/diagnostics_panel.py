import os
import json
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DiagnosticsPanel(QDialog):
    """
    A non-blocking tool window that appears when a graph Panics (unhandled exception).
    Displays the Failing Node, Error Message, Stack Trace, and active payloads.
    Also acts as the Breakpoint Controller.
    """
    def __init__(self, parent=None, is_breakpoint=False):
        super().__init__(parent)
        title = "Breakpoint Paused" if is_breakpoint else "Diagnostics: Execution Halted"
        self.setWindowTitle(title)
        self.resize(600, 450)
        
        # Tool window so it stays on top but doesn't block the UI like a modal
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.is_breakpoint = is_breakpoint
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header Status
        self.status_label = QLabel()
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.status_label.setFont(font)
        
        if self.is_breakpoint:
            self.status_label.setText("⏸️ Breakpoint Hit")
            self.status_label.setStyleSheet("color: #ffaa00;")
        else:
            self.status_label.setText("❌ Unhandled Exception (Panic)")
            self.status_label.setStyleSheet("color: #ff4444;")
            
        layout.addWidget(self.status_label)
        
        # Node Name & Error
        self.node_info_label = QLabel("Node: Unknown")
        self.node_info_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.node_info_label)
        
        self.error_msg_label = QLabel("")
        self.error_msg_label.setWordWrap(True)
        self.error_msg_label.setStyleSheet("color: #ffcccc; margin-bottom: 10px;")
        layout.addWidget(self.error_msg_label)

        # Stack Trace / Data Output
        layout.addWidget(QLabel("Telemetry / Payloads:"))
        self.data_view = QTextEdit()
        self.data_view.setReadOnly(True)
        self.data_view.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas;")
        layout.addWidget(self.data_view)

        # Controls
        control_layout = QHBoxLayout()
        
        if self.is_breakpoint:
             resume_btn = QPushButton("▶ Resume Execution")
             resume_btn.setStyleSheet("background-color: #2e7d32; color: white; padding: 5px;")
             resume_btn.clicked.connect(self.on_resume)
             control_layout.addWidget(resume_btn)
             
             step_btn = QPushButton("⏭ Step Over")
             step_btn.clicked.connect(self.on_step)
             control_layout.addWidget(step_btn)
             
        close_btn = QPushButton("Dismiss")
        close_btn.clicked.connect(self.close)
        control_layout.addWidget(close_btn)
        
        layout.addLayout(control_layout)

    def populate(self, error_object=None, node_name="Unknown", message=""):
        """Populates the panel with error data."""
        self.node_info_label.setText(f"Node: {node_name}")
        self.error_msg_label.setText(message)
        
        if error_object:
             # If it's a dict (serialized ErrorObject from the bridge)
             if isinstance(error_object, dict):
                 try:
                     formatted = json.dumps(error_object, indent=2)
                     self.data_view.setPlainText(formatted)
                 except:
                     self.data_view.setPlainText(str(error_object))
             else:
                 self.data_view.setPlainText(str(error_object))
        else:
             self.data_view.setPlainText("No telemetry data available.")

    def on_resume(self):
        """Signals the bridge to resume execution."""
        # 1. Clear Bridge States
        if hasattr(self, 'engine_bridge'):
              self.engine_bridge.set("_AXON_BREAKPOINT_RESUME", True, "DiagnosticsPanel")
              self.engine_bridge.set("_AXON_BREAKPOINT_ACTIVE", False, "DiagnosticsPanel")
              
        # 2. Reset the polling flag in Main Window
        if hasattr(self, 'main_window'):
             self.main_window._diagnostics_shown = False
             
        self.accept()

    def on_step(self):
        """Signals the bridge to step over the breakpoint."""
        if hasattr(self, 'engine_bridge'):
              self.engine_bridge.set("_AXON_BREAKPOINT_STEP", True, "DiagnosticsPanel")
              self.engine_bridge.set("_AXON_BREAKPOINT_ACTIVE", False, "DiagnosticsPanel")
              
        if hasattr(self, 'main_window'):
             self.main_window._diagnostics_shown = False
             
        self.accept()
