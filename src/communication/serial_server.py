import serial

from communication.parse_data import DATA_LENGTH
from communication.communication_server import CommunicationServer


class SerialCommunicationServer(CommunicationServer):

    def __init__(self, domain, port_name, baudrate=115200):
        super().__init__(domain)
        self.serial_port = serial.Serial(port_name, baudrate)

    def run(self):
        while self.is_running:
            try:
                data = self.serial_port.read(DATA_LENGTH)  # 读取固定长度的数据包
            except serial.SerialException:
                break

            self.handle_data(data)

    def stop(self):
        super().stop()
        self.serial_port.close()
