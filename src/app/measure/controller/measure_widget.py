# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""

from PyQt5.QtWidgets import QWidget

from src.app.measure.view.MeasureWidget import Ui_MeasureWidget


class QMeasureWidget(QWidget):
    def __init__(self, parent=None, channel_id=None):
        super().__init__(parent)
        self.ui = Ui_MeasureWidget()
        self.ui.setupUi(self)

        if channel_id is not None:
            self.ui.groupBox.setTitle(f"通道 {channel_id}")

    def update_x(self, x1, x2):
        self.ui.labelX1.setText("{:.2f}".format(x1))
        self.ui.labelX2.setText("{:.2f}".format(x2))
        self.ui.labelDeltaX.setText("{:.2f}".format(x2 - x1))

    def update_y(self, y1, y2):
        self.ui.labelY1.setText("{:.2f}".format(y1))
        self.ui.labelY2.setText("{:.2f}".format(y2))
        self.ui.labelDeltaY.setText("{:.2f}".format(y2 - y1))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = QMeasureWidget()
    window.show()
    sys.exit(app.exec())
