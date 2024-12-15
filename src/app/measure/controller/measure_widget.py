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
    def __init__(self, parent=None, channel_id=None, r=255, g=255, b=255):
        super().__init__(parent)
        self.ui = Ui_MeasureWidget()
        self.ui.setupUi(self)

        if channel_id is not None:
            self.ui.labelChannel.setText(str(channel_id))
        self.ui.labelChannel.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")

    def update_x(self, x1, x2):
        self.ui.labelX1.setText(str(x1))
        self.ui.labelX2.setText(str(x2))
        self.ui.labelDeltaX.setText(str(x2 - x1))

    def update_y(self, y1, y2):
        self.ui.labelY1.setText(str(y1))
        self.ui.labelY2.setText(str(y2))
        self.ui.labelDeltaY.setText(str(y2 - y1))
