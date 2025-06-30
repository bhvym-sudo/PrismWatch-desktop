from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QGroupBox,
                             QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.adb_controller import ADBController, ADBError
from core.package_analyzer import PackageAnalyzer

class PermissionsTab(QWidget):
    status_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_package = None
        self.adb = None
        self.package_analyzer = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.package_label = QLabel("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #7abaff;")
        header_layout.addWidget(self.package_label)

        header_layout.addStretch()

        self.refresh_btn = QPushButton("Refresh Permissions")
        self.refresh_btn.clicked.connect(self.refresh_permissions)
        self.refresh_btn.setEnabled(False)
        header_layout.addWidget(self.refresh_btn)

        layout.addLayout(header_layout)

        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel("Legend:"))

        granted_legend = QLabel("● Granted")
        granted_legend.setStyleSheet("color: #6bcf7f; font-weight: bold;")
        legend_layout.addWidget(granted_legend)

        dangerous_legend = QLabel("● Dangerous")
        dangerous_legend.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        legend_layout.addWidget(dangerous_legend)

        legend_layout.addStretch()
        layout.addLayout(legend_layout)

        requested_group = QGroupBox("Requested Permissions")
        requested_layout = QVBoxLayout(requested_group)

        self.requested_list = QListWidget()
        self.requested_list.setAlternatingRowColors(True)
        self.requested_list.setStyleSheet("""
            QListWidget {
                alternate-background-color: #12161f;
                background-color: #0b0d13;
                color: #c8d1dc;
                border: 1px solid #1f2733;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 6px;
                border: none;
                min-height: 20px;
            }
            QListWidget::item:selected {
                background-color: #2e88ff;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #1f2733;
            }
        """)
        requested_layout.addWidget(self.requested_list)

        self.requested_count_label = QLabel("Count: 0")
        self.requested_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        requested_layout.addWidget(self.requested_count_label)

        layout.addWidget(requested_group)

        self.show_no_package_message()

    def show_no_package_message(self):
        self.package_label.setText("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #555555;")

        self.requested_list.clear()
        placeholder_item = QListWidgetItem("Select a package from the Home tab to view permissions")
        placeholder_item.setForeground(QColor("#666666"))
        placeholder_item.setFlags(Qt.NoItemFlags)
        self.requested_list.addItem(placeholder_item)

    def refresh_permissions(self):
        if self.current_package:
            self.load_package_permissions(self.current_package)

    def load_package_permissions(self, package_name):
        self.current_package = package_name
        self.package_label.setText(f"Package: {package_name}")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #7abaff;")
        self.refresh_btn.setEnabled(True)
        self.requested_list.clear()

        try:
            if not self.adb:
                self.adb = ADBController()
                self.package_analyzer = PackageAnalyzer(self.adb)

            self.status_message.emit(f"Loading permissions for {package_name}...")
            package_info = self.package_analyzer.get_package_info(package_name)
            permissions = package_info.get('permissions', {})
            requested_perms = permissions.get('requested', [])
            granted_perms = permissions.get('granted', [])

            self.populate_permissions_list(self.requested_list, requested_perms, granted_perms)
            self.requested_count_label.setText(f"Count: {len(requested_perms)}")
            self.status_message.emit(f"Loaded permissions for {package_name}")

        except Exception as e:
            msg = f"Error loading permissions: {str(e)}"
            self.status_message.emit(msg)

            error_item = QListWidgetItem(f"Error: {str(e)}")
            error_item.setForeground(QColor("#ff6b6b"))
            error_item.setFlags(Qt.NoItemFlags)
            self.requested_list.addItem(error_item)

    def populate_permissions_list(self, list_widget, requested_permissions, granted_permissions):
        if not requested_permissions:
            item = QListWidgetItem("No permissions found")
            item.setForeground(QColor("#888888"))
            item.setFlags(Qt.NoItemFlags)
            list_widget.addItem(item)
            return

        granted_set = set(granted_permissions) if granted_permissions else set()

        for perm in requested_permissions:
            display_perm = perm.strip()
            item = QListWidgetItem(display_perm)

            if display_perm in granted_set:
                item.setForeground(QColor("#6bcf7f"))  # green
            elif self.is_dangerous_permission(display_perm):
                item.setForeground(QColor("#ff6b6b"))  # red
            else:
                item.setForeground(QColor("#c8d1dc"))  # default gray-blue

            list_widget.addItem(item)

    def is_dangerous_permission(self, permission):
        dangerous_keywords = [
            'camera', 'microphone', 'location', 'contacts', 'sms', 'phone',
            'call_log', 'calendar', 'body_sensors', 'storage', 'write_external_storage',
            'read_external_storage', 'record_audio', 'access_fine_location',
            'access_coarse_location', 'read_contacts', 'write_contacts',
            'read_sms', 'send_sms', 'receive_sms', 'read_phone_state',
            'call_phone', 'read_call_log', 'write_call_log'
        ]
        permission_lower = permission.lower()
        return any(keyword in permission_lower for keyword in dangerous_keywords)
