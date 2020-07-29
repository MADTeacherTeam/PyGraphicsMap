import sys

from PySide2 import QtWidgets
from PySide2.QtCore import QObject, QThread, Signal

from ExampleApp.MainWindow_ui import Ui_MainWindow
from PyGraphicsMap.MapGraphicsScene import MapGraphicsScene
from PyGraphicsMap.MapGraphicsView import MapGraphicsView
from PyGraphicsMap.tileSources.OSMTileSource import OSMTileSource
from ExampleApp.PlaneManager import PlaneManager
from PyGraphicsMap.guts.CompositeTileSourceConfigurationWidget import CompositeTileSourceConfigurationWidget


class MyWindow(QtWidgets.QMainWindow):
    threadPlaneManager = Signal()

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(lambda: self.close())
        scene = MapGraphicsScene(self)
        self.view = MapGraphicsView(scene, self)

        self.setCentralWidget(self.view)
        osmTiles = OSMTileSource(OSMTileSource.OSMTileType.OSMTiles)

        self.view.setTileSource(osmTiles)
        self.view.setZoomLevel(10)
        self.view.centerOn2(30.3609, 59.9311)

        self.tileConfigWidget = CompositeTileSourceConfigurationWidget(scene, self.ui.dockWidget)
        self.ui.dockWidget.setWidget(self.tileConfigWidget)

        # Example how to connect planes to project
        self.__thread_for_planes = QThread()
        self.flight = PlaneManager(scene)
        self.__thread_for_planes.start()
        self.flight.moveToThread(self.__thread_for_planes)
        self.threadPlaneManager.connect(self.flight.createPlanes)
        self.__thread_for_planes.finished.connect(self.flight.deleteLater)
        self.threadPlaneManager.emit()

    def closeEvent(self, event):
        self.__closeThreads()
        super(QtWidgets.QMainWindow, self).closeEvent(event)

    def __closeThreads(self):
        self.__thread_for_planes.quit()
        self.__thread_for_planes.wait()
        self.view.stopViewThreads()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = MyWindow()
    application.show()
    sys.exit(app.exec_())
