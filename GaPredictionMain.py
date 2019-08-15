from PyQt5 import QtCore, QtGui, QtWidgets, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import sys
import os
import datetime as dt
import DataFrameLoader as dfLoader
import CleaningDF as cDF
import Plots as showPlots

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

        self.button_close.clicked.connect(self.exit)

        self.button_clear.clicked.connect(self.clear)

        self.button_load.clicked.connect(self.load)

        self.show()  # Show the GUI

    def add_tab(self, name, figure):
        tab = QtWidgets.QWidget()
        canvas = FigureCanvas(figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        tab.setLayout(layout)
        self.graph_tab.addTab(tab, name)
        QtCore.QCoreApplication.processEvents()

    def update_progressbar(self, count):
        self.progressBar.setValue(count)
        QtCore.QCoreApplication.processEvents()

    def get_progressbar_status(self):
        return self.progressBar.value()

    def exit(self):
        self.close()

    def clear(self):
        self.console_output.setText('')

    def append(self, text):
        self.console_output.append(text)

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

    def load(self):
        self.button_load.setEnabled(False)
        self.update_progressbar(0)
        self.console_output.append("Loading Data (~25GB).")
        QtCore.QCoreApplication.processEvents()
        self.console_output.append("Started at : " + str(dt.datetime.now().time()))
        if os.path.exists("DataSets/train_cleaned.csv"):
            self.console_output.append("Loading cleaned train dataset...")
            train_df = dfLoader.load_df("DataSets/train_cleaned.csv", self)
            self.console_output.append("Loading cleaned test dataset...")
            test_df = dfLoader.load_df("DataSets/test_cleaned.csv", self)
        elif os.path.exists("DataSets/train_new.csv"):
            self.console_output.append("Loading new train dataset...")
            train_df = dfLoader.load_df("DataSets/train_new.csv", self)
            constants_columns = cDF.discovering_constant_columns(train_df)
            train_df = clean_data(train_df, constants_columns)
            train_df.to_csv("DataSets/train_cleaned.csv", index=False)

            self.console_output.append("Loading new test dataset...")
            test_df = dfLoader.load_df("DataSets/test_new.csv", self)
            test_df = clean_data(test_df, constants_columns)
            test_df.to_csv("DataSets/test_cleaned.csv", index=False)
        else:
            self.console_output.append("Loading train dataset...")
            train_df = dfLoader.load_df_clean_json("DataSets/train.csv", 100000)
            train_df.to_csv("DataSets/train_new.csv", index=False)

            self.console_output.append("Loading test dataset...")
            test_df = dfLoader.load_df_clean_json("DataSets/test.csv", 100000)
            test_df.to_csv("DataSets/test_new.csv", index=False)

        self.console_output.append("Finished at : " + str(dt.datetime.now().time()))
        self.console_output.append('Train data shape : ' + str(train_df.shape))
        self.console_output.append('Test data shape : ' + str(test_df.shape))

        self.load_graphs(train_df)

        self.console_output.append("Successfully loaded data.")
        self.update_progressbar(100)


def clean_data(df, to_drop):
    print("Data cleaning...")
    df = cDF.drop_constant_columns(df, to_drop)
    df = cDF.filling_na_values(df)
    df = cDF.normalizing(df)
    return df


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
