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
        self.toolBox = QToolBox(CompositeTileSourceConfigurationWidget)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setAutoFillBackground(False)
        self.markPage = QWidget()
        self.markPage.setObjectName(u"markPage")
        self.markPage.setGeometry(QRect(0, 0, 375, 271))
        self.formLayoutWidget = QWidget(self.markPage)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(0, 0, 81, 251))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 10, 0)
        self.verticalSpacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(0, QFormLayout.FieldRole, self.verticalSpacer)

        self.addMark_button = QPushButton(self.formLayoutWidget)
        self.addMark_button.setObjectName(u"addMark_button")
        icon = QIcon()
        icon.addFile(u"../images/edit_add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addMark_button.setIcon(icon)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.addMark_button)

        self.removeMark_button = QPushButton(self.formLayoutWidget)
        self.removeMark_button.setObjectName(u"removeMark_button")
        icon1 = QIcon()
        icon1.addFile(u"../images/editdelete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeMark_button.setIcon(icon1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.removeMark_button)

        self.changeColor_button = QPushButton(self.formLayoutWidget)
        self.changeColor_button.setObjectName(u"changeColor_button")
        icon2 = QIcon()
        icon2.addFile(u"../images/palette.png", QSize(), QIcon.Normal, QIcon.Off)
        self.changeColor_button.setIcon(icon2)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.changeColor_button)

        self.test_button = QPushButton(self.formLayoutWidget)
        self.test_button.setObjectName(u"test_button")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.test_button)

        self.verticalSpacer_2 = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(3, QFormLayout.FieldRole, self.verticalSpacer_2)

        self.toolBox.addItem(self.markPage, u"Marks")
        self.routePage = QWidget()
        self.routePage.setObjectName(u"routePage")
        self.routePage.setGeometry(QRect(0, 0, 375, 271))
        self.formLayoutWidget_2 = QWidget(self.routePage)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(0, 0, 77, 251))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.formLayout_2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout_2.setLabelAlignment(Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout_2.setContentsMargins(0, 0, 10, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout_2.setItem(0, QFormLayout.FieldRole, self.verticalSpacer_3)

        self.setRoad_button_2 = QPushButton(self.formLayoutWidget_2)
        self.setRoad_button_2.setObjectName(u"setRoad_button_2")
        self.setRoad_button_2.setIcon(icon)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.setRoad_button_2)

        self.removeRoad_button_2 = QPushButton(self.formLayoutWidget_2)
        self.removeRoad_button_2.setObjectName(u"removeRoad_button_2")
        self.removeRoad_button_2.setIcon(icon1)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.removeRoad_button_2)

        self.test_button_3 = QPushButton(self.formLayoutWidget_2)
        self.test_button_3.setObjectName(u"test_button_3")
        self.test_button_3.setIcon(icon2)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.test_button_3)

        self.test_button_2 = QPushButton(self.formLayoutWidget_2)
        self.test_button_2.setObjectName(u"test_button_2")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.test_button_2)

        self.verticalSpacer_4 = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout_2.setItem(3, QFormLayout.FieldRole, self.verticalSpacer_4)

        self.toolBox.addItem(self.routePage, u"Routes")

        self.verticalLayout.addWidget(self.toolBox)


        self.retranslateUi(CompositeTileSourceConfigurationWidget)

        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(CompositeTileSourceConfigurationWidget)
    # setupUi

    def retranslateUi(self, CompositeTileSourceConfigurationWidget):
        CompositeTileSourceConfigurationWidget.setWindowTitle(QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"Form", None))
        self.addMark_button.setText("")
        self.removeMark_button.setText("")
        self.changeColor_button.setText("")
        self.test_button.setText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.markPage), QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"Marks", None))
        self.setRoad_button_2.setText("")
        self.removeRoad_button_2.setText("")
        self.test_button_3.setText("")
        self.test_button_2.setText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.routePage), QCoreApplication.translate("CompositeTileSourceConfigurationWidget", u"Routes", None))
    # retranslateUi

