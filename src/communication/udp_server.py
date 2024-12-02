# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-02
@Description: 
    This is a brief description of what the script does.
"""

import socket

from src.communication.communication_server import CommunicationServer
from src.communication.parse_data import DATA_LENGTH, DomainEnum


class UDPCommunicationServer(CommunicationServer):
    def __init__(self, domain, server_ip, server_port, client_ip):
        super().__init__(domain)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((server_ip, server_port))
        self.target_client_ip = client_ip

    def run(self):
        while self.is_running:
            try:
                data, client_addr = self.sock.recvfrom(DATA_LENGTH)
            except OSError as e:
                self.data_error.emit(str(e), "UDP服务器接收数据失败")
                break

            if client_addr[0] == self.target_client_ip:
                self.handle_data(data)

    def stop(self):
        super().stop()
        self.sock.close()


if __name__ == "__main__":
    server = UDPCommunicationServer(DomainEnum.TIME, '127.0.0.1', 8080, '127.0.0.1')
    server.start()

    # 在这里可以添加控制逻辑，比如在某个条件满足时调用server.stop()来停止监听

    # 假设运行一段时间后停止服务
    input("按回车键停止服务器...")
    server.stop()

