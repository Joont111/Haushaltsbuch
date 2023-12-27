from PyQt5.QtGui import QIcon
from qtpy import QtWidgets
from ui.ui_dialog_new_categorie import Ui_Dialog
from Database import Database
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class NewCategorieDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = parent

        self.selected_filepath = None
        self.selected_kategroie = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.setWindowTitle("Haushaltsbuch - Neue Kategorie")
        self.show()

        self.ui.pushButtonSpeichern.clicked.connect(self.on_click_save_dialog)
        self.ui.pushButtonAbbrechen.clicked.connect(self.on_click_close_dialog)

        self.database = Database()

    def on_click_save_dialog(self):
        new_cat = self.ui.lineEditNewCategorie.text()

        if new_cat != '':
            self.database.save_new_categorie(categorie=new_cat)

        self.close()

    def on_click_close_dialog(self):
        self.close()