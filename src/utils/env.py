# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-05-21
@Description: 
    This is a brief description of what the script does.
"""
import os
import sys

TESTING = False


def is_code_env():
    return TESTING


def check_env():
    global TESTING
    # 当前启动的路径file是否为.py结尾，是则为测试环境，.exe则为正式环境
    TESTING = os.path.splitext(sys.argv[0])[1] == '.py'


if __name__ == '__main__':
    check_env()
    print(is_code_env())
