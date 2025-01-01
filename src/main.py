from src.app.main_window.controller.main_window_controller import MainWindowController
from src.app.main_window.view.main_window import QMyMainWindow


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QMyMainWindow()
    controller = MainWindowController(window)
    window.show()
    window.resize(1200, 900)
    sys.exit(app.exec())
