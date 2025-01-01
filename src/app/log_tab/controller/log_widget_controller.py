# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-01-01
@Description: 
    This is a brief description of what the script does.
"""
from src.app.log_tab.view.log_widget import QLogWidget


class LogTabController:
    def __init__(self, log_widget: QLogWidget):
        self.log_widget = log_widget

    def append_error_text(self, text):
        self.log_widget.append_error_text(text)

    def append_success_text(self, text):
        self.log_widget.append_success_text(text)
