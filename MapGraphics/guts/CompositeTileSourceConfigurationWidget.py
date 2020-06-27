from MapGraphics.guts.CompositeTileSourceConfigurationWidget_ui import Ui_CompositeTileSourceConfigurationWidget
from PySide2.QtWidgets import QWidget, QMenu, QColorDialog
from PySide2.QtCore import Signal
from MapGraphics.MapGraphicsScene import MapGraphicsScene


class CompositeTileSourceConfigurationWidget(QWidget):

    def __init__(self, scene:MapGraphicsScene, parent=0):
        super().__init__(parent)
        self.__scene = scene
        self.ui = Ui_CompositeTileSourceConfigurationWidget()
        self.ui.setupUi(self)
        self.ui.addMark_button.clicked.connect(self.addMarkButtonClicked)
        self.ui.removeMark_button.clicked.connect(self.removeMarkButtonClicked)
        self.ui.changeColor_button.clicked.connect(self.changeColorButtonClicked)
        self.ui.moveMark_button.clicked.connect(self.moveMarkButtonClicked)

        self.ui.addRoute_button.clicked.connect(self.addRouteButtonClicked)
        self.ui.removeRoute_button.clicked.connect(self.removeRouteButtonClicked)

        self.ui.toolBox.currentChanged.connect(self.clearToolBoxButtons)

    def clearToolBoxButtons(self, index):
        self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
        self.__scene.clearTempObject(True)

    def addMarkButtonClicked(self):
        """clicked button add Mark"""
        if self.ui.addMark_button.isChecked():
            self.ui.moveMark_button.setChecked(False)
            self.ui.removeMark_button.setChecked(False)
            # self.ui.changeColor_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.createObject()
        else:
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.clearTempObject(True)

    def removeMarkButtonClicked(self):
        """clicked button remove Mark"""
        self.__scene.clearTempObject(True)
        if self.ui.removeMark_button.isChecked():
            self.ui.addMark_button.setChecked(False)
            self.ui.moveMark_button.setChecked(False)
            # self.ui.changeColor_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.MarkRemove)
        pass

    def changeColorButtonClicked(self):
        """clicked button change color of Mark"""
        # if self.ui.changeColor_button.isChecked():
            # self.ui.addMark_button.setChecked(False)
            # self.ui.moveMark_button.setChecked(False)
            # self.ui.removeMark_button.setChecked(False)
            # color = QColorDialog.getColor()
        from MapGraphics.Objects.MarkObject import MarkObject
        if isinstance(self.__scene.tempObj, MarkObject):
            import random
            self.__scene.tempObj.changeImage(random.randint(0, 2))
            # if not color:
            #     self.ui.changeColor_button.setChecked(False)
            #     return
        pass

    def moveMarkButtonClicked(self):
        """clicked button move Mark"""
        from MapGraphics.Objects.MarkObject import MarkObject
        self.__scene.clearTempObject(True)
        if self.ui.moveMark_button.isChecked():
            self.ui.addMark_button.setChecked(False)
            self.ui.removeMark_button.setChecked(False)
            # self.ui.changeColor_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.setObjectMovable(MarkObject.__name__)
        else:
            self.__scene.setObjectMovable(MarkObject.__name__, False)

    def addRouteButtonClicked(self):
        """clicked button add Route"""
        if self.ui.addRoute_button.isChecked():
            self.ui.removeRoute_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.RouteCreation)
            self.__scene.createObject()
        else:
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.clearTempObject(True)

    def removeRouteButtonClicked(self):
        """clicked button remove Route"""
        self.__scene.clearTempObject(True)
        if self.ui.removeRoute_button.isChecked():
            self.ui.addRoute_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.RouteRemove)



