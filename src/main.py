from PyQt5.QtGui import QIcon

from src.app.main_window.controller.main_window_controller import MainWindowController
from src.app.main_window.view.main_window import QMyMainWindow
from src.utils.env import check_env
from src.utils.exception_hook import custom_exception_hook

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    check_env()
    sys.excepthook = custom_exception_hook

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":png/images/logo.png"))
    window = QMyMainWindow()
    controller = MainWindowController(window)
    window.show()
    window.resize(1200, 900)
    sys.exit(app.exec())
