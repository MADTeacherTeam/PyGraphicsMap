# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompositeTileSourceConfigurationWidget_ui.ui'
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


class Ui_CompositeTileSourceConfigurationWidget(object):
    def setupUi(self, CompositeTileSourceConfigurationWidget):
        if CompositeTileSourceConfigurationWidget.objectName():
            CompositeTileSourceConfigurationWidget.setObjectName(u"CompositeTileSourceConfigurationWidget")
        CompositeTileSourceConfigurationWidget.resize(393, 343)
        self.verticalLayout = QVBoxLayout(CompositeTileSourceConfigurationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addSourceButton = QToolButton(CompositeTileSourceConfigurationWidget)
        self.addSourceButton.setObjectName(u"addSourceButton")
        icon = QIcon()
        icon.addFile("../images/edit_add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addSourceButton.setIcon(icon)
        self.addSourceButton.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.addSourceButton)

        self.addSourceButton_2 = QToolButton(CompositeTileSourceConfigurationWidget)
        self.addSourceButton_2.setObjectName(u"addSourceButton_2")
        self.addSourceButton_2.setIcon(icon)
        self.addSourceButton_2.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.addSourceButton_2)

        self.addSourceButton_3 = QToolButton(CompositeTileSourceConfigurationWidget)
        self.addSourceButton_3.setObjectName(u"addSourceButton_3")
        self.addSourceButton_3.setIcon(icon)
        self.addSourceButton_3.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.addSourceButton_3)

        self.removeSourceButton = QToolButton(CompositeTileSourceConfigurationWidget)
        self.removeSourceButton.setObjectName(u"removeSourceButton")
        self.removeSourceButton.setPopupMode(QToolButton.InstantPopup)
        icon1 = QIcon()
        icon1.addFile("../images/editdelete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeSourceButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.removeSourceButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listView = QListView(CompositeTileSourceConfigurationWidget)
        self.listView.setObjectName(u"listView")
        self.listView.setFocusPolicy(Qt.ClickFocus)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setDragDropMode(QAbstractItemView.InternalMove)
        self.listView.setUniformItemSizes(True)

        self.verticalLayout.addWidget(self.listView)


        self.retranslateUi(CompositeTileSourceConfigurationWidget)

        QMetaObject.connectSlotsByName(CompositeTileSourceConfigurationWidget)
    # setupUi

    def retranslateUi(self, CompositeTileSourceConfigurationWidget):
        CompositeTileSourceConfigurationWidget.setWindowTitle(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"Form", None))
        self.addSourceButton.setText(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"+", None))
        self.addSourceButton_2.setText(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"+", None))
        self.addSourceButton_3.setText(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"+", None))
        self.removeSourceButton.setText(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"X", None))
    # retranslateUi

