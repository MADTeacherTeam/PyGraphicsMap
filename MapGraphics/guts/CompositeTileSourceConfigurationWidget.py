from MapGraphics.guts.CompositeTileSourceConfigurationWidget_ui import Ui_CompositeTileSourceConfigurationWidget
from PySide2.QtWidgets import QWidget, QMenu
from PySide2.QtCore import Signal
from MapGraphics.MapGraphicsScene import MapGraphicsScene


class CompositeTileSourceConfigurationWidget(QWidget):
    # creationMode = Signal(MapGraphicsScene.ObjectCreationMode)

    def __init__(self, scene, parent=0):
        super().__init__(parent)
        self.__scene = scene
        self.ui = Ui_CompositeTileSourceConfigurationWidget()
        self.ui.setupUi(self)
        self.ui.addMark_button.clicked.connect(self.addMarkButtonClicked)
        # self.creationMode.connect(self.__scene.setCreationMode)

    def addMarkButtonClicked(self):
        if self.ui.addMark_button.isChecked():
            self.ui.removeMark_button.setChecked(False)
            # self.creationMode.emit(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.MarkCreation)
            self.__scene.createObject()
        else:
            self.__scene.setCreationMode(MapGraphicsScene.ObjectCreationMode.NoCreation)
            self.__scene.tempObj = None

    def removeMarkButtonClicked(self):
        pass

    def addRouteButtonClicked(self):
        pass

    def removeRouteButtonClicked(self):
        pass


