# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-29
@Description: 
    This is a brief description of what the script does.
"""

from src.app.plot.model.channel_model import ChannelModel
from src.app.plot.view.plot_widget import QMyPlotWidget


class WavePlotController:
    def __init__(self, channel_id, plot_widget: QMyPlotWidget, color):
        self.channel_id = channel_id
        self.plot_widget = plot_widget
        self.data_model = ChannelModel(channel_id)
        if color == "red":
            self.curves, self.wave_labels = self.plot_widget.create_channel_curves(255, 0, 0)
        else:
            self.curves, self.wave_labels = self.plot_widget.create_channel_curves(0, 255, 0)

    def update_plot(self, pulse_id, new_waveform_data):
        # 处理数据
        self.data_model.receive_new_waveform_data(new_waveform_data)
        # 更新标签
        self.plot_widget.update_labels(pulse_id, self.wave_labels)
        # 更新图形,
        self.plot_widget.update_curve(self.curves, self.data_model.wave_data)

    def export_plot(self, save_path):
        self.plot_widget.export_plot(save_path)

    def clear_plot(self):
        self.plot_widget.clear_plot(self.curves, self.wave_labels)

