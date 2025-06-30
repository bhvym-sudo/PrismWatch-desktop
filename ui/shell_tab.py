# ui/shell_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import QTimer, Qt
from core.shell_backend import ShellBackend

class ShellTab(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = ShellBackend()
        self.init_ui()
        self.start_shell()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 10pt;
                border: 1px solid #404040;
            }
        """)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter shell command...")
        self.input_line.returnPressed.connect(self.send_command)
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 10pt;
                border: 1px solid #404040;
                padding: 5px;
            }
        """)

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)

    def start_shell(self):
        try:
            self.process = self.backend.start_interactive_shell()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.read_output)
            self.timer.start(100)
            self.append_text("Connected to device. Type commands below.\n")
        except Exception as e:
            self.append_text(f"[ERROR] {str(e)}\n")

    def read_output(self):
        if self.process and self.process.stdout:
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.append_text(line)

    def send_command(self):
        command = self.input_line.text().strip()
        if not command:
            return

        self.append_text(f"$ {command}\n")
        try:
            self.backend.send_command(command)
        except Exception as e:
            self.append_text(f"[ERROR] {str(e)}\n")

        self.input_line.clear()

    def append_text(self, text):
        self.output_area.moveCursor(Qt.TextCursor.End)
        self.output_area.insertPlainText(text)
        self.output_area.moveCursor(Qt.TextCursor.End)

    def closeEvent(self, event):
        if self.backend:
            self.backend.stop_shell()
        event.accept()
