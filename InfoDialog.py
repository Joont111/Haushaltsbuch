from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from ui.ui_dialog_info import Ui_Dialog

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        

        self.setWindowIcon(QIcon('ui/icon/analytics_chart.ico'))
        self.setWindowTitle("Haushaltsbuch")
        self.show()

        self.ui.closeButton.clicked.connect(self.on_click_close_dialog)

    def on_click_close_dialog(self):
        self.close()