# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-01-01
@Description: 
    This is a brief description of what the script does.
"""
import numpy as np

from src.app.plot.view.plot_widget import SAMPLE_NUM, WAVE_NUM


class ChannelModel:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.wave_data = [np.zeros(SAMPLE_NUM) for _ in range(WAVE_NUM)]

    def receive_new_waveform_data(self, new_data):
        # 移除第一个波形的数据
        self.wave_data.pop(0)
        # 插入新的波形数据
        self.wave_data.append(new_data)
