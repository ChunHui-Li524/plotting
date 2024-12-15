# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""


from PyQt5.QtWidgets import QMainWindow, QWidget, QSpacerItem, QSizePolicy

from src.app.main_window.view.MyMainWindow import Ui_MyMainWindow
from src.app.measure.controller.add_widget import QAddWidget
from src.app.measure.controller.measure_widget import QMeasureWidget
from src.app.plot.controller.plot_widget import QMyPlotWidget


class QMyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MyMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("通道测量仪")
        self._init_ui()

    def _init_ui(self):
        for i in range(3):
            for j in range(3):
                self.ui.framePlotGroup.layout().addWidget(QMyPlotWidget(), i, j)

        self.ui.frameMeasure.layout().addWidget(QMeasureWidget())
        self.ui.frameMeasure.layout().addWidget(QMeasureWidget(self, 1))
        self.ui.frameMeasure.layout().addWidget(QMeasureWidget(self, 2))
        self.ui.frameMeasure.layout().addWidget(QMeasureWidget(self, 3))
        self.ui.frameMeasure.layout().addWidget(QAddWidget())
        # self.ui.frameMeasure.layout().addlayout(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.ui.frameMeasure.hide()


    def on_actionStartMeasure_toggled(self, is_checked):
        self.ui.frameMeasure.setHidden(not is_checked)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QMyMainWindow()
    window.show()
    sys.exit(app.exec())
