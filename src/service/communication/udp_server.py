# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-02
@Description: 
    This is a brief description of what the script does.
"""

import socket
import threading

from src.service.communication.data_handler import DataHandler


class UDPServer:
    def __init__(self, server_ip, server_port, client_ips):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((server_ip, server_port))
        self.sock.settimeout(3)
        self.data_handlers = []
        self.threads = []
        for ip, port in client_ips:
            self.data_handlers.append(DataHandler(ip, port))

    def connect_callback(self, data_success_callback, data_error_callback):
        for data_handler in self.data_handlers:
            data_handler.data_succeeded.connect(data_success_callback)
            data_handler.data_erred.connect(data_error_callback)

    def run(self):
        for data_handler in self.data_handlers:
            thread = threading.Thread(target=data_handler.run, args=(self.sock,))
            self.threads.append(thread)
            thread.start()

    def stop(self):
        for data_handler in self.data_handlers:
            data_handler.stop()
        for thread in self.threads:
            thread.join()
        self.sock.close()
