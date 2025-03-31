# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-04
@Description: 
    This is a brief description of what the script does.
"""
import binascii
import socket

from PyQt5.QtCore import QObject, pyqtSignal

from src.service.communication.parse_data import check_frame, parse_time_domain_data
from src.service.log.my_logger import get_logger


class DataHandler(QObject):
    data_succeeded = pyqtSignal(int, int, list, str)  # channel_id, pulse_data_encoding, sample_points, hex_data
    data_erred = pyqtSignal(str, str)  # error msg, hex_data

    def __init__(self, target_client_ip, port):
        super().__init__()
        self.is_running = True
        self.target_client_ip = target_client_ip
        self.target_port = port
        self.frame_buffer = bytearray()  # 缓冲区用于构建完整的帧

    def run(self, sock: socket.socket):
        while self.is_running:
            try:
                data, addr = sock.recvfrom(2048)        # 数据帧有512个点，单个点2字节，加上帧头帧尾，大于1024
                get_logger().debug(f"Received data: {data}")
            except socket.timeout as e:
                get_logger().error(f"UDP连接超时: {self.target_client_ip}, {e}")
                continue
            except OSError as e:
                get_logger().error(f"UDP服务器接收数据失败: {self.target_client_ip}, {e}")
                self.data_erred.emit(f"UDP服务器接收数据失败: {self.target_client_ip}", str(e))
                self.is_running = False
                continue
            if addr == (self.target_client_ip, int(self.target_port)):
                self.handle_data(data)

    def handle_data(self, data):
        """
        持续接收UDP发来的数据
        :param data:
        :return:
        """
        self.frame_buffer.extend(data)
        # print("Received data:", binascii.hexlify(data))

        while self.is_running:
            # 从上次找到的帧头位置或起始位置开始查找下一个帧头
            frame_start = self.frame_buffer.find(b'\xDF\xFD')
            frame_end = self.frame_buffer.find(b'\xDE\xAF')
            # 数据中有帧头+帧尾
            if frame_start != -1 and frame_end != -1:
                if frame_start < frame_end:
                    # 发现新的完整帧,丢弃旧帧头
                    frame_data = self.frame_buffer[frame_start:frame_end + 2]
                    self.process_valid_frame(frame_data)
                else:
                    # 连续正常两帧，即帧尾、帧头（此时的帧头是下一帧的开始）
                    frame_data = self.frame_buffer[:frame_end + 2]
                    self.process_valid_frame(frame_data)
                self.frame_buffer = self.frame_buffer[frame_end + 2:]
            # Nothing
            elif frame_start == -1 and frame_end == -1:
                break
            # 只有帧尾，是完整的帧
            elif frame_start == -1 and frame_end != -1:
                frame_data = self.frame_buffer[:frame_end + 2]
                self.process_valid_frame(frame_data)
                self.frame_buffer = self.frame_buffer[frame_end + 2:]
            # 只有帧头，丢弃旧帧头
            else:
                self.frame_buffer = self.frame_buffer[frame_start:]
                break

    def process_valid_frame(self, data):
        hex_data = binascii.hexlify(data).decode('utf-8')
        hex_data = ' '.join([hex_data[i:i + 2] for i in range(0, len(hex_data), 2)])

        try:
            channel_id, pulse_data_encoding, valid_data = check_frame(data)
            sample_points = parse_time_domain_data(valid_data)
            get_logger().info(f"接收到数据: 通道{channel_id}, 脉冲{pulse_data_encoding}, data: \n{hex_data}")
        except ValueError as e:
            self.data_erred.emit(str(e), hex_data)
        else:
            self.data_succeeded.emit(channel_id, pulse_data_encoding, sample_points, hex_data)

    def stop(self):
        self.is_running = False
