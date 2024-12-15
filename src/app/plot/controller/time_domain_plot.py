# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-11-26
@Description: 
    This is a brief description of what the script does.
"""
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, Qt
from pyqtgraph import PlotWidget
from pyqtgraph.exporters import ImageExporter


class QWaveformPlot(PlotWidget):
    x_changed = pyqtSignal(float, float)
    y_changed = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self._set_x_axis()
        self._set_y_axis()
        self.curves = [self.plot(pen=(255, 0, 0), name=f'Waveform {i+1}') for i in range(5)]
        self.waveforms_data = [np.zeros(512) for _ in range(5)]
        self._set_wave_label()
        self._add_x_line()
        self._add_y_line()

    def _set_x_axis(self):
        # 设置x轴范围
        self.setXRange(0, 512 * 5)

        # 获取 X 轴对象
        ticks = [i * 512 for i in range(6)]
        x_axis = self.plotItem.getAxis('bottom')
        x_axis.setTicks([[(v, str(v)) for v in ticks]])

        # 添加无限线
        for i in range(6):
            x_pos = i * 512
            line = pg.InfiniteLine(pos=x_pos,
                                   angle=90,
                                   pen=pg.mkPen(color=(255, 255, 255), width=1, style=Qt.DashLine, dash=[2, 4]))
            self.plotItem.addItem(line)

        # 设置轴标签（PyQtGraph本身不直接支持单位，可以在标签文本中包含单位）
        self.plotItem.setLabel(axis='bottom', text='Time (ns)')

    def _set_y_axis(self):
        # 设置y轴范围
        self.setYRange(-0.6, 0.6)

        # 设置轴标签（PyQtGraph本身不直接支持单位，可以在标签文本中包含单位）
        self.plotItem.setLabel(axis='left', text='Voltage (V)')

    def _set_wave_label(self):
        self.wave_labels = [pg.TextItem(f"初始脉冲", color=(255, 255, 255)) for _ in range(5)]
        for i, label in enumerate(self.wave_labels):
            label.setVisible(False)
            label.setPos(i * 512, 0.5)
            self.plotItem.addItem(label)

    def _add_x_line(self):
        self.infinite_x1 = pg.InfiniteLine(pos=256, angle=90, pen=(255, 255, 255), movable=True)
        self.infinite_x1.xChanged.connect(self._x_line_changed)
        self.plotItem.addItem(self.infinite_x1)

        self.infinite_x2 = pg.InfiniteLine(pos=512, angle=90, pen=(255, 255, 255), movable=True)
        self.infinite_x2.xChanged.connect(self._x_line_changed)
        self.plotItem.addItem(self.infinite_x2)

    def _add_y_line(self):
        self.infinite_y1 = pg.InfiniteLine(pos=0.5, angle=0, pen=(255, 255, 255), movable=True)
        self.infinite_y1.yChanged.connect(self._y_line_changed)
        self.plotItem.addItem(self.infinite_y1)

        self.infinite_y2 = pg.InfiniteLine(pos=-0.5, angle=0, pen=(255, 255, 255), movable=True)
        self.infinite_y2.yChanged.connect(self._y_line_changed)
        self.plotItem.addItem(self.infinite_y2)

    def _x_line_changed(self):
        self.x_changed.emit(self.infinite_x1.x(), self.infinite_x2.x())

    def _y_line_changed(self):
        self.y_changed.emit(self.infinite_y1.y(), self.infinite_y2.y())

    def set_line_visible(self, is_visible):
        self.infinite_x1.setVisible(is_visible)
        self.infinite_x2.setVisible(is_visible)
        self.infinite_y1.setVisible(is_visible)
        self.infinite_y2.setVisible(is_visible)

    def update_plot(self, pulse_id, new_waveform_data):
        # 移除第一个波形的数据
        self.waveforms_data.pop(0)
        # 插入新的波形数据
        # self.waveforms_data.insert(0, new_waveform_data)
        self.waveforms_data.append(new_waveform_data)

        # 更新标签
        self._update_labels(pulse_id)

        # 更新图形,
        for i, curve in enumerate(self.curves):
            start = 512 * i
            x = np.arange(start, start + len(self.waveforms_data[i]), 1)
            curve.setData(x=x, y=self.waveforms_data[i])

            self.wave_labels[i].setVisible(True)

    def _update_labels(self, pulse_id):
        for i in range(4):
            self.wave_labels[i].setText(self.wave_labels[i + 1].toPlainText())
        self.wave_labels[4].setText(f"脉冲{pulse_id}")

    def clear_plot(self):
        for curve in self.curves:
            curve.clear()
        # 标签移出视野范围
        for label in self.wave_labels:
            label.setVisible(False)
        self.plotItem.getViewBox().update()

    def export_plot(self, save_path):
        # 创建ImageExporter对象来导出图像
        exporter = ImageExporter(self.plotItem)
        exporter.fileType = 'png'
        file_path = save_path
        exporter.export(file_path)
