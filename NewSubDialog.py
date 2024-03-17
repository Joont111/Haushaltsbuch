from PyQt5.QtGui import QIcon
from qtpy import QtWidgets
from PyQt5 import QtCore
from ui.ui_dialog_new_sub import Ui_Dialog
from Database import Database
from PyQt5.QtWidgets import QMessageBox

from datetime import date


class NewSubDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        self.selected_kategroie = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.database = Database()

        all_categories = self.database.get_all_categories()
        self.current_date = QtCore.QDate.fromString(date.today().strftime('%m.%Y'), 'MM.yyyy')
        self.ui.dateEditSubStartDate.setDate(self.current_date)

        for element in all_categories:
            self.ui.comboBoxSubCategorie.addItem(element[0])

        self.setWindowTitle("Haushaltsbuch - Neues Abo")
        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.show()

        self.ui.pushButtonAbbrechen.clicked.connect(self.on_click_close_dialog)
        self.ui.pushButtonSpeichern.clicked.connect(self.on_click_save_dialog)


    def on_click_save_dialog(self):
        self.sub_categroie = self.ui.comboBoxSubCategorie.currentText()
        self.sub_name = self.ui.lineEditSubName.text()
        self.sub_period = self.ui.comboBoxSubPeriod.currentText()
        self.sub_start_date = self.ui.dateEditSubStartDate.text()
        self.sub_duration = self.ui.comboBoxSubDuration.currentText()
        self.sub_price = round(float(self.ui.lineEditSubPrice.text().replace(',', '.')), 2)

        self.calday = self.current_date.toPyDate().strftime("%Y-%m-01")

        self.database.save_subscription_data(sub_calday=self.calday, sub_cat=self.sub_categroie, sub_name=self.sub_name, sub_period=self.sub_period, sub_start_date=self.sub_start_date, sub_duration=self.sub_duration, sub_price=self.sub_price)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Neues Abo")
        msgBox.setText("Daten wurden gespeichert!")
        msgBox.exec()
        
        self.close()

    def on_click_close_dialog(self):
        self.close()
