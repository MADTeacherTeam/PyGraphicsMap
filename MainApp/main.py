import sys

from PySide2 import QtWidgets
from PySide2.QtCore import QObject

from MainApp.MainWindow import Ui_MainWindow
from MapGraphics.MapGraphicsScene import MapGraphicsScene
from MapGraphics.MapGraphicsView import MapGraphicsView
from MapGraphics.tileSources.OSMTileSource import OSMTileSource


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        scene = MapGraphicsScene(self)
        view = MapGraphicsView(scene, self)

        self.setCentralWidget(view)
        osmTiles = OSMTileSource(OSMTileSource.OSMTileType.OSMTiles)
        view.setTileSource(osmTiles)

        self.ui.menuWindows.addAction(self.ui.dockWidget.toggleViewAction())
        self.ui.dockWidget.toggleViewAction().setText("&Layers")

        view.setZoomLevel(4)
        view.centerOn2(-111.658752, 40.255456)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec_())
