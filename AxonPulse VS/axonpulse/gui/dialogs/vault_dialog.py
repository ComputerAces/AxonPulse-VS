import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from axonpulse.utils.vault import vault

class VaultDialog(QDialog):
    """
    A UI panel for managing encrypted secrets in the local Enterprise Vault.
    Keys are visible, but values are hidden by default (bullet points).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enterprise Vault (Secrets)")
        self.resize(500, 400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header Info
        info_label = QLabel(
            "<b>Enterprise Vault</b><br>"
            "Secrets are encrypted using a machine-specific key and saved locally.<br>"
            "They will <b>never</b> be exported when you share a .syp graph file."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Key (Alias)", "Actions"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 80)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Add Secret Area
        add_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Key (e.g. OPENAI_API_KEY)")
        self.val_input = QLineEdit()
        self.val_input.setPlaceholderText("Secret Value")
        self.val_input.setEchoMode(QLineEdit.EchoMode.Password) # Mask input
        
        add_btn = QPushButton("Add Secret")
        add_btn.clicked.connect(self.add_secret)
        
        add_layout.addWidget(self.key_input, 1)
        add_layout.addWidget(self.val_input, 2)
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def refresh_table(self):
        self.table.setRowCount(0)
        keys = vault.list_keys()
        
        for row, key in enumerate(keys):
            self.table.insertRow(row)
            
            # Key Item
            key_item = QTableWidgetItem(key)
            self.table.setItem(row, 0, key_item)
            
            # Actions (Delete)
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("color: #ff4444; border: 1px solid #ff4444; padding: 2px;")
            del_btn.clicked.connect(lambda checked, k=key: self.delete_secret(k))
            
            self.table.setCellWidget(row, 1, del_btn)

    def add_secret(self):
        key = self.key_input.text().strip()
        val = self.val_input.text().strip()
        
        if not key or not val:
            QMessageBox.warning(self, "Invalid Input", "Both Key and Secret are required.")
            return

        if key in vault.list_keys():
            reply = QMessageBox.question(
                self, "Overwrite?", 
                f"The key '{key}' already exists in the Vault. Overwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        vault.set_secret(key, val)
        self.key_input.clear()
        self.val_input.clear()
        self.refresh_table()

    def delete_secret(self, key):
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete the secret '{key}' from the Vault?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            vault.delete_secret(key)
            self.refresh_table()
