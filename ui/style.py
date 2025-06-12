DARK_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QMainWindow {
    background-color: #2b2b2b;
}

QTabWidget {
    background-color: #2b2b2b;
    border: none;
}

QTabWidget::pane {
    border: 1px solid #404040;
    background-color: #2b2b2b;
    margin-top: -1px;
}

QTabBar::tab {
    background-color: #404040;
    color: #ffffff;
    padding: 8px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 100px;
}

QTabBar::tab:selected {
    background-color: #0078d4;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #505050;
}

QListWidget {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    color: #ffffff;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
    padding: 5px;
    border-radius: 4px;
}

QListWidget::item {
    padding: 4px;
    border-bottom: 1px solid #404040;
}

QListWidget::item:selected {
    background-color: #0078d4;
}

QListWidget::item:hover {
    background-color: #404040;
}

QComboBox {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    color: #ffffff;
    padding: 5px;
    border-radius: 4px;
    min-height: 20px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    color: #ffffff;
    selection-background-color: #0078d4;
}

QPushButton {
    background-color: #0078d4;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #404040;
    color: #808080;
}

QLabel {
    color: #ffffff;
    background-color: transparent;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #404040;
    border-radius: 5px;
    margin-top: 10px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

QScrollBar:vertical {
    background-color: #2b2b2b;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #404040;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #505050;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QScrollBar:horizontal {
    background-color: #2b2b2b;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #404040;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #505050;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}

QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    color: #ffffff;
    border-radius: 4px;
    padding: 5px;
}

QStatusBar {
    background-color: #404040;
    color: #ffffff;
    border-top: 1px solid #505050;
}
"""