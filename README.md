<br/>
<p align="center">
  <a href="https://github.com/Joont111/Haushaltsbuch">
    <img src="https://raw.githubusercontent.com/Joont111/Haushaltsbuch/main/ui/icon/analytics_chart.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Haushaltsbuch</h3>

  <p align="center">
    Dieses Tool hilft dir dabei deine Haushaltskosten zu analysieren.

Danke an [ShaanCoding](https://github.com/ShaanCoding/) für den Readme Generator!
Thanks to [ShaanCoding](https://github.com/ShaanCoding/) for the readme generator!
    <br/>
    <br/>
  </p>
</p>



## Inhalt

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

![Screen Shot](https://github.com/Joont111/Haushaltsbuch/blob/main/screenshots/screenshot_dashboard.jpg)

Die Idee für dieses Projekt ist mir nach dem einkaufen gekommen. Wer sich bei den Bonusprogrammen seines Supermarktes des vertrauens angemeldet hat, wird sicherlich schon einen Digitalen-Kassenbon bekommen haben.

Die Daten werden in Excel etwas formatiert, in eine CSV Datei umgewandelt und dann in die Software eingelesen. Daraus werden die verschiedenen Diagramme erstellt. (Beispiel Dateien sind vorhanden)

Zusätzlich gibt es eine Datei für die Fixkosten. Die kannst du ausfüllen und jeden Monat neu einlesen. Die Daten der Fixkosten werden nicht mit in die Top 5 Ausgaben eingerechnet.

![Screen Shot](https://github.com/Joont111/Haushaltsbuch/blob/main/screenshots/screenshot_menu.jpg)

![Screen Shot](https://github.com/Joont111/Haushaltsbuch/blob/main/screenshots/screenshot_listen.jpg)

![Screen Shot](https://github.com/Joont111/Haushaltsbuch/blob/main/screenshots/screenshot_deltaberechnung.png)

## Getting Started
Über den Download-Link kannst du dir den aktuellen Release herunterladen. Entpacke den Ordner und kopiere den Inhalt an einen Ort deiner Wahl. 
[Download](https://drive.google.com/file/d/1Koe9NUxOVbFBEtNTbzh2GLWn-M-vy1BT/view?usp=sharing)

## Built With

Die Anwendung wurde mit Python und Qt entwickelt. Nachfolgende Module habe ich dabei verwendet:

* [QtChart](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QChart.html)
* [csv](https://docs.python.org/3/library/csv.html)
* [QBarSet](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QBarSet.html)
* [QPercentBarSeries](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QPercentBarSeries.html)
* [QChart](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QChart.html)
* [QBarCategoryAxis](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QBarCategoryAxis.html)
* [QChartView](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QChartView.html)
* [QPieSeries](https://doc.qt.io/qtforpython-6/examples/example_charts_piechart.html)
* [QValueAxis](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QValueAxis.html)
* [QBarSeries](https://doc.qt.io/qtforpython-6/PySide6/QtCharts/QAbstractBarSeries.html)
* [QColor](https://doc.qt.io/qtforpython-5/PySide2/QtGui/QColor.html)
* [QPainter](https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPainter.html)
* [QPen](https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPen.html)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [calendar](https://docs.python.org/3/library/calendar.html)
* [pandas](https://pandas.pydata.org)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
* [QMessageBox](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMessageBox.html)
* [QDateEdit](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDateEdit.html)

## Usage

In dem Ordner "example_data" sind zwei Beispieldateien hinterlegt. Die Dateien kannst du für deine Daten verwenden.

- Fixkosten:
Die Datei besteht aus den Einnahmen, Ausgaben und einer Kategorie. In der Spalte Einnahmen trägst du zum Beispiel dein Gehalt ein. In die Spalte Ausgaben alle diese, die jeden Monat auf's neue abgerechnet werden. Wie zum Beispiel Streamingdienste, Strom, Handy oder Internet. Die Kategorien sind flexibel und können von die frei benannt werden. 

Solltest du eine Position Sparen haben, dann trägst du die Summe ebenfalls in die Ausgaben-Spalte ein. Die Kategorie ist fix und sollte immer als "Sparen" ausgewiesen werden. Andernfalls wird die Position im Diagramm nicht beachtet.

- Ausgaben:
Die Datei ist nach den Spalten Artikel, Preis und Kategorie eingeteilt. In der Spalte Artikel trägst du alles ein, was du gekauft hast. Zum Beispiel: Brot, Käse etc. Die Spalte Preis erklärt sich von selbst. In die Kategorie kannst du den Artikel einordnen. Zum Beispiel Lebensmittel, Hygiene, Süßigkeiten oder anderes. Solltest du öfter diese Artikel kaufen, sollte die Kategorie immer die selbe sein. (Aktueller Stand der Anwendung)

Tipp: Trag die Artikel am besten immer so ein, wie sie auf dem Kassenzettel stehen.

Wenn du alles eingetragen hast, dann speichere die Datei als CSV ab und lies sie in die Anwendung ein.

Wichtig: Entferne die €-Zeichen aus den Spalten!

## Roadmap

Eine Liste der vorgeschlagenen Funktionen (und bekannten Probleme) finden Sie in den [open issues](https://github.com/Joont111/Haushaltsbuch/issues).

## Authors

* **Christian S.** - *SAP Consultant* - [Chris](https://github.com/Joont111) - *Idee & Umsetzung Haushaltsbuch*

## Acknowledgements

* [ShaanCoding](https://github.com/ShaanCoding/)
