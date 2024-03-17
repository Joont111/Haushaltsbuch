import sqlite3
import os.path
from os import path

import pandas as pd
from PyQt5.QtWidgets import QMessageBox


class Database():
    def __init__(self):
        if path.exists('database/Haushalt.db'):
            self.create_table()


    def connect(self):
        connect = sqlite3.connect('database/Haushalt.db')

        return connect

    def insert_artikel(self, newData=None):
        connection = self.connect()
        cursor = connection.cursor()

        data_insert = []

        #Match von fehlenden Kategorien
        matched_data = self.match_artikel_kategorie(matchData=newData)

        if matched_data is not None:
            # Table: Calday, Calmonth, Calyear, Artikel, Preis, Kategorie
            for row in matched_data:
                data_insert.append([row[0], row[0][3:5], row[0][6:], row[1], row[2], row[3]])

            cursor.executemany("""INSERT INTO artikel VALUES(?, ?, ?, ?, ?, ?)""", data_insert)

            connection.commit()

        connection.close()

    def get_artikel(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT * FROM artikel"""
        cursor.execute(query)
        dataset = cursor.fetchall()

        return dataset

    def get_top_5_ausgaben(self, date=None):
        connection = self.connect()
        cursor = connection.cursor()

        month = date[5:7]
        year = date[:4]

        query = """SELECT artikelKategorie, round(sum(artikelPreis), 2) FROM artikel WHERE calmonth = '""" + month + """' AND calyear = '""" + year + """' GROUP BY artikelKategorie"""
        cursor.execute(query)
        dataset = cursor.fetchall()

        data_top_5 = []
        for row in dataset:
            data_top_5.append([row[0], row[1]])

        df = pd.DataFrame(data_top_5, columns=['Kategorie', 'Summe'])
        sorted_df = df.sort_values('Summe', ascending=False)

        data_top_5 = sorted_df.values.tolist()

        return data_top_5[0:5]

    def match_artikel_kategorie(self, matchData=None):
        connection = self.connect()
        cursor = connection.cursor()

        for row in matchData:

            if row[3] == 'None':
                query = """SELECT artikelKategorie FROM artikel WHERE artikelName = '""" + row[1] + """'"""

                cursor.execute(query)
                dataset = cursor.fetchall()

                if len(dataset) == 0:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setWindowTitle("Fehler")
                    msgBox.setText("Bitte Kategorie manuell matchen!")
                    msgBox.exec()

                    return None
                else:
                    row[3] = dataset[0][0]

        return matchData

    def save_table_widget_data(self, tableData=None):
        connection = self.connect()
        cursor = connection.cursor()

        data_insert = []

        # Table: Calday, Calmonth, Calyear, Einnahmen, Ausgaben, Kategorie
        for row in tableData:
            data_insert.append([row[0], row[0][3:5], row[0][6:], row[1].replace(' €', ''), row[2].replace(' €', ''), row[3]])

        cursor.executemany("""INSERT INTO tableWidgetDaten VALUES(?, ?, ?, ?, ?, ?)""", data_insert)

        connection.commit()

        connection.close()

    def delete_table_widget_data(self, caldate=None):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM tableWidgetDaten WHERE calmonth = '""" + caldate[5:7] + """' AND calyear = '""" + caldate[:4] + """'""")

        connection.commit()

        connection.close()

    def get_table_widget_data(self, caldate=None):
        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT calday, einnahmen, ausgaben, kategorie FROM tableWidgetDaten WHERE calmonth = '""" + caldate[5:7] + """' AND calyear = '""" + caldate[:4] + """'"""

        cursor.execute(query)
        dataset = cursor.fetchall()

        table_data = []

        for row in dataset:
            table_data.append([row[0], row[1].replace(' ', ''), row[2], row[3]])

        return table_data

    def get_kategorie_sparen(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT round(sum(ausgaben), 2) FROM tableWidgetDaten WHERE kategorie = 'Sparen'"""

        cursor.execute(query)
        dataset = cursor.fetchall()

        table_data = []

        sparen = 0.00
        db_summe = 0.00

        for row in dataset:

            db_summe = row[0]
            if db_summe != None:
                sparen = float(sparen) + float(db_summe)

        table_data.append([sparen])

        return table_data

    def save_new_categorie(self, categorie=None):
        connection = self.connect()
        cursor = connection.cursor()

        cat = []
        cat.append([categorie])

        cursor.executemany("""INSERT INTO kategorie VALUES(?)""", cat)

        connection.commit()

    def get_all_categories(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT kategorie FROM kategorie ORDER BY kategorie ASC"""

        cursor.execute(query)
        dataset = cursor.fetchall()

        table_data = []

        if len(dataset) == 0:
            table_data.append(['Bitte Kategorie anlegen'])
        else:
            for row in dataset:
                table_data.append([row[0]])

        return table_data

    def create_table(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS artikel (calday date, calmonth varchar(2), calyear int(11), artikelName varchar(100), artikelPreis float, artikelKategorie varchar(100));"""

        cursor.execute(query)
        connection.commit()

        query = """CREATE TABLE IF NOT EXISTS tableWidgetDaten (calday date, calmonth varchar(2), calyear int(11), einnahmen varchar(100), ausgaben varchar(100), kategorie varchar(100));"""

        cursor.execute(query)
        connection.commit()

        query = """CREATE TABLE IF NOT EXISTS kategorie (kategorie varchar(100));"""

        cursor.execute(query)
        connection.commit()

        query = """CREATE TABLE IF NOT EXISTS subscription (calday date, calmonth varchar(2), calyear int(11), sub_cat varchar(100), sub_name varchar(100), sub_period varchar(20), sub_start_date date, sub_duration varchar(20), sub_price float);"""

        cursor.execute(query)
        connection.commit()

        # Is Table categorie empty?
        query = """SELECT kategorie FROM kategorie ORDER BY kategorie ASC"""

        cursor.execute(query)
        dataset = cursor.fetchall()

        # If empty create initial cat's
        if len(dataset) == 0:
            cursor.execute("""INSERT INTO kategorie VALUES('Sparen')""")
            connection.commit()

            cursor.execute("""INSERT INTO kategorie VALUES('Einkauf')""")
            connection.commit()

        connection.close()

    def get_ausgaben_in_zahlen(self, date=None):
        connection = self.connect()
        cursor = connection.cursor()

        month = date[5:7]
        year = date[:4]

        query = """SELECT artikelKategorie, round(sum(artikelPreis), 2) FROM artikel WHERE calmonth = '""" + month + """' AND calyear = '""" + year + """' GROUP BY artikelKategorie"""
        cursor.execute(query)
        dataset = cursor.fetchall()

        data = []
        for row in dataset:
            data.append([row[0], row[1]])

        df = pd.DataFrame(data, columns=['Kategorie', 'Summe'])
        sorted_df = df.sort_values('Summe', ascending=False)

        data = sorted_df.values.tolist()

        return data

    def delete_data_by_calday(self, calday=None):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM artikel WHERE calday = '""" + calday + """'""")

        connection.commit()

        cursor.execute("""DELETE FROM tableWidgetDaten WHERE calday = '""" + calday + """'""")

        connection.commit()

    def get_delta_sum(self, date=None):

        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT calmonth, round(sum(einnahmen), 2), round(sum(ausgaben), 2) FROM tableWidgetDaten WHERE calyear = '""" + date[0:4] + """' AND kategorie != 'Sparen' GROUP BY calmonth"""
        cursor.execute(query)
        dataset = cursor.fetchall()

        data = []
        for row in dataset:
                data.append([row[0], row[1], row[2]])

        df = pd.DataFrame(data, columns=['Calmonth', 'Einnahmen', 'Ausgaben'])
        result_set = pd.DataFrame()
        
        sorted_df = df.sort_values('Calmonth', ascending=True)
        for element in sorted_df:
            result_set['calmonth'] = sorted_df['Calmonth']
            result_set['result'] = round(sorted_df['Einnahmen'] - sorted_df['Ausgaben'], 2)
        
        sorted_result = result_set.sort_values('calmonth', ascending=True)
        data = sorted_result.values.tolist()

        return data       
    
    def get_delta_single_sum(self, date=None):
        connection = self.connect()
        cursor = connection.cursor()

        query = """SELECT calmonth, round(sum(einnahmen), 2), round(sum(ausgaben), 2) FROM tableWidgetDaten WHERE calmonth = """ + date[5:7] + """ AND calyear = '""" + date[0:4] + """' AND kategorie != 'Sparen' GROUP BY calmonth"""
        cursor.execute(query)
        dataset = cursor.fetchall()

        data = []
        for row in dataset:
                data.append([row[1] - row[2]])

        return data
    
    def save_subscription_data(self, sub_calday, sub_cat, sub_name, sub_period, sub_start_date, sub_duration, sub_price):
        connection = self.connect()
        cursor = connection.cursor()
        
        sub_calday = sub_calday
        sub_calmonth = sub_calday[5:7]
        sub_calyear = sub_calday[:4]

        dataset = []

        dataset.append([sub_calday, sub_calmonth, sub_calyear, sub_cat, sub_name, sub_period, sub_start_date, sub_duration, sub_price])

        cursor.executemany("""INSERT INTO subscription VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", dataset)

        connection.commit()

        connection.close()

    def get_subscription_data(self, date=None):
        connection = self.connect()
        cursor = connection.cursor()

        if date != None:
            query = """SELECT sub_name, sub_period, sub_start_date, sub_duration, sub_price FROM subscription WHERE calmonth = '""" + date[5:7] + """' AND calyear = '""" + date[0:4] + """'"""
        else:
            query = """SELECT sub_name, sub_period, sub_start_date, sub_duration, sub_price FROM subscription"""

        cursor.execute(query)
        dataset = cursor.fetchall()

        data = []
        for row in dataset:
                data.append([row[2], row[0], row[1], row[3], row[4]])

        return data
    
    def delete_subscription_data(self, name=None):
        connection = self.connect()
        cursor = connection.cursor()

        query = """DELETE FROM subscription WHERE sub_name = '""" + name + """'"""   

        cursor.execute(query)
        connection.commit()

        connection.close()    

    def update_subscription_data_year(self, data=None):
        connection = self.connect()
        cursor = connection.cursor()

        for element in data:
            calmonth = element[0][3:5]
            calyear = int(element[0][6:]) + 1 # set to next year
            
            new_date = str(calyear) + '-' + calmonth + '-' + '01' 
            
            query = """UPDATE subscription SET calday = '""" + new_date + """', calyear = '""" + str(calyear) + """' WHERE sub_name = '""" + element[1] + """'"""   

            cursor.execute(query)
            connection.commit()

        connection.close()          