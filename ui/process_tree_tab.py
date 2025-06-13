from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QPushButton, QGroupBox, QTextEdit,
                             QListWidgetItem, QSplitter, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.adb_controller import ADBController, ADBError
from core.package_analyzer import PackageAnalyzer
from core.process_analyzer import ProcessAnalyzer
from core.uid_mapper import UIDMapper

class ProcessTreeTab(QWidget):
    status_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_package = None
        self.current_uid = None
        self.adb = None
        self.package_analyzer = None
        self.process_analyzer = None
        self.uid_mapper = None
        self.all_processes = []
        self.package_processes = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        
        header_layout = QHBoxLayout()
        
        self.package_label = QLabel("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0078d4;")
        header_layout.addWidget(self.package_label)
        
        header_layout.addStretch()
        
        
        self.show_all_checkbox = QCheckBox("Show all processes")
        self.show_all_checkbox.stateChanged.connect(self.toggle_process_view)
        self.show_all_checkbox.setEnabled(False)
        header_layout.addWidget(self.show_all_checkbox)
        
        
        self.refresh_btn = QPushButton("Refresh Processes")
        self.refresh_btn.clicked.connect(self.refresh_processes)
        self.refresh_btn.setEnabled(False)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        
        splitter = QSplitter(Qt.Vertical)
        
        
        tree_group = QGroupBox("Process Tree")
        tree_layout = QVBoxLayout(tree_group)
        
        
        self.uid_label = QLabel("UID: Not determined")
        self.uid_label.setStyleSheet("color: #888888; font-size: 10pt;")
        tree_layout.addWidget(self.uid_label)
        
        self.process_list = QListWidget()
        self.process_list.setAlternatingRowColors(True)
        self.process_list.setFont(QFont("Courier New", 9))  
        tree_layout.addWidget(self.process_list)
        
        
        self.process_count_label = QLabel("Processes: 0")
        self.process_count_label.setStyleSheet("color: #888888; font-size: 9pt;")
        tree_layout.addWidget(self.process_count_label)
        
        splitter.addWidget(tree_group)
        
        
        details_group = QGroupBox("Process Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(200)
        self.details_text.setPlainText("Select a process from the tree above to view details...")
        details_layout.addWidget(self.details_text)
        
        splitter.addWidget(details_group)
        
        
        splitter.setSizes([500, 200])
        layout.addWidget(splitter)
        
        
        self.process_list.itemSelectionChanged.connect(self.on_process_selected)
        
        
        self.show_no_package_message()
        
    def show_no_package_message(self):
        """Show message when no package is selected"""
        self.package_label.setText("No package selected")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #888888;")
        
        
        placeholder_item = QListWidgetItem("📱 Select a package from the Home tab to view process tree")
        placeholder_item.setForeground(Qt.gray)
        placeholder_item.setFlags(Qt.NoItemFlags)
        self.process_list.addItem(placeholder_item)
        
    def load_package_processes(self, package_name):
        """Load process tree for the selected package"""
        self.current_package = package_name
        self.package_label.setText(f"Package: {package_name}")
        self.package_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0078d4;")
        self.refresh_btn.setEnabled(True)
        self.show_all_checkbox.setEnabled(True)
        
        
        self.process_list.clear()
        self.details_text.setPlainText("Loading processes...")
        self.uid_label.setText("UID: Determining...")
        
        try:
            
            if not self.adb:
                self.adb = ADBController()
                self.process_analyzer = ProcessAnalyzer(self.adb)
                self.uid_mapper = UIDMapper(self.adb)
            
            self.status_message.emit(f"Loading processes for {package_name}...")
            
            
            self.current_uid = self.uid_mapper.get_uid_for_package(package_name)
            self.uid_label.setText(f"UID: {self.current_uid}")
            
            
            self.all_processes = self.process_analyzer.get_processes()
            
            
            self.package_processes = self.process_analyzer.get_processes(filter_uid=self.current_uid)
            
            
            self.update_process_display()
            
            self.status_message.emit(f"Loaded {len(self.package_processes)} processes for {package_name}")
            
        except Exception as e:
            error_msg = f"Error loading processes: {str(e)}"
            self.status_message.emit(error_msg)
            
            
            error_item = QListWidgetItem(f"❌ Error: {str(e)}")
            error_item.setForeground(Qt.red)
            error_item.setFlags(Qt.NoItemFlags)
            self.process_list.addItem(error_item)
            
            self.details_text.setPlainText(f"Error loading processes:\n{str(e)}")
            self.uid_label.setText("UID: Error")
            
    def update_process_display(self):
        """Update the process display based on current settings"""
        self.process_list.clear()
        
        if self.show_all_checkbox.isChecked():
            processes_to_show = self.all_processes
            title_suffix = " (All Processes)"
        else:
            processes_to_show = self.package_processes
            title_suffix = f" (UID: {self.current_uid})"
            
        if not processes_to_show:
            item = QListWidgetItem("No processes found")
            item.setForeground(Qt.gray)
            item.setFlags(Qt.NoItemFlags)
            self.process_list.addItem(item)
            self.process_count_label.setText("Processes: 0")
            return
            
        
        tree = self.process_analyzer.build_process_tree(processes_to_show)
        self.display_process_tree_in_list(tree, processes_to_show)
        
        
        self.process_count_label.setText(f"Processes: {len(processes_to_show)}{title_suffix}")
        
        
        if self.show_all_checkbox.isChecked():
            self.details_text.setPlainText(
                f"Showing all system processes\n"
                f"Total processes: {len(processes_to_show)}\n"
                f"Package processes (UID {self.current_uid}): {len(self.package_processes)}\n\n"
                f"Select a process to view details."
            )
        else:
            self.details_text.setPlainText(
                f"Showing processes for {self.current_package}\n"
                f"UID: {self.current_uid}\n"
                f"Process count: {len(processes_to_show)}\n\n"
                f"Select a process to view details."
            )
            
    def display_process_tree_in_list(self, tree, processes):
        """Display process tree in the list widget with proper indentation"""
        
        process_pids = {p['PID'] for p in processes}
        root_processes = [p for p in processes if p['PPID'] not in process_pids]
        
        
        root_processes.sort(key=lambda x: int(x['PID']) if x['PID'].isdigit() else 0)
        
        
        for root in root_processes:
            self.add_process_to_tree(tree, root, 0, processes)
            
    def add_process_to_tree(self, tree, process, level, all_processes):
        """Recursively add process and its children to the tree display"""
        
        indent = "  " * level
        tree_chars = "└─ " if level > 0 else ""
        
        
        pid = process['PID']
        ppid = process['PPID']
        uid = process['UID']
        name = process['NAME']
        
        
        display_text = f"{indent}{tree_chars}PID:{pid} PPID:{ppid} UID:{uid} → {name}"
        
        item = QListWidgetItem(display_text)
        item.setData(Qt.UserRole, process)  
        
        
        if uid == self.current_uid:
            item.setForeground(Qt.green)  
            font = QFont("Courier New", 9)
            font.setBold(True)
            item.setFont(font)
        elif uid.startswith('u0_'):
            item.setForeground(Qt.yellow)  
        elif uid in ['root', 'system', 'shell']:
            item.setForeground(Qt.cyan)  
        else:
            item.setForeground(Qt.white)  
            
        self.process_list.addItem(item)
        
        
        children = tree.get(pid, [])
        children.sort(key=lambda x: int(x['PID']) if x['PID'].isdigit() else 0)
        
        for child in children:
            self.add_process_to_tree(tree, child, level + 1, all_processes)
            
    def on_process_selected(self):
        """Handle process selection to show details"""
        current_item = self.process_list.currentItem()
        if not current_item:
            return
            
        
        process_data = current_item.data(Qt.UserRole)
        if not process_data:
            return
            
        
        details = f"Process Details:\n"
        details += f"{'=' * 50}\n"
        details += f"Process ID (PID): {process_data['PID']}\n"
        details += f"Parent PID (PPID): {process_data['PPID']}\n"
        details += f"User ID (UID): {process_data['UID']}\n"
        details += f"Process Name: {process_data['NAME']}\n\n"
        
        
        if process_data['UID'] == self.current_uid:
            details += f"This process belongs to the selected package: {self.current_package}\n"
        elif process_data['UID'] == 'root':
            details += "This is a root system process\n"
        elif process_data['UID'] == 'system':
            details += "This is a system process\n"
        elif process_data['UID'].startswith('u0_'):
            details += "This is a user application process\n"
        else:
            details += "This is an unknown process type\n"
            
        
        details += f"\nSecurity Notes:\n"
        details += f"- Process running with UID: {process_data['UID']}\n"
        if process_data['UID'] == 'root':
            details += "- Root processes have full system access\n"
        elif process_data['UID'] == self.current_uid:
            details += f"- This process can access all data belonging to {self.current_package}\n"
            
        self.details_text.setPlainText(details)
        
    def toggle_process_view(self):
        """Toggle between showing all processes or just package processes"""
        if hasattr(self, 'all_processes') and self.all_processes:
            self.update_process_display()
            
    def refresh_processes(self):
        """Refresh process tree for current package"""
        if self.current_package:
            self.load_package_processes(self.current_package)