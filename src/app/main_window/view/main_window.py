# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""

from PyQt5.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy

from src.app.log_tab.view.log_widget import QLogWidget
from src.app.main_window.view.ui.MyMainWindow import Ui_MyMainWindow
from src.app.measure.controller.add_widget import QAddWidget
from src.app.measure.controller.config_widget import QMeasureConfigWidget
from src.app.measure.controller.measure_widget import QMeasureWidget
from src.app.plot.view.plot_widget import QMyPlotWidget
from src.app.udp_config.controller.udp_config_widget import QUdpConfigWidget


class QMyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MyMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("18通道AD测量仪")
        self._plot_widgets = {}
        self._measure_widgets = {}
        self._init_ui()

    def _init_ui(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab)
        self.uiUpdConfig = QUdpConfigWidget(self)
        self._init_log_tab()
        self._init_plot_frame()
        self._init_measure_frame()
        self.ui.actionUDPConfig.triggered.connect(self.uiUpdConfig.show)
        self.ui.actionMeasureConfig.triggered.connect(self.uiMeasureConfigWidget.show)
        for i in range(1, 10):
            self._plot_widgets[i].x_changed.connect(self._measure_widgets[i].update_x)
            self._plot_widgets[i].y_changed.connect(self._measure_widgets[i].update_y)

    def _init_log_tab(self):
        self.uiLog = QLogWidget(self)
        self.ui.tabWidget.addTab(self.uiLog, "日志")

    def _init_plot_frame(self):
        """
        生成3*3的绘图区域
        :return:
        """
        index = 1
        for i in range(3):
            widget = QMyPlotWidget()
            self.ui.frame.layout().addWidget(widget)
            self._plot_widgets[index] = widget
            index += 1
        for i in range(3):
            widget = QMyPlotWidget()
            self.ui.frame_2.layout().layout().addWidget(widget)
            self._plot_widgets[index] = widget
            index += 1
        for i in range(3):
            widget = QMyPlotWidget()
            self.ui.frame_3.layout().addWidget(widget)
            self._plot_widgets[index] = widget
            index += 1

    def get_plot_widgets(self):
        return self._plot_widgets

    def _init_measure_frame(self):
        """
        初始化测量区域，默认显示所有区域
        :return:
        """
        self._add_widget = QAddWidget(self)
        self.uiMeasureConfigWidget = QMeasureConfigWidget(self)
        self._add_widget.clicked.connect(self.uiMeasureConfigWidget.show)
        self.uiMeasureConfigWidget.config_confirmed.connect(self.on_config_confirmed)

        # 第一个测量说明控件
        self.ui.frameMeasure.layout().addWidget(QMeasureWidget())
        # 默认九个测量页面
        for i in range(1, 10):
            widget = QMeasureWidget(self, i)
            self.ui.frameMeasure.layout().addWidget(widget)
            self._measure_widgets[i] = widget
        # 一个设置按钮
        self.ui.frameMeasure.layout().addWidget(self._add_widget)
        # 一个弹簧美化
        self.ui.frameMeasure.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.ui.frameMeasure.hide()

    def on_config_confirmed(self, screen_ids):
        # 配置确定后，先显示测量控件
        self.ui.actionStartMeasure.setChecked(True)
        # 根据配置情况显示或隐藏UI
        for index in range(1, 10):
            if index in screen_ids:
                self._measure_widgets[index].show()
                self._plot_widgets[index].set_ruler_visible(True)
            else:
                self._measure_widgets[index].hide()
                self._plot_widgets[index].set_ruler_visible(False)

    def on_actionStartMeasure_toggled(self, is_checked):
        self.ui.frameMeasure.setHidden(not is_checked)
        # 如果选中，则显示测量尺
        if is_checked:
            self.uiMeasureConfigWidget.on_btnConfirm_clicked()
        else:
            for plot_widget in self._plot_widgets.values():
                plot_widget.set_ruler_visible(False)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QMyMainWindow()
    window.show()
    sys.exit(app.exec())
