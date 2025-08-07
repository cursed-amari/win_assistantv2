from PyQt6.QtWidgets import QApplication

import sys

from main_window import MainWindowView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowView()
    window.show()
    sys.exit(app.exec())
