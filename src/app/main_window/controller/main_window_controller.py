# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-01-01
@Description: 
    This is a brief description of what the script does.
"""
import queue
import threading

from PyQt5.QtCore import QTimer

from src.app.log_tab.controller.log_widget_controller import LogTabController
from src.app.main_window.view.main_window import QMyMainWindow
from src.app.plot.controller.channel_controller import WavePlotController
from src.service.communication.udp_server import UDPServer
from src.service.log.my_logger import get_logger


class MainWindowController:
    def __init__(self, window: QMyMainWindow):
        self.window = window
        self._udp_server: UDPServer = None
        self._communicate_thread = None
        self.plot_controller = {}

        self.data_queue = queue.Queue()  # 使用队列存储待处理数据
        self.timer = QTimer()
        self.timer.setInterval(50)      # 50ms绘制一次波形，防止界面卡顿
        self.timer.timeout.connect(self._delay_update)

        self._init_plot_controller()
        self.log_controller = LogTabController(self.window.uiLog)
        self.window.uiUpdConfig.confirmed.connect(self.on_udp_config_confirmed)

    def _init_plot_controller(self):
        # 每个屏对应两个波形
        for index, plot_widget in self.window.get_plot_widgets().items():
            controller1 = WavePlotController(2 * index - 1, plot_widget, "red")
            self.plot_controller[2 * index - 1] = controller1

            controller2 = WavePlotController(2 * index, plot_widget, "green")
            self.plot_controller[2 * index] = controller2

    def on_udp_config_confirmed(self):
        if self.window.uiUpdConfig.is_open:
            self.timer.stop()
            self._udp_server.stop()
            self._communicate_thread.join()
            self.window.uiUpdConfig.set_closed()
        else:
            self._udp_server = UDPServer(*self.window.uiUpdConfig.get_udp_config())
            self._udp_server.connect_callback(self.process_succeeded_data, self.process_erred_data)
            self._communicate_thread = threading.Thread(target=self._udp_server.run)
            self._communicate_thread.start()
            self.timer.start()
            self.window.uiUpdConfig.set_open()

    def process_succeeded_data(self, channel_id, pulse_id, sample_points, hex_data):
        self.data_queue.put((channel_id, pulse_id, sample_points, hex_data))
        self.log_controller.append_success_text(f"接收通道{channel_id} 脉冲{pulse_id}数据成功\n"
                                                f"数据：{sample_points}\n"
                                                f"原始数据：{hex_data}")

    def process_erred_data(self, error_msg, hex_data):
        text = f"{error_msg} >>> {hex_data}"
        self.log_controller.append_error_text(text)
        get_logger().error(text)

    def _delay_update(self):
        if not self.data_queue.empty():
            channel_id, pulse_id, sample_points, hex_data = self.data_queue.get()
            if channel_id in self.plot_controller:
                self.plot_controller[channel_id].update_plot(pulse_id, sample_points)
