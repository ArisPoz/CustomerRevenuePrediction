import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import datetime as dt
import DataFrameLoader as dfLoader
import Plots as showPlots
import Prediction as pred

"""
Created on Fri Jul 26 13:48:19 2019

@author: apozidis
"""

Ui_MainWindow, QtBaseClass = uic.loadUiType('resources/gui.ui')


class Ui(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        self.setWindowTitle("Ga Customer Revenue")

        icon = QtGui.QIcon('resources/ga.ico')
        self.setWindowIcon(icon)
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setMaximumWidth(1070)
        self.setMinimumWidth(1070)

        # hidden/disabled/read-only parts
        self.label_PleaseWait.hide()
        self.console.hide()
        self.console.setReadOnly(True)
        self.console_output.setReadOnly(True)
        self.button_prediction.setEnabled(False)
        self.button_create_graph.setEnabled(False)
        self.line_Column.setEditable(True)

        # button action listener
        self.button_close.clicked.connect(self.exit)
        self.button_clear.clicked.connect(self.clear)
        self.button_load.clicked.connect(self.load)
        self.button_prediction.clicked.connect(self.predict)
        self.button_openConsole.clicked.connect(self.console_control)
        self.button_create_graph.clicked.connect(self.create_graph)

        self.show()  # Show the GUI

    def add_tab(self, name, figure, position, tooltip):
        tab = QtWidgets.QWidget()
        canvas = FigureCanvas(figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        tab.setLayout(layout)
        self.graph_tab.addTab(tab, name)
        self.graph_tab.setTabToolTip(position, tooltip)
        QtCore.QCoreApplication.processEvents()

    def add_tab_web_page(self, name, url, position, tooltip):
        tab = QtWidgets.QWidget()
        web_tab = QWebEngineView()
        web_url = QtCore.QUrl.fromLocalFile(r""+url)
        web_tab.load(web_url)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(web_tab)
        tab.setLayout(layout)
        self.graph_tab.addTab(tab, name)
        self.graph_tab.setTabToolTip(position, tooltip)
        QtCore.QCoreApplication.processEvents()

    def update_progressbar(self, count):
        self.progressBar.setValue(count)
        QtCore.QCoreApplication.processEvents()

    def console_control(self):
        if self.console.isVisible():
            self.console.hide()
            self.button_openConsole.setText("►")
            self.setMaximumWidth(1070)
            self.setMinimumWidth(1070)
            self.resize(1070, 858)
        else:
            self.console.show()
            self.button_openConsole.setText("◄")
            self.setMaximumWidth(1500)
            self.setMinimumWidth(1500)
            self.resize(1500, 858)

    def get_progressbar_status(self):
        return self.progressBar.value()

    def exit(self):
        self.close()

    def clear(self):
        self.console_output.setText('')

    def append(self, text):
        self.console_output.append(text)

    def append_console(self, text):
        self.console.append("#" * 10 + '\n' + text)

    def load_graphs(self, df):
        showPlots.show_revenue_graph(self, df)
        showPlots.show_device_browser(self, df)
        showPlots.show_cross_revenue_browser(self, df)
        showPlots.show_channel_grouping(self, df)
        showPlots.show_operating_systems(self, df)
        showPlots.transaction_by_os(self, df)
        showPlots.top_cities(self, df)
        showPlots.top_countries(self, df)
        showPlots.frequent_subcontinents(self, df)

    def create_graph(self):
        column = str(self.line_Column.currentText())
        title = self.line_Title.text()
        html = showPlots.pie_chart(train_df, column, title)
        self.append_console('Created Pie graph with title :' + title)
        self.add_tab_web_page(title, html, 15, column.capitalize() + "\n" + title.capitalize())

    def predict(self):
        global test_df
        self.label_PleaseWait.show()
        self.label_PleaseWait.setText('Please Wait while test data are loading...')
        self.console_output.append("Loading Test Data (~8GB).")
        QtCore.QCoreApplication.processEvents()
        test_df = dfLoader.load_test_set(self)
        self.console_output.append("Successfully loaded test data.")
        self.console_output.append("Starting Prediction ...")
        self.label_PleaseWait.setText('Please Wait While Predicting...')
        QtCore.QCoreApplication.processEvents()
        score = pred.predict_revenue_at_session_level(self, train_df, test_df)
        self.line_Prediction.setText(str(score))
        self.console_output.append('Test data shape : ' + str(test_df.shape))
        self.console_output.append("Prediction score (%) " + str(score * 100))
        self.update_progressbar(100)
        self.label_PleaseWait.hide()

    def load(self):
        global train_df
        self.label_PleaseWait.show()
        self.button_load.setEnabled(False)
        self.console_output.append("Loading Train Data (~20GB).")
        QtCore.QCoreApplication.processEvents()
        self.console_output.append("Started at : " + str(dt.datetime.now().time()))
        train_df = dfLoader.load_train_set(self)
        self.console_output.append("Finished at : " + str(dt.datetime.now().time()))
        self.console_output.append('Train data shape : ' + str(train_df.shape))
        self.load_graphs(train_df)

        self.console_output.append("Successfully loaded train data.")
        self.update_progressbar(100)
        self.label_PleaseWait.hide()
        self.button_prediction.setEnabled(True)
        self.button_create_graph.setEnabled(True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
