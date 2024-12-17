# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2024-12-16
@Description: 
    This is a brief description of what the script does.
"""
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox

from src.app.udp_config.view.UdpConfig import Ui_UdpConfig


class QUdpConfigWidget(QWidget):
    confirmed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_UdpConfig()
        self.ui.setupUi(self)

        self.is_open = False
        self._init_ui()

    def _init_ui(self):
        self.ui.lineEditServerIP.setText("192.168.0.71")
        self.ui.lineEditServerPort.setText("10010")

        self.ui.lineEditClientIP1.setText("192.168.0.98")
        self.ui.lineEditClientPort1.setText("10018")

        self.ui.lineEditClientIP2.setText("192.168.0.99")
        self.ui.lineEditClientPort1.setText("10019")

        self.ui.lineEditClientIP3.setText("192.168.0.100")
        self.ui.lineEditClientPort1.setText("10020")

        # 本地测试
        self.ui.lineEditServerIP.setText("127.0.0.1")
        self.ui.lineEditServerPort.setText("8080")

        self.ui.lineEditClientIP1.setText("127.0.0.1")
        self.ui.lineEditClientPort1.setText("8081")

        self.ui.lineEditClientIP2.setText("127.0.0.1")
        self.ui.lineEditClientPort1.setText("8082")

        self.ui.lineEditClientIP3.setText("127.0.0.1")
        self.ui.lineEditClientPort1.setText("8083")

    @pyqtSlot()
    def on_btnOpen_clicked(self):
        # 当前未开启，说明点击开启，要检查输入
        if not self.is_open:
            try:
                port1 = int(self.ui.lineEditClientPort1.text())
                port2 = int(self.ui.lineEditClientPort2.text())
                port3 = int(self.ui.lineEditClientPort3.text())
            except ValueError:
                QMessageBox.warning(self, "错误", "端口必须是整数")
                return
            clients = {(self.ui.lineEditClientIP1.text(), port1),
                       (self.ui.lineEditClientIP2.text(), port2),
                       (self.ui.lineEditClientIP3.text(), port3)}
            if len(clients) != 3:
                QMessageBox.warning(self, "错误", "请输入3个不重复的客户端IP地址")
                return
        self.confirmed.emit()

    def get_udp_config(self):
        return (self.ui.lineEditServerIP.text(),
                self.ui.lineEditServerPort.text(),
                [(self.ui.lineEditClientIP1.text(), int(self.ui.lineEditClientPort1.text())),
                 (self.ui.lineEditClientIP2.text(), int(self.ui.lineEditClientPort2.text())),
                 (self.ui.lineEditClientIP3.text(), int(self.ui.lineEditClientPort3.text()))])

    def set_open(self):
        self.ui.btnOpen.setIcon(QIcon(":/png/images/open.png"))
        self.is_open = True

    def set_closed(self):
        self.ui.btnOpen.setIcon(QIcon(":/png/images/close.png"))
        self.is_open = False


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QUdpConfigWidget()
    window.show()
    window.set_closed()
    sys.exit(app.exec())
