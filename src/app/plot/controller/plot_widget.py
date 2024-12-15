# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""


from PyQt5.QtWidgets import QWidget
from pyqtgraph import PlotWidget


class QMyPlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self):
        self.setXRange(0, 1000)
        self.setYRange(0, 1)