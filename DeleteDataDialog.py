from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from qtpy import QtWidgets
from ui.ui_dialog_delete_data import Ui_Dialog
from Database import Database

class DeleteDataDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.setWindowTitle("Haushaltsbuch - Daten löschen")
        self.show()

        self.ui.dateEditDeleteCalday.setDate(QDate.currentDate())

        self.ui.pushButtonOk.clicked.connect(self.on_click_delete)
        self.ui.pushButtonCancel.clicked.connect(self.on_click_cancel)

    def on_click_delete(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Daten löschen")
        msgBox.setText("Daten wirklich löschen?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return_value =  msgBox.exec()

        if return_value == QMessageBox.Ok:
            date = self.ui.dateEditDeleteCalday.text()

            self.database = Database()
            self.database.delete_data_by_calday(calday=date)

            self.close()

        elif return_value == QMessageBox.Cancel:
            self.close()

    def on_click_cancel(self):
        self.close()