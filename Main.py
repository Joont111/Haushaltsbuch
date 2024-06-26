import csv
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QBrush
from PyQt5 import QtCore
from Chart import Chart
import dateutil.relativedelta

from ui.ui_mainwindow import Ui_MainWindow
from NewCategorieDialog import NewCategorieDialog
from NewDataDialog import NewDataDialog
from DeleteDataDialog import DeleteDataDialog
from InfoDialog import InfoDialog
from NewSubDialog import NewSubDialog
from DeleteSubDataDialog import DeleteSubDataDialog
from Database import Database

from datetime import date, datetime
import calendar
import pandas as pd
import numpy as np

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

        # Syn function to add new subs or current subs into table data
        self.sync_sub_data_with_table_data()

        # Connect Buttonns to functions
        self.ui.home_button_1.toggled.connect(self.on_home_button_1_toggled)
        self.ui.home_button_2.toggled.connect(self.on_home_button_2_toggled)

        self.ui.dashboard_button_1.toggled.connect(self.on_dashboard_button_1_toggled)
        self.ui.dashboard_button_2.toggled.connect(self.on_dashboard_button_2_toggled)

        self.ui.table_button_1.toggled.connect(self.on_table_button_1_toggled)
        self.ui.table_button_2.toggled.connect(self.on_table_button_2_toggled)

        self.ui.account_balance_button_1.toggled.connect(self.on_account_balance_1_toggled)
        self.ui.account_balance_button_2.toggled.connect(self.on_account_balance_2_toggled)

        self.ui.sub_button_1.toggled.connect(self.on_sub_1_toggled)
        self.ui.sub_button_2.toggled.connect(self.on_sub_2_toggled)

        self.ui.add_categorie_button.clicked.connect(self.add_new_categorie)
        self.ui.add_fixed_costs_button.clicked.connect(self.on_click_load_fixed_costs)
        self.ui.add_data_button.clicked.connect(self.on_click_new_data)
        self.ui.delete_data_button.clicked.connect(self.on_click_delete_data)
        self.ui.export_data_button.clicked.connect(self.on_click_export)
        
        self.ui.info_button_1.clicked.connect(self.on_click_show_info_dialog)
        self.ui.info_button_2.clicked.connect(self.on_click_show_info_dialog)

        self.ui.add_sub_button.clicked.connect(self.on_click_new_sub)
        self.ui.delete_sub_button.clicked.connect(self.on_click_delete_sub)

        self.ui.exit_button_1.clicked.connect(self.close)
        self.ui.exit_button_2.clicked.connect(self.close)

        #self.ui.combo_box_stichtag.currentTextChanged.connect(self.get_stichtag)
        self.ui.date_edit_stichtag.dateChanged.connect(self.get_stichtag)

        # Create TableWidget -> account balance -> Differences Cat's
        self.table_widget_cat_month = QTableWidget()
        self.table_widget_cat_prev_month = QTableWidget() # TableWidget on left side; Just with cat's from previous month
        self.table_widget_cat_curr_month = QTableWidget() # TableWidget on right side; Just with cat's from current month

        # Create TableWidget -> Subscription data
        self.table_widget_subscription_data = QTableWidget()

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
        # self.set_delta_sum_account_balance()
    

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

    def on_sub_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.show_all_subscription_data()

    def on_sub_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.show_all_subscription_data()

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

    def on_click_new_sub(self):
        self.sub_dialog = NewSubDialog()
            
    # Delete Data
    def on_click_delete_sub(self):
        self.delete_sub_dialog = DeleteSubDataDialog()

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

        # Table categorie differences refresh & load
        self.calc_dif_categorie_prev_curr_month()

        # Table sub refresh & load
        self.show_all_subscription_data()

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
        # Set to 0 because on a change the old data will be visible on field that has no values
        self.set_delta_sum_account_balance_to_zero()

        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        self.ui.label_dif_current_year.setText(self.current_stichtag[0:4])
        account_balance_current_year = self.database.get_delta_sum(self.current_stichtag)

        for calmonth, sum in account_balance_current_year:
            for label in self.ui.page_account_balance.findChildren(QLabel, name='label_dif_' + month[int(calmonth)-1] + '_sum'):
                label.setText(str(sum) + ' €')

        self.calc_delta_account_balance_prev_curr_month()

    # set all difference label to 0
    def set_delta_sum_account_balance_to_zero(self):
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for calmonth in month:
            label = self.ui.page_account_balance.findChild(QLabel, name='label_dif_' + calmonth + '_sum')
            label.setText(str('0.00 €'))        

        for calmonth in month:
            label = self.ui.page_account_balance.findChild(QLabel, name='label_dif_' + calmonth + '_vm')
            label.setText(str('0.00 €'))


    # Calc dif between month
    def calc_delta_account_balance_prev_curr_month(self):
        month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        self.ui.label_dif_current_year.setText(self.current_stichtag[0:4])
        account_balance_current_year = self.database.get_delta_sum(self.current_stichtag)
        account_balance_dec_prev_year = self.database.get_delta_single_sum((str(int(self.current_stichtag[0:4]) - 1) + '-12-31'))

        if len(account_balance_dec_prev_year) == 0:
            prev_dec = {'dez': [0.00]}
        else:
            prev_dec = {'dez': [account_balance_dec_prev_year[0][0]]}

        for calmonth, sum in account_balance_current_year:
            label = self.ui.page_account_balance.findChild(QLabel, name='label_dif_' + month[int(calmonth)-1] + '_vm')

            if calmonth == '01':
                if prev_dec['dez'][0] == 0.00:
                    label.setText(str('0.00 €'))
                else:
                    label.setText(str(prev_dec['dez'][0]) + ' €')

                prev_month_sum = sum
            else:
                if prev_month_sum == 0.00:
                    label.setText('0.00 €')
                else:
                    label.setText(str(round(sum - prev_month_sum, 2)) + ' €' )
                    prev_month_sum = sum

    def calc_dif_categorie_prev_curr_month(self):
        # Get current and previous month from selected stichtag
        curr_month = datetime(int(self.current_stichtag[0:4]), int(self.current_stichtag[6:7]), 1)
        prev_month = curr_month - dateutil.relativedelta.relativedelta(months=1)

        # get list with selected categories
        cat_curr_month = self.database.get_ausgaben_in_zahlen(date=str(curr_month.date()))
        cat_prev_month = self.database.get_ausgaben_in_zahlen(date=str(prev_month.date()))

        # Set to dataframe
        df_curr_month = pd.DataFrame(cat_curr_month, columns=['cat', 'summe'])
        df_prev_month = pd.DataFrame(cat_prev_month, columns=['cat', 'summe'])

        df_result = df_curr_month.set_index(['cat']).subtract(df_prev_month.set_index(['cat']))
        df_result = df_result.dropna()
        df_result = df_result.reset_index()
        df_result = df_result.sort_values(['summe'], ascending=True)

        # Get prev month data
        list_curr_month = df_curr_month.cat.tolist()
        list_prev_month = df_prev_month.cat.tolist()
        
        # diff_cat_curr_month = set(list_curr_month).difference(set(list_prev_month)) # Categories that only appear in the current month
        diff_cat_prev_month = set(list_prev_month).difference(set(list_curr_month))
        df_prev_month = df_prev_month[df_prev_month.cat.isin(diff_cat_prev_month)]

        # Reset Row Count for new Data (Change Key Date)
        self.table_widget_cat_month.setRowCount(0)
        self.table_widget_cat_prev_month.setRowCount(0)
        self.table_widget_cat_curr_month.setRowCount(0)

        # Left Table
        # Categories that only appear in the previous month
        self.table_widget_cat_prev_month.setColumnCount(2)   
        self.table_widget_cat_prev_month.setHorizontalHeaderItem(0, QTableWidgetItem('Kategorie'))
        self.table_widget_cat_prev_month.setHorizontalHeaderItem(1, QTableWidgetItem('Summe'))
   
        #Table will fit the screen horizontally 
        self.table_widget_cat_prev_month.horizontalHeader().setStretchLastSection(True) 
        self.table_widget_cat_prev_month.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.ui.group_box_lay_cat_prev_month.addWidget(self.table_widget_cat_prev_month)

        table_data_left = df_prev_month.values.tolist()

        for categorie, summe in table_data_left:
            row = self.table_widget_cat_prev_month.rowCount()
            self.table_widget_cat_prev_month.insertRow(row)

            self.table_widget_cat_prev_month.setItem(row, 0, QTableWidgetItem(categorie))
            self.table_widget_cat_prev_month.setItem(row, 1, QTableWidgetItem(str(round(summe, 2))))

        # Categories that occur in the previous month and the current month
        #Column count 
        self.table_widget_cat_month.setColumnCount(2)   
        self.table_widget_cat_month.setHorizontalHeaderItem(0, QTableWidgetItem('Kategorie'))
        self.table_widget_cat_month.setHorizontalHeaderItem(1, QTableWidgetItem('Summe'))
   
        #Table will fit the screen horizontally 
        self.table_widget_cat_month.horizontalHeader().setStretchLastSection(True) 
        self.table_widget_cat_month.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.ui.group_box_lay_cat_month.addWidget(self.table_widget_cat_month)

        table_data_mid = df_result.values.tolist()

        for categorie, summe in table_data_mid:
            row = self.table_widget_cat_month.rowCount()
            self.table_widget_cat_month.insertRow(row)

            number = round(summe, 2)
            formatedNumber = QTableWidgetItem(str(round(summe, 2)))

            if number < 0:
                formatedNumber.setForeground(QBrush(QColor(34, 139, 34)))
            else:
                formatedNumber.setForeground(QBrush(QColor(205, 51, 51)))

            self.table_widget_cat_month.setItem(row, 0, QTableWidgetItem(categorie))
            self.table_widget_cat_month.setItem(row, 1, QTableWidgetItem(formatedNumber))

        # Categories that occur in the current month
            
        diff_cat_curr_month = set(list_curr_month).difference(set(list_prev_month)) # Categories that only appear in the current month
        df_curr_month = df_curr_month[df_curr_month.cat.isin(diff_cat_curr_month)]

        #Column count     
        self.table_widget_cat_curr_month.setColumnCount(2)   
        self.table_widget_cat_curr_month.setHorizontalHeaderItem(0, QTableWidgetItem('Kategorie'))
        self.table_widget_cat_curr_month.setHorizontalHeaderItem(1, QTableWidgetItem('Summe'))
   
        #Table will fit the screen horizontally 
        self.table_widget_cat_curr_month.horizontalHeader().setStretchLastSection(True) 
        self.table_widget_cat_curr_month.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.ui.group_box_lay_cat_cur_month.addWidget(self.table_widget_cat_curr_month)

        table_data_right = df_curr_month.values.tolist()  

        for categorie, summe in table_data_right:
            row = self.table_widget_cat_curr_month.rowCount()
            self.table_widget_cat_curr_month.insertRow(row)

            self.table_widget_cat_curr_month.setItem(row, 0, QTableWidgetItem(categorie))
            self.table_widget_cat_curr_month.setItem(row, 1, QTableWidgetItem(str(round(summe, 2))))

    def show_all_subscription_data(self):
        subscription_data = self.database.get_subscription_data()

        # Reset Row Count for new Data (Change Key Date)
        self.table_widget_subscription_data.setRowCount(0)

        # Left Table
        # Categories that only appear in the previous month
        self.table_widget_subscription_data.setColumnCount(5)   
        self.table_widget_subscription_data.setHorizontalHeaderItem(0, QTableWidgetItem('Beginn ab'))
        self.table_widget_subscription_data.setHorizontalHeaderItem(1, QTableWidgetItem('Beschreibung'))
        self.table_widget_subscription_data.setHorizontalHeaderItem(2, QTableWidgetItem('Abrechnung'))
        self.table_widget_subscription_data.setHorizontalHeaderItem(3, QTableWidgetItem('Laufzeit'))
        self.table_widget_subscription_data.setHorizontalHeaderItem(4, QTableWidgetItem('Preis'))

        #Table will fit the screen horizontally 
        self.table_widget_subscription_data.horizontalHeader().setStretchLastSection(True) 
        self.table_widget_subscription_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.ui.page_sub_horizontal_layout.addWidget(self.table_widget_subscription_data)

        for start_date, name, period, duration, price in subscription_data:
            row = self.table_widget_subscription_data.rowCount()
            self.table_widget_subscription_data.insertRow(row)

            self.table_widget_subscription_data.setItem(row, 0, QTableWidgetItem(start_date))
            self.table_widget_subscription_data.setItem(row, 1, QTableWidgetItem(name))    
            self.table_widget_subscription_data.setItem(row, 2, QTableWidgetItem(period))    
            self.table_widget_subscription_data.setItem(row, 3, QTableWidgetItem(duration))
            self.table_widget_subscription_data.setItem(row, 4, QTableWidgetItem(str(price)))

    def sync_sub_data_with_table_data(self):
        table_data = pd.DataFrame(self.database.get_table_widget_data(self.current_stichtag), columns=['date', 'einnahmen', 'ausgaben', 'text'])
        sub_data = pd.DataFrame(self.database.get_subscription_data(self.current_stichtag), columns=['date', 'text', 'abrechnung', 'laufzeit', 'preis'])
        sub_data_year = sub_data.copy()
        current_date = self.ui.date_edit_stichtag.date().toPyDate().strftime("%d.%m.%Y")

        # Get index from data there is in table data
        new_data = sub_data[sub_data.text.isin(table_data.text)].index
        
        # Delete all subscriptions that already exist in the data tables 
        sub_data.drop(new_data, inplace=True)

        # Check start date of new subs
        not_now_values = sub_data[sub_data['date'] > current_date].index
        sub_data.drop(not_now_values, inplace=True)

        sub_data = sub_data.reset_index(drop=True)

        sub_data_list = []

        sub_data_list = sub_data.values.tolist()

        new_data = []

        # Harmonize data for tableWidget
        for element in sub_data_list:
            new_data.append([current_date, '0.00 €', str(str(element[4]) + ' €'), element[1]])

        # Save data into table widget
        self.database.save_table_widget_data(tableData=new_data)

        # after saving the data, we will set the 'jährlich' data to next year
        update_values = sub_data_year[sub_data_year['abrechnung'] == 'monatlich'].index
        sub_data_year.drop(update_values, inplace=True)

        sub_data_year_list = sub_data_year.values.tolist()

        self.database.update_subscription_data_year(data=sub_data_year_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Loading Style
    with open('ui/style.qss', 'r') as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())