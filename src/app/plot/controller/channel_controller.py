# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-29
@Description: 
    This is a brief description of what the script does.
"""

import os
import time

from src.app.plot.model.channel_model import ChannelModel
from src.app.plot.view.plot_widget import QMyPlotWidget


class PlotPathManager:
    base_folder = os.path.join('数据波形', time.strftime("%Y-%m-%d %H-%M-%S"))

    @classmethod
    def _ensure_folder_exists(cls):
        if not os.path.exists(cls.base_folder):
            os.makedirs(cls.base_folder)

    @classmethod
    def update_base_folder(cls, base_folder='数据波形'):
        cls.base_folder = os.path.join(base_folder, time.strftime("%Y-%m-%d %H-%M-%S"))
        cls._ensure_folder_exists()

    def get_save_path(self, channel_id, pulse_id):
        filename = f"通道{channel_id}-脉冲{pulse_id - 4}-脉冲{pulse_id}.png"
        return os.path.join(self.__class__.base_folder, filename)

    def get_final_save_path(self, channel_id):
        filename = f"通道{channel_id}-关闭时.png"
        return os.path.join(self.__class__.base_folder, filename)


class WavePlotController:
    def __init__(self, channel_id, plot_widget: QMyPlotWidget, color):
        self.channel_id = channel_id
        self.plot_widget = plot_widget
        self.data_model = ChannelModel(channel_id)
        self.path_manager = PlotPathManager()  # 初始化路径管理器

        if color == "red":
            self.curves, self.wave_labels = self.plot_widget.create_channel_curves(255, 0, 0, 0.5)
        else:
            self.curves, self.wave_labels = self.plot_widget.create_channel_curves(0, 255, 0, 0.3)

    def update_plot(self, pulse_id, new_waveform_data):
        # 处理数据
        self.data_model.receive_new_waveform_data(new_waveform_data)
        # 更新标签
        self.plot_widget.update_labels(pulse_id, self.wave_labels)
        # 更新图形
        self.plot_widget.update_curve(self.curves, self.data_model.wave_data)

        # 检查 pulse_id 是否为 5 的倍数
        if pulse_id % 5 == 0:
            save_path = self.path_manager.get_save_path(self.channel_id, pulse_id)
            self.plot_widget.export_plot(save_path)

    def save_final_plot(self):
        self.plot_widget.export_plot(self.path_manager.get_final_save_path(self.channel_id))

    def clear_plot(self):
        self.plot_widget.clear_plot(self.curves, self.wave_labels)
