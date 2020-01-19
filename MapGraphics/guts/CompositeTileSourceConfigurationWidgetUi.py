# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CompositeTileSourceConfigurationWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompositeTileSourceConfigurationWidget(object):
    def setupUi(self, CompositeTileSourceConfigurationWidget):
        CompositeTileSourceConfigurationWidget.setObjectName("CompositeTileSourceConfigurationWidget")
        CompositeTileSourceConfigurationWidget.resize(393, 343)
        self.verticalLayout = QtWidgets.QVBoxLayout(CompositeTileSourceConfigurationWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addSourceButton = QtWidgets.QToolButton(CompositeTileSourceConfigurationWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/edit_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addSourceButton.setIcon(icon)
        self.addSourceButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.addSourceButton.setObjectName("addSourceButton")
        self.horizontalLayout.addWidget(self.addSourceButton)
        self.removeSourceButton = QtWidgets.QToolButton(CompositeTileSourceConfigurationWidget)
        self.removeSourceButton.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/editdelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeSourceButton.setIcon(icon1)
        self.removeSourceButton.setObjectName("removeSourceButton")
        self.horizontalLayout.addWidget(self.removeSourceButton)
        self.moveDownButton = QtWidgets.QToolButton(CompositeTileSourceConfigurationWidget)
        self.moveDownButton.setEnabled(False)
        self.moveDownButton.setArrowType(QtCore.Qt.DownArrow)
        self.moveDownButton.setObjectName("moveDownButton")
        self.horizontalLayout.addWidget(self.moveDownButton)
        self.moveUpButton = QtWidgets.QToolButton(CompositeTileSourceConfigurationWidget)
        self.moveUpButton.setEnabled(False)
        self.moveUpButton.setArrowType(QtCore.Qt.UpArrow)
        self.moveUpButton.setObjectName("moveUpButton")
        self.horizontalLayout.addWidget(self.moveUpButton)
        self.opacitySlider = QtWidgets.QSlider(CompositeTileSourceConfigurationWidget)
        self.opacitySlider.setEnabled(False)
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setTracking(False)
        self.opacitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.opacitySlider.setObjectName("opacitySlider")
        self.horizontalLayout.addWidget(self.opacitySlider)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listView = QtWidgets.QListView(CompositeTileSourceConfigurationWidget)
        self.listView.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listView.setUniformItemSizes(True)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)

        self.retranslateUi(CompositeTileSourceConfigurationWidget)
        QtCore.QMetaObject.connectSlotsByName(CompositeTileSourceConfigurationWidget)

    def retranslateUi(self, CompositeTileSourceConfigurationWidget):
        _translate = QtCore.QCoreApplication.translate
        CompositeTileSourceConfigurationWidget.setWindowTitle(_translate("CompositeTileSourceConfigurationWidget", "Form"))
        self.addSourceButton.setText(_translate("CompositeTileSourceConfigurationWidget", "+"))
        self.removeSourceButton.setText(_translate("CompositeTileSourceConfigurationWidget", "X"))
        self.moveDownButton.setText(_translate("CompositeTileSourceConfigurationWidget", "D"))
        self.moveUpButton.setText(_translate("CompositeTileSourceConfigurationWidget", "U"))
import resources_rc
