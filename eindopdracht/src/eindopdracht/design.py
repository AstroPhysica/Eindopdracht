# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Eindopdracht_structuur.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 10, 731, 341))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.start_button = QDoubleSpinBox(self.gridLayoutWidget)
        self.start_button.setObjectName(u"start_button")

        self.verticalLayout_2.addWidget(self.start_button)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.stop_button = QDoubleSpinBox(self.gridLayoutWidget)
        self.stop_button.setObjectName(u"stop_button")

        self.verticalLayout_2.addWidget(self.stop_button)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.runs_button = QDoubleSpinBox(self.gridLayoutWidget)
        self.runs_button.setObjectName(u"runs_button")

        self.verticalLayout_2.addWidget(self.runs_button)


        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_ff = QLabel(self.gridLayoutWidget)
        self.label_ff.setObjectName(u"label_ff")

        self.verticalLayout.addWidget(self.label_ff)

        self.text_line = QLineEdit(self.gridLayoutWidget)
        self.text_line.setObjectName(u"text_line")

        self.verticalLayout.addWidget(self.text_line)


        self.gridLayout.addLayout(self.verticalLayout, 4, 2, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.plot_button = QPushButton(self.gridLayoutWidget)
        self.plot_button.setObjectName(u"plot_button")

        self.verticalLayout_3.addWidget(self.plot_button)

        self.save_button = QPushButton(self.gridLayoutWidget)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout_3.addWidget(self.save_button)


        self.gridLayout.addLayout(self.verticalLayout_3, 4, 0, 1, 1)

        self.IU_graph = PlotWidget(self.gridLayoutWidget)
        self.IU_graph.setObjectName(u"IU_graph")

        self.gridLayout.addWidget(self.IU_graph, 2, 1, 1, 1)

        self.PU_graph = PlotWidget(self.gridLayoutWidget)
        self.PU_graph.setObjectName(u"PU_graph")

        self.gridLayout.addWidget(self.PU_graph, 2, 2, 1, 1)

        self.label_pu = QLabel(self.gridLayoutWidget)
        self.label_pu.setObjectName(u"label_pu")

        self.gridLayout.addWidget(self.label_pu, 0, 2, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.Pstring = QLineEdit(self.gridLayoutWidget)
        self.Pstring.setObjectName(u"Pstring")

        self.verticalLayout_4.addWidget(self.Pstring)


        self.gridLayout.addLayout(self.verticalLayout_4, 4, 1, 1, 1)

        self.label_iu = QLabel(self.gridLayoutWidget)
        self.label_iu.setObjectName(u"label_iu")

        self.gridLayout.addWidget(self.label_iu, 0, 1, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.list_devices = QComboBox(self.gridLayoutWidget)
        self.list_devices.setObjectName(u"list_devices")

        self.verticalLayout_5.addWidget(self.list_devices)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Start value", None))
        self.start_button.setSuffix(QCoreApplication.translate("MainWindow", u" Volt", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Stop value", None))
        self.stop_button.setSuffix(QCoreApplication.translate("MainWindow", u" Volt", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Number of runs", None))
        self.label_ff.setText(QCoreApplication.translate("MainWindow", u"FF value", None))
        self.plot_button.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label_pu.setText(QCoreApplication.translate("MainWindow", u"                                          PU Diagram", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"P-Max", None))
        self.label_iu.setText(QCoreApplication.translate("MainWindow", u"                                          IU Diagram", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Select Device", None))
    # retranslateUi

