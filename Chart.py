from PyQt5 import QtChart
from PyQt5.QtChart import QBarSet, QPercentBarSeries, QChart, QBarCategoryAxis, QChartView, QPieSeries, QValueAxis, \
    QBarSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen


class Chart():
    def __init__(self):
        self.percentage_bar_chart = QChart()
        self.pie_chart = QChart()
        self.bar_chart = QChart()

    def func_percentage_bar(self, listEinnahmen=None, listAusgaben=None, listGespartes=None):
        self.set0 = QBarSet("Einnahmen")
        self.set0.setColor(QColor('#003f5c'))
        self.set1 = QBarSet("Ausgaben")
        self.set1.setColor(QColor('#bc5090'))
        self.set2 = QBarSet("Gespartes")
        self.set2.setColor(QColor('#ffa600'))

        self.set0.append(listEinnahmen)
        self.set1.append(listAusgaben)
        self.set2.append(listGespartes)

        self.series = QPercentBarSeries()
        self.series.append(self.set0)
        self.series.append(self.set1)
        self.series.append(self.set2)

        self.percentage_bar_chart.addSeries(self.series)
        self.percentage_bar_chart.setTitle("Einnahmen / Ausgaben / Gespartes in %")
        self.percentage_bar_chart.setTitleBrush(QColor('#fff'))
        self.percentage_bar_chart.setAnimationOptions(QChart.SeriesAnimations)

        self.categories = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        self.axis = QBarCategoryAxis()
        self.axis.append(self.categories)
        self.percentage_bar_chart.createDefaultAxes()

        self.percentage_bar_chart.addAxis(self.axis, Qt.AlignBottom)
        self.series.attachAxis(self.axis)

        self.percentage_bar_chart.legend().setVisible(True)
        self.percentage_bar_chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view = QChartView(self.percentage_bar_chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        return self.chart_view

    # Update Data from Chart
    def update_percentage_data(self, listEinnahmen, listAusgaben, listGespartes):
        # Clear the current Data Series
        self.percentage_bar_chart.removeSeries(self.series)

        # Clear the sets 
        self.set0.remove(0, len(self.set0))
        self.set1.remove(0, len(self.set1))
        self.set2.remove(0, len(self.set2))

        self.set0.append(listEinnahmen)
        self.set1.append(listAusgaben)
        self.set2.append(listGespartes)

        self.series.append(self.set0)
        self.series.append(self.set1)
        self.series.append(self.set2)

        self.percentage_bar_chart.addSeries(self.series)

    def func_pie_chart(self, data=None, pieLabel=None):
        self.pie_series = QPieSeries()

        list_color = [QColor('#003f5c'), QColor('#58508d'), QColor('#bc5090'), QColor('#ff6361'), QColor('#ffa600')]
        slice_index = 0

        for label, value in data:
            self.pie_series.append(label, value)
            self.slice = self.pie_series.slices()[slice_index]
            self.slice.setLabelVisible()
            self.slice.setPen(QPen(list_color[slice_index], 2))
            self.slice.setBrush(list_color[slice_index])

            slice_index += 1

        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setTitle(pieLabel)
        self.pie_chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.pie_chart.legend()

        self._chart_view = QChartView(self.pie_chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        return self._chart_view

    def update_pie_chart(self, data=None, pie_label=None):
        self.pie_series = QPieSeries()

        list_color = [QColor('#003f5c'), QColor('#58508d'), QColor('#bc5090'), QColor('#ff6361'), QColor('#ffa600')]
        slice_index = 0

        for label, value in data:
            self.pie_series.append(label, value)
            self.slice = self.pie_series.slices()[slice_index]
            self.slice.setLabelVisible()
            self.slice.setPen(QPen(list_color[slice_index], 2))
            self.slice.setBrush(list_color[slice_index])

            slice_index += 1

        self.pie_chart.removeAllSeries()

        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setTitle(pie_label)

    def func_bar_chart(self, data=None, barChartLabel=None):
        self.bar_char_set_0 = QBarSet("Gespartes")

        self.bar_char_set_0.append(data[0])
        self.bar_char_set_0.setColor(QColor('#003f5c'))

        self.bar_chart_series = QBarSeries()
        self.bar_chart_series.append(self.bar_char_set_0)

        self.bar_chart.addSeries(self.bar_chart_series)
        self.bar_chart.setTitle(barChartLabel)
        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)

        self.categories = ["Summe"]
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.bar_chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_chart_series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.bar_chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_chart_series.attachAxis(self.axis_y)

        self.bar_chart.legend().setVisible(True)
        self.bar_chart.legend().setAlignment(Qt.AlignBottom)

        self.bar_chart_view = QChartView(self.bar_chart)
        self.bar_chart_view.setRenderHint(QPainter.Antialiasing)

        return self.bar_chart_view
    
    def update_bar_chart(self, data=None, bar_chart_label=None):
        self.bar_chart.removeSeries(self.bar_chart_series)
        self.bar_char_set_0 = QBarSet('Gespartes')

        self.bar_char_set_0.append(data[0])
        self.bar_char_set_0.setColor(QColor('#003f5c'))

        self.bar_chart_series = QBarSeries()
        self.bar_chart_series.append(self.bar_char_set_0)

        self.bar_chart.addSeries(self.bar_chart_series)
        self.bar_chart.setTitle(bar_chart_label)

        self.bar_chart.removeAxis(self.axis_y)

        self.axis_y = QValueAxis()
        self.bar_chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_chart_series.attachAxis(self.axis_y)