# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-15
@Description: 
    This is a brief description of what the script does.
"""
import threading

from PyQt5.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy

from src.app.main_window.view.ui.MyMainWindow import Ui_MyMainWindow
from src.app.measure.controller.add_widget import QAddWidget
from src.app.measure.controller.config_widget import QMeasureConfigWidget
from src.app.measure.controller.measure_widget import QMeasureWidget
from src.app.plot.view.plot_widget import QMyPlotWidget
from src.app.udp_config.controller.udp_config_widget import QUdpConfigWidget
from src.service.communication.udp_server import UDPServer


class QMyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MyMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("通道测量仪")
        self._plot_widgets = {}
        self._measure_widgets = {}
        self._udp_server: UDPServer = None
        self._communicate_thread = None
        self._init_ui()

    def _init_ui(self):
        self._init_udp_config_widget()
        self._init_plot_frame()
        self._init_measure_frame()
        self.ui.actionUDPConfig.triggered.connect(self._udp_config.show)
        self.ui.actionMeasureConfig.triggered.connect(self._config_widget.show)

    def _init_udp_config_widget(self):
        self._udp_config = QUdpConfigWidget(self)
        self._udp_config.confirmed.connect(self.on_udp_config_confirmed)

    def on_udp_config_confirmed(self):
        if self._udp_config.is_open:
            self._udp_server.stop()
            self._communicate_thread.join()
            self._udp_config.set_closed()
        else:
            self._udp_server = UDPServer(*self._udp_config.get_udp_config())
            self._udp_server.connect_callback(print, print)
            self._communicate_thread = threading.Thread(target=self._udp_server.run)
            self._communicate_thread.start()
            self._udp_config.set_open()

    def _init_plot_frame(self):
        """
        生成3*3的绘图区域
        :return:
        """
        index = 1
        for i in range(3):
            for j in range(3):
                widget = QMyPlotWidget()
                self.ui.framePlotGroup.layout().addWidget(widget, i, j)

                self._plot_widgets[index] = widget
                index += 1

    def _init_measure_frame(self):
        """
        初始化测量区域，默认显示所有区域
        :return:
        """
        self._add_widget = QAddWidget(self)
        self._config_widget = QMeasureConfigWidget(self)
        self._add_widget.clicked.connect(self._config_widget.show)
        self._config_widget.config_confirmed.connect(self.on_config_confirmed)

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
                self._plot_widgets[index].show_ruler()
            else:
                self._measure_widgets[index].hide()
                self._plot_widgets[index].hide_ruler()

    def on_actionStartMeasure_toggled(self, is_checked):
        self.ui.frameMeasure.setHidden(not is_checked)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QMyMainWindow()
    window.show()
    sys.exit(app.exec())
