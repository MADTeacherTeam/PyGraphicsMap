from PySide2.QtCore import Signal, QRectF
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class MapTileGraphicsObject(QGraphicsObject):
    tileRequested = Signal(int, int, int)

    def __init__(self, tileSize=256):
        QGraphicsObject.__init__(self)
        self.__tileSize = None
        self.__tile = None
        self.__tileX = 0
        self.__tileY = 0
        self.__tileZoom = 0
        self.__initialized = False
        self.__havePendingRequest = False
        self.__tileSource = None

        self.setTileSize(tileSize)
        self.setZValue(-1.0)

    def __del__(self):
        if self.__tile != 0:
            self.__tile = 0

    def boundingRect(self):
        """return bounding rectangle"""
        size = self.tileSize()
        return QRectF(-1 * size / 2.0,
                      -1 * size / 2.0,
                      size,
                      size)

    def paint(self, painter, option, widget=None):
        """override Paint"""
        if self.__tile != 0:
            painter.drawPixmap(self.boundingRect().toRect(), self.__tile)
        else:
            if self.__tileSource is None:
                string = " No tile source defined"
            else:
                string = " Loading..."
            painter.drawText(self.boundingRect(), string, QTextOption(Qt.AlignCenter))

    def tileSize(self):
        """return tileSize"""
        return self.__tileSize

    def setTileSize(self, tileSize):
        if tileSize == self.__tileSize:
            return
        self.__tileSize = tileSize

    def setTile(self, x, y, z, force=False):
        """set Tile about x,y,z"""
        # return if tile is already displaying
        if self.__tileX == x and self.__tileY == y and self.__tileZoom == z and not force and self.__initialized:
            return
        # delete old Tile
        if self.__tile != 0:
            self.__tile = 0

        self.__tileX = x
        self.__tileY = y
        self.__tileZoom = z
        self.__initialized = True

        if self.__tileSource is None:
            return

        self.__tileSource.tileRetrieved.connect(self.handleTileRetrieved)

        self.__havePendingRequest = True
        self.__tileSource.requestTile(x, y, z)

    def tileSource(self):
        """return tileSource"""
        return self.__tileSource

    def setTileSource(self, nSource):
        self.__tileSource = nSource

        if not self.__tileSource is None:
            self.__tileSource.allTilesInvalidated.connect(self.handleTileInvalidation)

        self.handleTileInvalidation()

    def handleTileRetrieved(self, x, y, z):
        """handle Tile by coordinates"""
        if not self.__havePendingRequest:
            return
        elif self.__tileX != x or self.__tileY != y or self.__tileZoom != z:
            return

        self.__havePendingRequest = False

        if self.__tileSource is None:
            return

        image = self.__tileSource.getFinishedTile(x, y, z)

        if image == 0:
            print("Failed to get tile " + x + y + z + " from MapTileSource")
            return

        tile = QPixmap.fromImage(image)

        image = 0

        if self.__tile != 0:
            print("Tile should be null, but isn't")
            self.__tile = 0

        self.__tile = tile
        self.update()

    def handleTileInvalidation(self):
        """call Tile invalidation"""
        if self.__initialized:
            return
        self.setTile(self.__tileX, self.__tileY, self.__tileZoom, True)
