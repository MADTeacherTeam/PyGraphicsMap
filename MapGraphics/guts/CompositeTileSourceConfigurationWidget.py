from MapGraphics.guts.CompositeTileSourceConfigurationWidget_ui import Ui_CompositeTileSourceConfigurationWidget
from PySide2.QtWidgets import QWidget, QMenu
from PySide2.QtCore import Signal
from MapGraphics.MapGraphicsScene import MapGraphicsScene


class CompositeTileSourceConfigurationWidget(QWidget):
    # creationMode = Signal(MapGraphicsScene.ObjectCreationMode)

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
        # self.creationMode.connect(self.__scene.setCreationMode)

    def addMarkButtonClicked(self):
        if self.ui.addMark_button.isChecked():
            self.ui.moveMark_button.setChecked(False)
            self.ui.removeMark_button.setChecked(False)
            self.ui.changeColor_button.setChecked(False)
            # self.creationMode.emit(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.createObject()
        else:
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.tempObj.setVisible(False)
            self.__scene.tempObj = None

    def removeMarkButtonClicked(self):
        if self.__scene.tempObj:
            self.__scene.tempObj.setVisible(False)
            self.__scene.tempObj = None
        if self.ui.removeMark_button.isChecked():
            self.ui.addMark_button.setChecked(False)
            self.ui.moveMark_button.setChecked(False)
            self.ui.changeColor_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.MarkRemove)
        pass

    def changeColorButtonClicked(self):
        if self.ui.changeColor_button.isChecked():
            self.ui.addMark_button.setChecked(False)
            self.ui.moveMark_button.setChecked(False)
            self.ui.removeMark_button.setChecked(False)
        pass

    def moveMarkButtonClicked(self):
        from MapGraphics.Objects.MarkObject import MarkObject
        if self.__scene.tempObj:
            self.__scene.tempObj.setVisible(False)
            self.__scene.tempObj = None
        if self.ui.moveMark_button.isChecked():
            self.ui.addMark_button.setChecked(False)
            self.ui.removeMark_button.setChecked(False)
            self.ui.changeColor_button.setChecked(False)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.setObjectMovable(MarkObject.__name__)
        else:
            self.__scene.setObjectMovable(MarkObject.__name__, False)

    def addRouteButtonClicked(self):
        if self.ui.addRoute_button.isChecked():
            self.ui.removeRoute_button.setChecked(False)
            # self.creationMode.emit(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.RouteCreation)
            self.__scene.createObject()
        else:
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.tempObj.setVisible(False)
            self.__scene.tempObj = None

    def removeRouteButtonClicked(self):
        pass


