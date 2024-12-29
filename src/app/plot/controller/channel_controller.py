# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-29
@Description: 
    This is a brief description of what the script does.
"""
import numpy as np
from pyqtgraph.exporters import ImageExporter

from src.app.plot.view.plot_widget import QMyPlotWidget, SAMPLE_NUM, WAVE_NUM


class WavePlotController:
    def __init__(self, channel_id, plot_widget: QMyPlotWidget):

        self.channel_id = channel_id
        self.plot_widget = plot_widget

        self.wave_data = [np.zeros(SAMPLE_NUM) for _ in range(WAVE_NUM)]

    def update_plot(self, pulse_id, new_waveform_data):
        # 移除第一个波形的数据
        self.wave_data.pop(0)
        # 插入新的波形数据
        self.wave_data.append(new_waveform_data)

        # 更新标签
        self.plot_widget.update_labels(pulse_id)
        # 更新图形,
        self.plot_widget.update_curve(self.wave_data)

    def export_plot(self, save_path):
        # 创建ImageExporter对象来导出图像
        exporter = ImageExporter(self.plot_widget.plotItem)
        exporter.fileType = 'png'
        exporter.export(save_path)

