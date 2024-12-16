# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""
from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget

from src.app.measure.view.AddWidget import Ui_AddWidget


class QAddWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddWidget()
        self.ui.setupUi(self)
        self.setMinimumWidth(50)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.clicked.emit()  # 发出信号
            return True
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = QAddWidget()
    window.show()
    sys.exit(app.exec())
