# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-17
@Description: 
    This is a brief description of what the script does.
"""
import threading

from src.service.communication.udp_server import UDPServer


def my_test_udp_server():
    client_ips = [('127.0.0.1', 8081),
                  ('127.0.0.1', 8082),
                  ('127.0.0.1', 8083)]
    server = UDPServer('127.0.0.1',
                       8080,
                       client_ips)
    server.connect_callback(print, print)
    thread = threading.Thread(target=server.run)
    thread.start()
    thread.join()


if __name__ == '__main__':
    my_test_udp_server()
