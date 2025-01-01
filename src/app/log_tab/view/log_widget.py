# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-01-01
@Description: 
    This is a brief description of what the script does.
"""
from datetime import datetime

from PyQt5.QtGui import QColor, QFont, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QPlainTextEdit


class QLogWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置背景颜色为黑色
        self.setStyleSheet("background-color: black;")
        # 设置字体为微软雅黑
        font = QFont("Microsoft YaHei")
        self.setFont(font)

    def append_success_text(self, text):
        # 设置文字颜色为白色
        self._set_text_color(QColor("white"))
        processed_text = self._process_log(text)
        self.appendPlainText(processed_text)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def append_error_text(self, text):
        # 设置文字颜色为黑色
        self._set_text_color(QColor("red"))
        processed_text = self._process_log(text)
        self.appendPlainText(processed_text)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def _set_text_color(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self.setCurrentCharFormat(fmt)

    def _process_log(self, text):
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp}:  {text}\n"
