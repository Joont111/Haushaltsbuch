# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/chris/Documents/GitHub/Haushaltsbuch/ui/ui_dialog_delete_data.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 344)
        Dialog.setStyleSheet("background-color: #313a46;")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelDeleteCalday = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.labelDeleteCalday.setFont(font)
        self.labelDeleteCalday.setStyleSheet("color: #ffffff;")
        self.labelDeleteCalday.setObjectName("labelDeleteCalday")
        self.gridLayout.addWidget(self.labelDeleteCalday, 1, 0, 1, 1)
        self.dateEditDeleteCalday = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.dateEditDeleteCalday.setStyleSheet("color: #ffffff;")
        self.dateEditDeleteCalday.setCalendarPopup(True)
        self.dateEditDeleteCalday.setObjectName("dateEditDeleteCalday")
        self.gridLayout.addWidget(self.dateEditDeleteCalday, 1, 1, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setGeometry(QtCore.QRect(80, 310, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButtonCancel.setFont(font)
        self.pushButtonCancel.setStyleSheet("QPushButton {\n"
"    background-color:  #6d6d6d;\n"
"    border-radius: 5px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color: #e0e1e3;\n"
"    color: #fff;\n"
"}")
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setGeometry(QtCore.QRect(240, 310, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButtonOk.setFont(font)
        self.pushButtonOk.setStyleSheet("QPushButton {\n"
"    background-color:  #6d6d6d;\n"
"    border-radius: 5px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color: #e0e1e3;\n"
"    color: #fff;\n"
"}")
        self.pushButtonOk.setObjectName("pushButtonOk")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelDeleteCalday.setText(_translate("Dialog", "Einen Tag löschen:"))
        self.pushButtonCancel.setText(_translate("Dialog", "Abbrechen"))
        self.pushButtonOk.setText(_translate("Dialog", "Löschen"))
