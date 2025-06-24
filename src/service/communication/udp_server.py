# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-02
@Description: 
    This is a brief description of what the script does.
"""

import socket
import threading
import queue

from src.service.communication.data_handler import DataHandler
from src.service.log.my_logger import get_logger


class UDPServer:
    def __init__(self, server_ip, server_port, client_ips):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((server_ip, server_port))
        # 增加超时时间，避免因为超时导致数据丢失
        self.sock.settimeout(10)
        self.client_addresses = client_ips

        self.is_running = False
        self.data_queue = queue.Queue()  # 新增队列用于接收数据
        self.data_handler = DataHandler()  # 单例 DataHandler
        self.threads = []

    def connect_callback(self, data_success_callback, data_error_callback):
        self.data_handler.data_succeeded.connect(data_success_callback)
        self.data_handler.data_erred.connect(data_error_callback)

    def run(self):
        self.is_running = True

        # 启动数据接收线程
        receive_thread = threading.Thread(target=self.receive_data)
        self.threads.append(receive_thread)
        receive_thread.start()

        # 启动数据处理线程
        process_thread = threading.Thread(target=self.process_data)
        self.threads.append(process_thread)
        process_thread.start()

    def receive_data(self):
        while self.is_running:
            try:
                data, addr = self.sock.recvfrom(2048)  # 接收数据
                if addr in self.client_addresses:
                    self.data_queue.put((data, addr))  # 将数据放入队列
                    get_logger().info(f"Received data from {addr}")
                else:
                    get_logger().error(f"Received data from unauthorized IP: {addr}")
            except socket.timeout:
                continue
            except ConnectionResetError as e:
                # 忽略由ICMP Port Unreachable引起的ConnectionResetError
                get_logger().warning("Connection reset ignored (possibly ICMP 'Port Unreachable')")
                continue
            except OSError as e:
                get_logger().error(f"UDP服务器接收数据失败: {e}")
                self.stop()
                continue

    def process_data(self):
        while self.is_running:
            try:
                data, addr = self.data_queue.get(timeout=1)  # 设置超时时间为1秒
                self.data_handler.handle_data(data)  # 使用 DataHandler 处理数据
            except queue.Empty:
                continue  # 如果队列为空，继续循环

    def send_clear_cmd(self):
        cmd = "dffd01010000000055aa"
        for addr in self.client_addresses:
            self.send_data(addr, cmd)

    def send_data(self, address, data):
        """
        向指定的客户端发送16进制命令
        :param address: 目标客户端的地址 (ip, port)
        :param data: 要发送的数据
        """
        hex_data = bytes.fromhex(data.replace(" ", "").lower())
        try:
            self.sock.sendto(hex_data, address)
            get_logger().info(f"Sent data to {address}: {data}")
        except Exception as e:
            get_logger().error(f"Failed to send data to {address}: {e}")

    def stop(self):
        self.is_running = False
        for thread in self.threads:
            thread.join()
        self.sock.close()
