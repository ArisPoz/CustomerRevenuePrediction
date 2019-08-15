# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form_main(object):
    def setupUi(self, form_main):
        form_main.setObjectName("form_main")
        form_main.resize(912, 763)
        form_main.setMinimumSize(QtCore.QSize(912, 763))
        form_main.setMaximumSize(QtCore.QSize(912, 763))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        form_main.setWindowIcon(icon)
        self.button_close = QtWidgets.QPushButton(form_main)
        self.button_close.setGeometry(QtCore.QRect(810, 720, 93, 28))
        self.button_close.setObjectName("button_close")
        self.button_clear = QtWidgets.QPushButton(form_main)
        self.button_clear.setGeometry(QtCore.QRect(810, 680, 93, 28))
        self.button_clear.setObjectName("button_clear")
        self.button_load = QtWidgets.QPushButton(form_main)
        self.button_load.setGeometry(QtCore.QRect(810, 570, 93, 28))
        self.button_load.setObjectName("button_load")
        self.console_output = QtWidgets.QTextEdit(form_main)
        self.console_output.setEnabled(False)
        self.console_output.setGeometry(QtCore.QRect(10, 570, 781, 181))
        self.console_output.setObjectName("console_output")
        self.graph_tab = QtWidgets.QTabWidget(form_main)
        self.graph_tab.setEnabled(True)
        self.graph_tab.setGeometry(QtCore.QRect(10, 10, 889, 549))
        self.graph_tab.setObjectName("graph_tab")

        self.retranslateUi(form_main)
        self.graph_tab.setCurrentIndex(-1)
        self.button_clear.clicked.connect(self.graph_tab.hide)
        QtCore.QMetaObject.connectSlotsByName(form_main)

    def retranslateUi(self, form_main):
        _translate = QtCore.QCoreApplication.translate
        form_main.setWindowTitle(_translate("form_main", "GA Customer Revenue"))
        self.button_close.setText(_translate("form_main", "Close"))
        self.button_clear.setText(_translate("form_main", "Clear"))
        self.button_load.setText(_translate("form_main", "Load Data"))
        self.console_output.setHtml(_translate("form_main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

