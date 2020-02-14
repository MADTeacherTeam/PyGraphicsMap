# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1103, 688)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1103, 21))
        self.menuWindow = QMenu(self.menuBar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuWindow.menuAction())
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TestApp", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Layers", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"&Window", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
    # retranslateUi

