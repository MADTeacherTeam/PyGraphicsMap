import sys

from PySide2 import QtWidgets
from PySide2.QtCore import QObject, QThread, Signal

from MainApp.MainWindow import Ui_MainWindow
from MapGraphics.MapGraphicsScene import MapGraphicsScene
from MapGraphics.MapGraphicsView import MapGraphicsView
from MapGraphics.tileSources.OSMTileSource import OSMTileSource
from MainApp.PlaneManager import PlaneManager
import threading


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
        self.view.setZoomLevel(4)
        self.view.centerOn2(-111.658752, 40.255456)

        self.__thread_for_planes = QThread()
        self.__thread_for_planes.setObjectName('Zapor keka')
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
