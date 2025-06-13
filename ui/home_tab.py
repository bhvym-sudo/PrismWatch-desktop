from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QComboBox, QPushButton, QGroupBox,
                             QListWidgetItem, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.adb_controller import ADBController, ADBError
from core.package_analyzer import PackageAnalyzer

class HomeTab(QWidget):
    package_selected = pyqtSignal(str)
    status_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.adb = None
        self.package_analyzer = None
        self.installed_apps = []
        self.init_ui()
        self.check_device_connection()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel(
            "PrismWatch is a forensic analysis tool for Android devices.\n\n"
            "Requirements:\n"
            "• Rooted Android device\n"
            "• ADB debugging enabled\n"
            "• Device connected via USB\n\n"
            "Select an application above to view its permissions and process tree."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #cccccc;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        
        device_group = QGroupBox("Device Connection Status")
        device_layout = QVBoxLayout(device_group)
        
        self.device_status_list = QListWidget()
        self.device_status_list.setMaximumHeight(100)
        device_layout.addWidget(self.device_status_list)
        
        
        refresh_btn = QPushButton("Refresh Connection")
        refresh_btn.clicked.connect(self.check_device_connection)
        device_layout.addWidget(refresh_btn)
        
        layout.addWidget(device_group)
        
        
        app_group = QGroupBox("Application Selection")
        app_layout = QVBoxLayout(app_group)
        
        
        instruction_label = QLabel("Select an installed application to analyze:")
        instruction_label.setWordWrap(True)
        app_layout.addWidget(instruction_label)
        
        
        self.app_combo = QComboBox()
        self.app_combo.setEnabled(False)
        self.app_combo.currentTextChanged.connect(self.on_app_selected)
        app_layout.addWidget(self.app_combo)
        
        
        refresh_apps_btn = QPushButton("Refresh App List")
        refresh_apps_btn.clicked.connect(self.load_installed_apps)
        refresh_apps_btn.setEnabled(False)
        self.refresh_apps_btn = refresh_apps_btn
        app_layout.addWidget(refresh_apps_btn)
        
        
        self.selected_app_label = QLabel("No application selected")
        self.selected_app_label.setStyleSheet("color: #888888; font-style: italic;")
        app_layout.addWidget(self.selected_app_label)
        
        layout.addWidget(app_group)
        
        
        
        
        
        layout.addStretch()
        
    def check_device_connection(self):
        """Check if device is connected and rooted"""
        self.device_status_list.clear()
        
        try:
            
            self.adb = ADBController()
            
            
            result = self.adb.execute_command("echo 'test'", timeout=5)
            if result == "test":
                self.add_status_item("ADB Connection: Connected", True)
                
                
                try:
                    root_result = self.adb.execute_command("whoami", use_su=True, timeout=10)
                    if "root" in root_result.lower():
                        self.add_status_item("Root Access: Available", True)
                        self.device_connected = True
                        self.enable_app_selection()
                        self.status_message.emit("Device connected and rooted - Ready for analysis")
                    else:
                        self.add_status_item("Root Access: Not available", False)
                        self.device_connected = False
                        self.disable_app_selection()
                        self.status_message.emit("Device connected but not rooted")
                except Exception:
                    self.add_status_item("Root Access: Not available", False)
                    self.device_connected = False
                    self.disable_app_selection()
                    self.status_message.emit("Device connected but not rooted")
            else:
                self.add_status_item("ADB Connection: Failed", False)
                self.device_connected = False
                self.disable_app_selection()
                
        except ADBError as e:
            self.add_status_item("Device Not Detected", False)
            self.add_status_item(f"Error: {str(e)}", False)
            self.device_connected = False
            self.disable_app_selection()
            self.status_message.emit("No device detected")
        except Exception as e:
            self.add_status_item("Connection Error", False)
            self.add_status_item(f"Error: {str(e)}", False)
            self.device_connected = False
            self.disable_app_selection()
            self.status_message.emit("Connection error occurred")
            
    def add_status_item(self, text, is_success):
        """Add a status item to the device status list"""
        item = QListWidgetItem(text)
        if is_success:
            item.setForeground(Qt.green)
        else:
            item.setForeground(Qt.red)
        
        font = QFont()
        font.setBold(True)
        item.setFont(font)
        
        self.device_status_list.addItem(item)
        
    def enable_app_selection(self):
        """Enable app selection controls"""
        self.app_combo.setEnabled(True)
        self.refresh_apps_btn.setEnabled(True)
        self.load_installed_apps()
        
    def disable_app_selection(self):
        """Disable app selection controls"""
        self.app_combo.setEnabled(False)
        self.refresh_apps_btn.setEnabled(False)
        self.app_combo.clear()
        self.selected_app_label.setText("No application selected")
        
    def load_installed_apps(self):
        """Load list of installed applications"""
        if not self.adb:
            return
            
        try:
            self.status_message.emit("Loading installed applications...")
            self.package_analyzer = PackageAnalyzer(self.adb)
            
            
            self.installed_apps = self.package_analyzer.get_installed_apps()
            
            
            self.app_combo.clear()
            self.app_combo.addItem("-- Select an application --")
            
            
            sorted_apps = sorted(self.installed_apps, key=lambda x: x[0])
            
            for package_name, uid in sorted_apps:
                display_name = package_name
                
                if package_name.startswith("com.android."):
                    display_name = f"{package_name} (System)"
                elif package_name.startswith("com.google."):
                    display_name = f"{package_name} (Google)"
                    
                self.app_combo.addItem(display_name, package_name)
                
            self.status_message.emit(f"Loaded {len(self.installed_apps)} applications")
            
        except Exception as e:
            self.status_message.emit(f"Error loading applications: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to load applications:\n{str(e)}")
            
    def on_app_selected(self, display_text):

        if display_text == "-- Select an application --" or not display_text:
            self.selected_app_label.setText("No application selected")
            self.selected_app_label.setStyleSheet("color: #888888; font-style: italic;")
            return
            
        
        current_index = self.app_combo.currentIndex()
        if current_index > 0:  
            package_name = self.app_combo.itemData(current_index)
            if package_name:
                self.selected_app_label.setText(f"Selected: {package_name}")
                self.selected_app_label.setStyleSheet("color: #0078d4; font-weight: bold;")
                self.package_selected.emit(package_name)
                self.status_message.emit(f"Selected package: {package_name}")