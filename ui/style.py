DARK_THEME = """
QWidget {
    background-color: #0f111a;
    color: #c8d1dc;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10.5pt;
}

QMainWindow {
    background-color: #0f111a;
}

QTabWidget::pane {
    border: 1px solid #1f2733;
    background-color: #0f111a;
}

QTabBar::tab {
    background-color: #1a1f2b;
    color: #c8d1dc;
    padding: 8px 18px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 100px;
}

QTabBar::tab:selected {
    background-color: #2e88ff;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #1f2633;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #1f2733;
    border-radius: 5px;
    margin-top: 10px;
    color: #c8d1dc;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #7abaff;
}

QLabel {
    color: #7abaff;
}

QComboBox {
    background-color: #12161f;
    border: 1px solid #2a2f3a;
    color: #ffffff;
    padding: 5px;
    border-radius: 3px;
}

QComboBox::drop-down {
    border: none;
    width: 18px;
}

QComboBox QAbstractItemView {
    background-color: #12161f;
    border: 1px solid #2a2f3a;
    selection-background-color: #2e88ff;
    color: #ffffff;
}

QListWidget {
    background-color: #12161f;
    border: 1px solid #2a2f3a;
    color: #c8d1dc;
    selection-background-color: #2e88ff;
    padding: 5px;
}

QListWidget::item {
    padding: 5px;
}

QListWidget::item:selected {
    background-color: #2e88ff;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #1f2733;
}

QPushButton {
    background-color: #2e88ff;
    color: #ffffff;
    border: none;
    padding: 7px 14px;
    border-radius: 3px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1f7ae0;
}

QPushButton:pressed {
    background-color: #1c6bd1;
}

QPushButton:disabled {
    background-color: #2a2f3a;
    color: #777777;
}

QTextEdit, QPlainTextEdit {
    background-color: #0b0d13;
    color: #00ff88;
    border: 1px solid #1f2733;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10.2pt;
    border-radius: 3px;
    padding: 5px;
}

QScrollBar:vertical {
    background: #0f111a;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #2a2f3a;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #3c4453;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}

QStatusBar {
    background-color: #1a1f2b;
    color: #7abaff;
    border-top: 1px solid #1f2733;
}
"""
