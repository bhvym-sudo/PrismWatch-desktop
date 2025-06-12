from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from .style import DARK_THEME
from .home_tab import HomeTab
from .permissions_tab import PermissionsTab
from .process_tree_tab import ProcessTreeTab

class MainWindow(QMainWindow):
    # Signal to communicate package selection between tabs
    package_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.selected_package = None
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        self.setWindowTitle("PrismWatch - Android Forensic Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Apply dark theme
        self.setStyleSheet(DARK_THEME)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        layout.addWidget(self.tab_widget)
        
        # Initialize tabs
        self.home_tab = HomeTab()
        self.permissions_tab = PermissionsTab()
        self.process_tree_tab = ProcessTreeTab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.home_tab, "🏠 Home")
        self.tab_widget.addTab(self.permissions_tab, "🔒 Permissions")
        self.tab_widget.addTab(self.process_tree_tab, "🌳 Process Tree")
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Select a device and package to begin analysis")
        
    def setup_connections(self):
        """Setup signal connections between tabs"""
        # Connect home tab package selection to other tabs
        self.home_tab.package_selected.connect(self.on_package_selected)
        
        # Connect package selection signal to other tabs
        self.package_selected.connect(self.permissions_tab.load_package_permissions)
        self.package_selected.connect(self.process_tree_tab.load_package_processes)
        
        # Connect status updates
        self.home_tab.status_message.connect(self.update_status)
        self.permissions_tab.status_message.connect(self.update_status)
        self.process_tree_tab.status_message.connect(self.update_status)
        
    def on_package_selected(self, package_name):
        """Handle package selection from home tab"""
        self.selected_package = package_name
        self.package_selected.emit(package_name)
        self.update_status(f"Package selected: {package_name}")
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.showMessage(message)
        
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self, 
            'Exit PrismWatch', 
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()