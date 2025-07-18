

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PrismWatch")
    app.setApplicationVersion("1.0")
    
    
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    