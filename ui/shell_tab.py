from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument
from core.shell_backend import ShellBackend
from ui.style import DARK_THEME

class ShellHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_format = QTextCharFormat()
        self.command_format.setForeground(QColor('#2e88ff'))
        self.command_format.setFontWeight(75)
        
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor('#ff5555'))
        
        self.prompt_format = QTextCharFormat()
        self.prompt_format.setForeground(QColor('#00ff88'))

    def highlightBlock(self, text):
        # Highlight command inputs
        if text.startswith('# '):
            self.setFormat(0, len(text), self.prompt_format)
            self.setFormat(0, 2, QTextCharFormat())  # Don't highlight the prompt
            if len(text) > 2:
                self.setFormat(2, len(text)-2, self.command_format)
        
        # Highlight errors
        if '[ERROR]' in text:
            self.setFormat(text.find('[ERROR]'), len(text), self.error_format)

class ShellTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(DARK_THEME)
        self.backend = ShellBackend()
        self.init_ui()
        self.start_shell()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0b0d13;
                color: #c8d1dc;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10.2pt;
                border: 1px solid #1f2733;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.highlighter = ShellHighlighter(self.output_area.document())

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter root shell command...")
        self.input_line.returnPressed.connect(self.send_command)
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #12161f;
                color: #ffffff;
                border: 1px solid #2a2f3a;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10.2pt;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)

        # Setup output polling timer
        self.output_timer = QTimer(self)
        self.output_timer.timeout.connect(self.poll_output)
        self.output_timer.start(50)

    def start_shell(self):
        try:
            if self.backend.start_interactive_shell():
                self.append_text("# Root shell initialized\n", is_prompt=True)
            else:
                self.append_text("[ERROR] Failed to get root shell\n", is_error=True)
        except Exception as e:
            self.append_text(f"[ERROR] {str(e)}\n", is_error=True)

    def poll_output(self):
        output = self.backend.get_output()
        if output:
            self.append_text(output)

    def send_command(self):
        command = self.input_line.text().strip()
        if not command:
            return

        self.append_text(f"# {command}\n", is_command=True)
        try:
            self.backend.send_command(command)
        except Exception as e:
            self.append_text(f"[ERROR] {str(e)}\n", is_error=True)

        self.input_line.clear()

    def append_text(self, text, is_command=False, is_error=False, is_prompt=False):
        self.output_area.moveCursor(QTextCursor.End)
        
        if is_command or is_error or is_prompt:
            # Save current position
            cursor = self.output_area.textCursor()
            pos = cursor.position()
            
            # Insert text
            self.output_area.insertPlainText(text)
            
            # Highlight if needed
            if is_command:
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text)-2)  # Skip prompt
                cursor.mergeCharFormat(self.highlighter.command_format)
            elif is_error:
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(self.highlighter.error_format)
            elif is_prompt:
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(self.highlighter.prompt_format)
        else:
            self.output_area.insertPlainText(text)
            
        self.output_area.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        self.backend.stop_shell()
        event.accept()