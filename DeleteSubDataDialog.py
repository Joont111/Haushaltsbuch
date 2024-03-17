from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from qtpy import QtWidgets
from ui.ui_dialog_sub_delete_data import Ui_Dialog
from Database import Database

class DeleteSubDataDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.setWindowTitle("Haushaltsbuch - Daten löschen")
        self.show()

        self.database = Database()

        self.sub_data = self.database.get_subscription_data(date=None)

        for element in self.sub_data:
            self.ui.comboBoxSubs.addItem(element[1]) # Set name of subscription

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
            self.database.delete_subscription_data(name=self.ui.comboBoxSubs.currentText())

            self.close()

        elif return_value == QMessageBox.Cancel:
            self.close()

    def on_click_cancel(self):
        self.close()