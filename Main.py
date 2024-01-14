import csv
import sys
import re
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog, QLabel
from PyQt5 import QtGui
from PyQt5 import QtCore
from Chart import Chart

from ui.ui_mainwindow import Ui_MainWindow
from NewCategorieDialog import NewCategorieDialog
from NewDataDialog import NewDataDialog
from DeleteDataDialog import DeleteDataDialog
from InfoDialog import InfoDialog
from Database import Database

from datetime import date
import calendar
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Init GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set Window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setWindowIcon(QtGui.QIcon('ui/icon/analytics_chart.ico'))
        self.setWindowTitle('Haushaltsbuch')
        self.showMaximized()

        self.ui.full_menu_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_button_1.setChecked(True)

        # Set content to combo box
        # self.generate_stichtag()
        current_date = QtCore.QDate.fromString(date.today().strftime('%m.%Y'), 'MM.yyyy')
        self.ui.date_edit_stichtag.setDate(current_date)
        self.current_stichtag = self.ui.date_edit_stichtag.date().toPyDate().strftime("%Y-%m-%d")

        self.database = Database()

        # Connect Buttonns to functions
        self.ui.home_button_1.toggled.connect(self.on_home_button_1_toggled)
        self.ui.home_button_2.toggled.connect(self.on_home_button_2_toggled)

        self.ui.dashboard_button_1.toggled.connect(self.on_dashboard_button_1_toggled)
        self.ui.dashboard_button_2.toggled.connect(self.on_dashboard_button_2_toggled)

        self.ui.table_button_1.toggled.connect(self.on_table_button_1_toggled)
        self.ui.table_button_2.toggled.connect(self.on_table_button_2_toggled)

        self.ui.account_balance_button_1.toggled.connect(self.on_account_balance_1_toggled)
        self.ui.account_balance_button_2.toggled.connect(self.on_account_balance_2_toggled)

        self.ui.add_categorie_button.clicked.connect(self.add_new_categorie)
        self.ui.add_fixed_costs_button.clicked.connect(self.on_click_load_fixed_costs)
        self.ui.add_data_button.clicked.connect(self.on_click_new_data)
        self.ui.delete_data_button.clicked.connect(self.on_click_delete_data)
        self.ui.export_data_button.clicked.connect(self.on_click_export)
        
        self.ui.info_button_1.clicked.connect(self.on_click_show_info_dialog)
        self.ui.info_button_2.clicked.connect(self.on_click_show_info_dialog)

        self.ui.exit_button_1.clicked.connect(self.close)
        self.ui.exit_button_2.clicked.connect(self.close)

        #self.ui.combo_box_stichtag.currentTextChanged.connect(self.get_stichtag)
        self.ui.date_edit_stichtag.dateChanged.connect(self.get_stichtag)

        # **********************************************************************
        # Stacked Page: Dashboard Widgets
        # **********************************************************************

        # Create main layout on dashboard page
        self.dashboard_page_vbox_layout = QVBoxLayout()

        # Create Bar Chart
        self.chart = Chart()
        self.list_einnahmen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.list_ausgaben = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.list_gespartes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.bar_chart_hbox_layout = QHBoxLayout()
        self.bar_chart_hbox_layout.addWidget(self.chart.func_percentage_bar(listEinnahmen=self.list_einnahmen, listAusgaben=self.list_ausgaben, listGespartes=self.list_gespartes))
        self.dashboard_page_vbox_layout.addItem(self.bar_chart_hbox_layout)

        # Create Pie Chart Top 5 Ausgaben
        self.chart_pie = Chart()
        self.pie_data = self.database.get_top_5_ausgaben(date=self.current_stichtag)
        self.pie_label = 'Top 5 Ausgaben'
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.chart_pie.func_pie_chart(self.pie_data, pieLabel=self.pie_label))
                
        # Create Bar Chart Gespartes
        self.bar_chart = Chart()
        self.hbox_layout.addWidget(self.bar_chart.func_bar_chart(data=[0], barChartLabel='Gespartes'))
        self.dashboard_page_vbox_layout.addItem(self.hbox_layout)

        # Add main layout to page widget
        self.ui.page_dashboard.setLayout(self.dashboard_page_vbox_layout)
        # **********************************************************************
        # Stacked Page: Dashboards End
        # **********************************************************************

        # **********************************************************************
        # Stacked Page: Table Widgets
        # **********************************************************************
        self.table_page_hbox_layout = QHBoxLayout()

        # Create TableWidget -> table page
        self.table_widget = QTableWidget()
  
        #Column count 
        self.table_widget.setColumnCount(4)   
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem('Datum'))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem('Einnahmen'))
        self.table_widget.setHorizontalHeaderItem(2, QTableWidgetItem('Ausgaben'))
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem('Kategorie'))
   
        #Table will fit the screen horizontally 
        self.table_widget.horizontalHeader().setStretchLastSection(True) 
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.table_page_hbox_layout.addWidget(self.table_widget)

        # Secon Table: Overview categories
        self.table_widget_overview_cat = QTableWidget()

        self.table_widget_overview_cat.setColumnCount(2)
        self.table_widget_overview_cat.setHorizontalHeaderItem(0, QTableWidgetItem('Kategorie'))
        self.table_widget_overview_cat.setHorizontalHeaderItem(1, QTableWidgetItem('Summe'))

        self.table_widget_overview_cat.horizontalHeader().setStretchLastSection(True)
        self.table_widget_overview_cat.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_page_hbox_layout.addWidget(self.table_widget_overview_cat)

        self.ui.page_tables.setLayout(self.table_page_hbox_layout)
        # **********************************************************************
        # Stacked Page: Table Widgets End
        # **********************************************************************

        # Init Data and fill charts and Tables
        self.get_stichtag()

        # Set Delta Account Balance
        self.set_delta_sum_account_balance()


    # Button Functions (Change StackedWidget Pages)
    def on_home_button_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_home_button_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashboard_button_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_dashboard_button_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_table_button_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def on_table_button_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_account_balance_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_account_balance_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    # Call Dialog show Infos
    def on_click_show_info_dialog(self):
        self.info_dialog = InfoDialog()

    # Call Dialog delete Data
    def on_click_delete_data(self):
        self.dialog_delete = DeleteDataDialog()

        if self.dialog_delete.exec() == 0:
            self.get_stichtag()

    def on_click_load_fixed_costs(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.ExistingFile)
        file = file.getOpenFileName()[0]

        if file != '':
            self.read_data_file(file)

    def get_selected_categorie(self, cat):
        self.new_data_categorie = cat

    def get_selected_file_path(self, path):
        file_data = self.read_data_file(filepath=path, returning=True)

        self.database.insert_artikel(file_data)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Neue Daten")
        msgBox.setText("Daten wurden gespeichert!")
        msgBox.exec()

        converted_data = []
        total_ausgaben = 0.00

        #Convert fileData to TableWidgetData
        for line in file_data:
            total_ausgaben = total_ausgaben + float(line[2])

        converted_data.append([file_data[0][0], '0.00', round(total_ausgaben, 2), self.new_data_categorie])

        self.set_table_data(tableData=converted_data, noSave=False)

    # Add New Data
    def on_click_new_data(self):
        self.dialog = NewDataDialog()
        self.dialog.ui.lineEditSelectedFile.textChanged.connect(self.get_selected_file_path)
        self.dialog.ui.comboBoxKategorie.currentTextChanged.connect(self.get_selected_categorie)

    # **********************************************************************
    # Application Functions
    # **********************************************************************

    # Update Charts and Table data by new date
    def get_stichtag(self):
        self.current_stichtag = self.ui.date_edit_stichtag.date().toPyDate().strftime("%Y-%m-%d")

        self.table_widget.clear()
        self.table_widget.setRowCount(0)

        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem('Datum'))
        self.table_widget.setHorizontalHeaderItem(1, QTableWidgetItem('Einnahmen'))
        self.table_widget.setHorizontalHeaderItem(2, QTableWidgetItem('Ausgaben'))
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem('Kategorie'))

        self.ui.label_einnahmen_number.setText('0')
        self.ui.label_ausgaben_number.setText('0')

        # Datenbank mit den neuem Stichtag abfragen
        self.set_table_data(self.database.get_table_widget_data(self.current_stichtag), noSave=True)

        # Tab 2 Tabelle refreshen
        self.update_table_ausgaben_in_zahlen()

    # Add new Data to Table Widget
    def set_table_data(self, tableData=None, noSave=True):

        if len(tableData) > 0:
            for date, value_1, value_2, kategorie in tableData:
                row = self.table_widget.rowCount()
                self.table_widget.insertRow(row)
                self.table_widget.setItem(row, 0, QTableWidgetItem(date))
                self.table_widget.setItem(row, 1, QTableWidgetItem(str(value_1) + ' €'))
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(value_2) + ' €'))
                self.table_widget.setItem(row, 3, QTableWidgetItem(kategorie))

                total_einnahmen = float(self.ui.label_einnahmen_number.text().replace(' €', '')) + float(value_1)
                self.ui.label_einnahmen_number.setText(str(round(total_einnahmen, 2)) + ' €')

                # Exclude cat 'Sparen'
                if kategorie != 'Sparen':
                    total_ausgaben = float(self.ui.label_ausgaben_number.text().replace(' €', '')) + float(value_2)
                    self.ui.label_ausgaben_number.setText(str(round(total_ausgaben, 2)) + ' €')

            if noSave == False:
                self.save_table_data()

            # Update Chart Data
            self.percantage_chart_data_changed()
            self.pie_chart_data_changed()
            self.bar_chart_data_changed()

            self.update_table_ausgaben_in_zahlen()
            self.set_delta_sum_account_balance()

    # Save TableWigdet Data (Left Table) -> Obsolete?
    def save_table_data(self):
        self.database.delete_table_widget_data(self.current_stichtag)

        list_new_data = []
        for i in range(0, self.table_widget.rowCount()):
            if self.table_widget.item(i, 1).text() == '':
                einnahmen = 0.00
            else:
                einnahmen = self.table_widget.item(i, 1).text().replace('€', '')

            if self.table_widget.item(i, 2).text() == '':
                ausgaben = 0.00
            else:
                ausgaben = self.table_widget.item(i, 2).text().replace(' €', '')

            list_new_data.append([self.table_widget.item(i, 0).text(), einnahmen, ausgaben, self.table_widget.item(i, 3).text()])

        self.database.save_table_widget_data(list_new_data)

    # Read CSV File with Data and save them into the database
    def read_data_file(self, filepath=None, returning=False):
        with open(filepath, 'r', encoding='utf-8') as file:
            file_data = list(csv.reader(file, dialect='excel', delimiter=';', quotechar='"'))

        file_data.pop(0)

        converted_list = []

        # Die Value felder sind entweder einnahmen und ausgaben, oder Artikelbeschreibung und Preis
        for date, value_1, value_2, kategorie in file_data:
            if value_1 == '':
                value_1 = '0,00'

            if value_2 == '':
                value_2 = '0,00'

            converted_list.append([date, value_1.replace(',', '.'), value_2.replace(',', '.'), kategorie])

        if returning:
            return converted_list
        else:
            self.set_table_data(converted_list, noSave=False)

    # Refresh Table Group By Cat
    def update_table_ausgaben_in_zahlen(self):
        # Tab 2 Tabelle refreshen
        self.table_widget_overview_cat.clear()
        self.table_widget_overview_cat.setRowCount(0)

        self.table_widget_overview_cat.setHorizontalHeaderItem(0, QTableWidgetItem('Kategorie'))
        self.table_widget_overview_cat.setHorizontalHeaderItem(1, QTableWidgetItem('Summe'))

        self.set_table_data_ausgaben_in_zahlen(self.database.get_ausgaben_in_zahlen(self.current_stichtag))

    # Set Data for Second Table View
    def set_table_data_ausgaben_in_zahlen(self, tableData=None):
        for kategorie, summe in tableData:
            row = self.table_widget_overview_cat.rowCount()
            self.table_widget_overview_cat.insertRow(row)
            self.table_widget_overview_cat.setItem(row, 0, QTableWidgetItem(kategorie))
            self.table_widget_overview_cat.setItem(row, 1, QTableWidgetItem(str(summe) + ' €'))

    # Update Percentage Chart
    def percantage_chart_data_changed(self):
        month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        year = int(self.current_stichtag[:4])

        if year == '':
            year = date.today().year

        for i in range(0, 12):
            last_days = calendar.monthrange(year, int(month[i]))
            last_days = str(year) + '-' + str(month[i]) + '-' + str(last_days[1])

            table_data = self.database.get_table_widget_data(caldate=last_days)

            gesamt_einnahmen = 0.00
            gesamt_ausgaben = 0.00
            gesamt_sparen = 0.00

            for datum, einnahmen, ausgaben, kategorie in table_data:
                if len(table_data) > 0:
                    gesamt_einnahmen = gesamt_einnahmen + round(float(einnahmen), 2)

                    # Exclude cat "Sparen"
                    if kategorie != 'Sparen':
                        gesamt_ausgaben = gesamt_ausgaben + round(float(ausgaben), 2)
                else:
                    gesamt_einnahmen = 0.00
                    gesamt_ausgaben = 0.00

                if kategorie == 'Sparen':
                    gesamt_sparen = ausgaben

            self.list_einnahmen[i] = round(round(float(gesamt_einnahmen), 2) - round(float(gesamt_ausgaben), 2), 2)
            self.list_ausgaben[i] = round(float(gesamt_ausgaben), 2)
            self.list_gespartes[i] = float(gesamt_sparen)

        self.chart.update_percentage_data(listEinnahmen=self.list_einnahmen, listAusgaben=self.list_ausgaben, listGespartes=self.list_gespartes)

    # Update Pie Chart
    def pie_chart_data_changed(self):
        self.pie_label = "Top 5 Ausgaben"

        data = self.database.get_top_5_ausgaben(date=self.current_stichtag)
       
        self.chart_pie.update_pie_chart(data=data, pie_label=self.pie_label)

    # Update Bar Chart
    def bar_chart_data_changed(self):
        self.bar_chart.update_bar_chart(data=self.database.get_kategorie_sparen(), bar_chart_label='Gespartes')

    # Add a new categorie
    def add_new_categorie(self):
        self.new_categorie_dialog = NewCategorieDialog()

    # Export Table Data
    def on_click_export(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.ExistingFile)
        file = file.getSaveFileName()

        if file[0] != '':
            export_data = self.database.get_table_widget_data(self.current_stichtag)
            top5_in_zahlen = self.database.get_ausgaben_in_zahlen(self.current_stichtag)

            converted_export_ein_ausgaben = []
            converted_export_ausgaben_in_zahlen = []

            for row in export_data:
                converted_export_ein_ausgaben.append([row[0], row[1].replace('.', ','), row[2].replace('.', ','), row[3]])

            for row in top5_in_zahlen:
                converted_export_ausgaben_in_zahlen.append([row[0], str(row[1]).replace('.', ',')])

            df = pd.DataFrame(data=converted_export_ein_ausgaben, columns=['Datum', 'Einnahmen', 'Ausgaben', 'Kategorie'])
            df1 = pd.DataFrame(data=converted_export_ausgaben_in_zahlen, columns=['Kategorie', 'Summe'])

            with pd.ExcelWriter(file[0]) as excelWriter:
                df.to_excel(excelWriter, sheet_name='Ein- Ausgaben')
                df1.to_excel(excelWriter, sheet_name='Ausgaben in Zahlen')

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Export")
            msgBox.setText("Daten wurden exportiert!")
            msgBox.exec()

    # Set delta from Ein und Ausgaben for every month in current year
    def set_delta_sum_account_balance(self):
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        self.ui.label_dif_current_year.setText(self.current_stichtag[0:4])
        account_balance_current_year = self.database.get_delta_sum(self.current_stichtag)

        for calmonth, sum in account_balance_current_year:
            for label in self.ui.page_account_balance.findChildren(QLabel, name='label_dif_' + month[int(calmonth)-1] + '_sum'):
                label.setText(str(sum))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Loading Style
    with open('ui/style.qss', 'r') as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())