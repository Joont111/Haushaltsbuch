from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from qtpy import QtWidgets
from ui.ui_dialog_new_data import Ui_Dialog
from Database import Database

class NewDataDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        self.selected_filepath = None
        self.selected_kategroie = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.database = Database()

        all_categories = self.database.get_all_categories()

        for element in all_categories:
            self.ui.comboBoxKategorie.addItem(element[0])

        self.setWindowTitle("Haushaltsbuch - Neue Daten")
        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.show()

        self.ui.toolButtonFileDialog.clicked.connect(self.open_file_dialog)

        self.ui.pushButtonAbbrechen.clicked.connect(self.on_click_close_dialog)
        self.ui.pushButtonSpeichern.clicked.connect(self.on_click_save_dialog)

    def open_file_dialog(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.ExistingFile)
        self.ui.lineEditSelectedFile.setText(file.getOpenFileName()[0])

    def on_click_save_dialog(self):
        self.selected_filepath = self.ui.lineEditSelectedFile.text()
        self.selected_kategroie = self.ui.comboBoxKategorie.currentText()

        self.close()

    def get_selected_filepath(self):
        return self.selected_filepath

    def on_click_close_dialog(self):
        self.close()
