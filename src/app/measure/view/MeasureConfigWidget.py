# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MeasureConfigWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeasureConfigWidget(object):
    def setupUi(self, MeasureConfigWidget):
        MeasureConfigWidget.setObjectName("MeasureConfigWidget")
        MeasureConfigWidget.resize(295, 211)
        self.gridLayout = QtWidgets.QGridLayout(MeasureConfigWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnConfirm = QtWidgets.QPushButton(MeasureConfigWidget)
        self.btnConfirm.setObjectName("btnConfirm")
        self.gridLayout.addWidget(self.btnConfirm, 2, 0, 1, 1)
        self.btnCheckAll = QtWidgets.QPushButton(MeasureConfigWidget)
        self.btnCheckAll.setObjectName("btnCheckAll")
        self.gridLayout.addWidget(self.btnCheckAll, 0, 0, 1, 1)
        self.btnUncheckAll = QtWidgets.QPushButton(MeasureConfigWidget)
        self.btnUncheckAll.setObjectName("btnUncheckAll")
        self.gridLayout.addWidget(self.btnUncheckAll, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(72, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(MeasureConfigWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 3)

        self.retranslateUi(MeasureConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(MeasureConfigWidget)

    def retranslateUi(self, MeasureConfigWidget):
        _translate = QtCore.QCoreApplication.translate
        MeasureConfigWidget.setWindowTitle(_translate("MeasureConfigWidget", "Form"))
        self.btnConfirm.setText(_translate("MeasureConfigWidget", "确定"))
        self.btnCheckAll.setText(_translate("MeasureConfigWidget", "全选"))
        self.btnUncheckAll.setText(_translate("MeasureConfigWidget", "全部取消"))
        self.groupBox.setTitle(_translate("MeasureConfigWidget", "屏幕量尺显示设置"))
