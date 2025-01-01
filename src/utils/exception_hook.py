# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-01-01
@Description: 
    This is a brief description of what the script does.
"""
from traceback import extract_tb, format_list

from src.service.log.my_logger import get_logger


def custom_exception_hook(type_, value, traceback):
    # 记录异常堆栈信息到日志中
    error_stack = ''.join(format_list(extract_tb(traceback)))
    get_logger().error(f"Exception occurred:\n"
                       f"{type_.__name__}: {value}\n"
                       f"Stack trace:\n"
                       f"{error_stack}")
