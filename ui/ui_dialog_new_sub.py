# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/chris/Documents/GitHub/Haushaltsbuch/ui/ui_dialog_new_sub.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(567, 388)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color: #313a46;")
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonAbbrechen = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButtonAbbrechen.setFont(font)
        self.pushButtonAbbrechen.setStyleSheet("QPushButton {\n"
"    background-color:  #6d6d6d;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color: #e0e1e3;\n"
"    color: white;\n"
"}")
        self.pushButtonAbbrechen.setObjectName("pushButtonAbbrechen")
        self.gridLayout_2.addWidget(self.pushButtonAbbrechen, 1, 0, 1, 1)
        self.pushButtonSpeichern = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButtonSpeichern.setFont(font)
        self.pushButtonSpeichern.setStyleSheet("QPushButton {\n"
"    background-color:  #6d6d6d;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    background-color: #e0e1e3;\n"
"    color: white;\n"
"}")
        self.pushButtonSpeichern.setObjectName("pushButtonSpeichern")
        self.gridLayout_2.addWidget(self.pushButtonSpeichern, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.lineEditSubName = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEditSubName.setFont(font)
        self.lineEditSubName.setStyleSheet("color: white;")
        self.lineEditSubName.setObjectName("lineEditSubName")
        self.gridLayout.addWidget(self.lineEditSubName, 4, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: white;")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.comboBoxSubCategorie = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.comboBoxSubCategorie.setFont(font)
        self.comboBoxSubCategorie.setStyleSheet("QComboBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QComboBox:items {\n"
"    color: white;\n"
"}\n"
"\n"
"QListView {\n"
"    color: white;\n"
"}   \n"
"\n"
"QLineEdit {\n"
"    color: white;\n"
"}")
        self.comboBoxSubCategorie.setObjectName("comboBoxSubCategorie")
        self.comboBoxSubCategorie.addItem("")
        self.comboBoxSubCategorie.setItemText(0, "")
        self.gridLayout.addWidget(self.comboBoxSubCategorie, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: white;")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 9, 0, 1, 1)
        self.dateEditSubStartDate = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.dateEditSubStartDate.setFont(font)
        self.dateEditSubStartDate.setStyleSheet("color: white;")
        self.dateEditSubStartDate.setCalendarPopup(True)
        self.dateEditSubStartDate.setObjectName("dateEditSubStartDate")
        self.gridLayout.addWidget(self.dateEditSubStartDate, 8, 2, 1, 1)
        self.comboBoxSubPeriod = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.comboBoxSubPeriod.setFont(font)
        self.comboBoxSubPeriod.setStyleSheet("QComboBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QComboBox:items {\n"
"    color: white;\n"
"}\n"
"\n"
"QListView {\n"
"    color: white;\n"
"}   \n"
"\n"
"QLineEdit {\n"
"    color: white;\n"
"}")
        self.comboBoxSubPeriod.setObjectName("comboBoxSubPeriod")
        self.comboBoxSubPeriod.addItem("")
        self.comboBoxSubPeriod.setItemText(0, "")
        self.comboBoxSubPeriod.addItem("")
        self.comboBoxSubPeriod.addItem("")
        self.gridLayout.addWidget(self.comboBoxSubPeriod, 6, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 1, 0, 1, 1)
        self.comboBoxSubDuration = QtWidgets.QComboBox(Dialog)
        self.comboBoxSubDuration.setStyleSheet("QComboBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QComboBox:items {\n"
"    color: white;\n"
"}\n"
"\n"
"QListView {\n"
"    color: white;\n"
"}   \n"
"\n"
"QLineEdit {\n"
"    color: white;\n"
"}")
        self.comboBoxSubDuration.setObjectName("comboBoxSubDuration")
        self.comboBoxSubDuration.addItem("")
        self.comboBoxSubDuration.setItemText(0, "")
        self.comboBoxSubDuration.addItem("")
        self.comboBoxSubDuration.addItem("")
        self.gridLayout.addWidget(self.comboBoxSubDuration, 10, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: white;")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 11, 0, 1, 1)
        self.lineEditSubPrice = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Cabin")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEditSubPrice.setFont(font)
        self.lineEditSubPrice.setStyleSheet("color: white;")
        self.lineEditSubPrice.setObjectName("lineEditSubPrice")
        self.gridLayout.addWidget(self.lineEditSubPrice, 11, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonAbbrechen.setText(_translate("Dialog", "Abbrechen"))
        self.pushButtonSpeichern.setText(_translate("Dialog", "Speichern"))
        self.label_4.setText(_translate("Dialog", "Abrechnung:"))
        self.label_5.setText(_translate("Dialog", "Beginn ab:"))
        self.label.setText(_translate("Dialog", "Abo anlegen"))
        self.label_6.setText(_translate("Dialog", "Laufzeit:"))
        self.label_3.setText(_translate("Dialog", "Name:"))
        self.comboBoxSubPeriod.setItemText(1, _translate("Dialog", "monatlich"))
        self.comboBoxSubPeriod.setItemText(2, _translate("Dialog", "jährlich"))
        self.label_2.setText(_translate("Dialog", "Kategorie:"))
        self.comboBoxSubDuration.setItemText(1, _translate("Dialog", "monatlich"))
        self.comboBoxSubDuration.setItemText(2, _translate("Dialog", "jährlich"))
        self.label_7.setText(_translate("Dialog", "Preis:"))