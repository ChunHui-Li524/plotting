from src.app.main_window.view.main_window import QMyMainWindow


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QMyMainWindow()
    window.show()
    sys.exit(app.exec())
