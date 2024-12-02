import binascii

from PyQt5.QtCore import QThread, pyqtSignal

from src.communication.parse_data import parse_time_domain_data, DomainEnum, parse_frequency_domain_data, check_frame


class CommunicationServer(QThread):
    data_received = pyqtSignal(int, int, list, str)  # channel_id, pulse_data_encoding, sample_points
    data_error = pyqtSignal(str, str)  # error msg, data

    def __init__(self, domain: DomainEnum):
        super().__init__()
        self.is_running = True

        self.parse_func = {
            DomainEnum.TIME: parse_time_domain_data,
            DomainEnum.FREQUENCY: parse_frequency_domain_data
        }.get(domain)

        self.frame_buffer = bytearray()  # ���������ڹ���������֡

    def run(self):
        raise NotImplementedError("run() method must be implemented in subclass")

    def handle_data(self, data):
        self.frame_buffer.extend(data)
        # print("Received data:", binascii.hexlify(data))

        while self.is_running:
            # ���ϴ��ҵ���֡ͷλ�û���ʼλ�ÿ�ʼ������һ��֡ͷ
            frame_start = self.frame_buffer.find(b'\xDF\xFD')
            frame_end = self.frame_buffer.find(b'\xDE\xAF')
            # ֡ͷ+֡β
            if frame_start != -1 and frame_end != -1:
                if frame_start < frame_end:
                    # �����µ�֡ͷ,������֡ͷ
                    frame_data = self.frame_buffer[frame_start:frame_end + 2]
                    self.process_valid_frame(frame_data)
                else:
                    # ����������֡
                    frame_data = self.frame_buffer[:frame_end + 2]
                    self.process_valid_frame(frame_data)
                self.frame_buffer = self.frame_buffer[frame_end + 2:]
            # Nothing
            elif frame_start == -1 and frame_end == -1:
                break
            # ֡β
            elif frame_start == -1 and frame_end != -1:
                frame_data = self.frame_buffer[:frame_end + 2]
                self.process_valid_frame(frame_data)
                self.frame_buffer = self.frame_buffer[frame_end + 2:]
            # ֡ͷ
            else:
                self.frame_buffer = self.frame_buffer[frame_start:]
                break

    def process_valid_frame(self, data):
        hex_data = binascii.hexlify(data).decode('utf-8')
        hex_data = ' '.join([hex_data[i:i + 2] for i in range(0, len(hex_data), 2)])

        try:
            channel_id, pulse_data_encoding, valid_data = check_frame(data)
            sample_points = parse_time_domain_data(valid_data)
        except ValueError as e:
            self.data_error.emit(str(e), hex_data)
        else:
            self.data_received.emit(channel_id, pulse_data_encoding, sample_points, hex_data)

    def stop(self):
        self.is_running = False
        self.quit()
