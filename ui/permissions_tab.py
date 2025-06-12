from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QPushButton, QGroupBox, QSplitter,
                             QListWidgetItem, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

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
        
        # Header section
        header_layout = QHBoxLayout()
        
        self.package_label = QLabel("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0078d4;")
        header_layout.addWidget(self.package_label)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh Permissions")
        self.refresh_btn.clicked.connect(self.refresh_permissions)
        self.refresh_btn.setEnabled(False)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Create splitter for side-by-side lists
        splitter = QSplitter(Qt.Horizontal)
        
        # Requested Permissions Section
        requested_group = QGroupBox("Requested Permissions")
        requested_layout = QVBoxLayout(requested_group)
        
        self.requested_list = QListWidget()
        self.requested_list.setAlternatingRowColors(True)
        requested_layout.addWidget(self.requested_list)
        
        # Requested permissions count
        self.requested_count_label = QLabel("Count: 0")
        self.requested_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        requested_layout.addWidget(self.requested_count_label)
        
        splitter.addWidget(requested_group)
        
        # Granted Permissions Section
        granted_group = QGroupBox("Granted Permissions")
        granted_layout = QVBoxLayout(granted_group)
        
        self.granted_list = QListWidget()
        self.granted_list.setAlternatingRowColors(True)
        granted_layout.addWidget(self.granted_list)
        
        # Granted permissions count
        self.granted_count_label = QLabel("Count: 0")
        self.granted_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        granted_layout.addWidget(self.granted_count_label)
        
        splitter.addWidget(granted_group)
        
        # Set equal sizes for both panels
        splitter.setSizes([400, 400])
        layout.addWidget(splitter)
        
        # Permission Details Section
        details_group = QGroupBox("Permission Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(150)
        self.details_text.setReadOnly(True)
        self.details_text.setPlainText("Select a permission from the lists above to view details...")
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # Connect list selection events
        self.requested_list.itemSelectionChanged.connect(self.on_permission_selected)
        self.granted_list.itemSelectionChanged.connect(self.on_permission_selected)
        
        # Add initial message
        self.show_no_package_message()
        
    def show_no_package_message(self):
        """Show message when no package is selected"""
        self.package_label.setText("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #888888;")
        
        # Add placeholder items
        placeholder_item = QListWidgetItem("📱 Select a package from the Home tab to view permissions")
        placeholder_item.setForeground(Qt.gray)
        placeholder_item.setFlags(Qt.NoItemFlags)  # Make it non-selectable
        self.requested_list.addItem(placeholder_item)
        
        placeholder_item2 = QListWidgetItem("📱 Select a package from the Home tab to view permissions")
        placeholder_item2.setForeground(Qt.gray)
        placeholder_item2.setFlags(Qt.NoItemFlags)
        self.granted_list.addItem(placeholder_item2)
    
    def refresh_permissions(self):
    # You can later fill this function to reload permissions when user clicks refresh
        pass

        
    def load_package_permissions(self, package_name):
        """Load permissions for the selected package"""
        self.current_package = package_name
        self.package_label.setText(f"Package: {package_name}")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0078d4;")
        self.refresh_btn.setEnabled(True)
        
        # Clear previous data
        self.requested_list.clear()
        self.granted_list.clear()
        self.details_text.setPlainText("Loading permissions...")
        
        try:
            # Initialize ADB and analyzer if not already done
            if not self.adb:
                self.adb = ADBController()
                self.package_analyzer = PackageAnalyzer(self.adb)
            
            self.status_message.emit(f"Loading permissions for {package_name}...")
            
            # Get package info
            package_info = self.package_analyzer.get_package_info(package_name)
            permissions = package_info.get('permissions', {})
            
            # Populate requested permissions
            requested_perms = permissions.get('requested', [])
            self.populate_permissions_list(self.requested_list, requested_perms, "📋")
            self.requested_count_label.setText(f"Count: {len(requested_perms)}")
            
            # Populate granted permissions
            granted_perms = permissions.get('granted', [])
            self.populate_permissions_list(self.granted_list, granted_perms, "✅")
            self.granted_count_label.setText(f"Count: {len(granted_perms)}")
            
            # Update details
            self.details_text.setPlainText(
                f"Permissions loaded for {package_name}\n"
                f"Requested: {len(requested_perms)} permissions\n"
                f"Granted: {len(granted_perms)} permissions\n\n"
                f"Select a permission from either list to view detailed information."
            )
            
            self.status_message.emit(f"Loaded permissions for {package_name}")
            
        except Exception as e:
            error_msg = f"Error loading permissions: {str(e)}"
            self.status_message.emit(error_msg)
            
            # Show error in lists
            error_item = QListWidgetItem(f"❌ Error: {str(e)}")
            error_item.setForeground(Qt.red)
            error_item.setFlags(Qt.NoItemFlags)
            self.requested_list.addItem(error_item)
            
            error_item2 = QListWidgetItem(f"❌ Error: {str(e)}")
            error_item2.setForeground(Qt.red)
            error_item2.setFlags(Qt.NoItemFlags)
            self.granted_list.addItem(error_item2)
            
            self.details_text.setPlainText(f"Error loading permissions:\n{str(e)}")
            
    def populate_permissions_list(self, list_widget, permissions, icon):
        """Populate a permissions list widget"""
        if not permissions:
            item = QListWidgetItem(f"{icon} No permissions found")
            item.setForeground(Qt.gray)
            item.setFlags(Qt.NoItemFlags)
            list_widget.addItem(item)
            return
            
        for perm in permissions:
            # Clean up permission name for display
            display_perm = perm.strip()
            
            # Color code based on permission type
            item = QListWidgetItem(f"{icon} {display_perm}")
            
            if display_perm.startswith('android.permission.'):
                # System permissions - different colors based on sensitivity
                if any(sensitive in display_perm.lower() for sensitive in 
                       ['camera', 'microphone', 'location', 'contacts', 'sms', 'phone']):
                    item.setForeground(Qt.red)  # High risk
                elif any(moderate in display_perm.lower() for moderate in 
                         ['storage', 'write', 'read', 'internet']):
                    item.setForeground(Qt.yellow)  # Medium risk
                else:
                    item.setForeground(Qt.white)  # Normal
            else:
                # Custom permissions
                item.setForeground(Qt.cyan)
                
            list_widget.addItem(item)
            
    def on_permission_selected(self):
        """Handle permission selection to show details"""
        selected_items = []