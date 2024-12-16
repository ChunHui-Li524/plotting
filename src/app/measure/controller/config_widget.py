# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-16
@Description: 
    This is a brief description of what the script does.
"""
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox

from src.app.measure.view.MeasureConfigWidget import Ui_MeasureConfigWidget


class QMeasureConfigWidget(QWidget):
    config_confirmed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MeasureConfigWidget()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.Window)

        self._checkboxes = []
        self._init_ui()

    def _init_ui(self):
        for i in range(1, 10):
            checkbox = QCheckBox(self.ui.groupBox)
            checkbox.setText(f"屏幕{i}")
            checkbox.setChecked(True)
            self.ui.groupBox.layout().addWidget(checkbox)

            self._checkboxes.append(checkbox)

    @pyqtSlot()
    def on_btnCheckAll_clicked(self):
        for checkbox in self._checkboxes:
            checkbox.setChecked(True)

    @pyqtSlot()
    def on_btnUncheckAll_clicked(self):
        for checkbox in self._checkboxes:
            checkbox.setChecked(False)

    @pyqtSlot()
    def on_btnConfirm_clicked(self):
        result = []
        for checkbox in self._checkboxes:
            if checkbox.isChecked():
                result.append(int(checkbox.text().removeprefix('屏幕')))
        self.config_confirmed.emit(result)
        self.close()
