# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-02
@Description: 
    This is a brief description of what the script does.
"""

import socket
import threading

from src.communication.data_handler import DataHandler


class UDPServer:
    def __init__(self, server_ip, server_port, client_ips):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((server_ip, server_port))
        self.data_handlers = []
        for ip in client_ips:
            self.data_handlers.append(DataHandler(ip))

    def connect_callback(self, data_success_callback, data_error_callback):
        for data_handler in self.data_handlers:
            data_handler.data_succeeded.connect(data_success_callback)
            data_handler.data_erred.connect(data_error_callback)

    def run(self):
        for data_handler in self.data_handlers:
            threading.Thread(target=data_handler.run, args=(self.sock,)).start()

    def stop(self):
        for data_handler in self.data_handlers:
            data_handler.stop()
        self.sock.close()

