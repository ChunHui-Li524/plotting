# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddWidget(object):
    def setupUi(self, AddWidget):
        AddWidget.setObjectName("AddWidget")
        AddWidget.resize(152, 239)
        AddWidget.setStyleSheet("image: url(:/png/images/加号.png);")

        self.retranslateUi(AddWidget)
        QtCore.QMetaObject.connectSlotsByName(AddWidget)

    def retranslateUi(self, AddWidget):
        _translate = QtCore.QCoreApplication.translate
        AddWidget.setWindowTitle(_translate("AddWidget", "Form"))
import image_rc
