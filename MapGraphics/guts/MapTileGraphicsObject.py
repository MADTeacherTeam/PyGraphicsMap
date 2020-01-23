from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QRectF, qWarning
from MapGraphics.MapTileSource import MapTileSource


class MapTileGraphicsObject(QGraphicsObject):
    tileRequested = Signal(int, int, int)
    tileRetrieved = Signal(int, int, int)
    allTilesInvalidated = Signal()

    def __init__(self, tileSize=256):
        QGraphicsObject.__init__(self)
        self.__tileSize = None
        self.__tile = None
        self.__tileX = 0
        self.__tileY = 0
        self.__tileZoom = 0
        self.__initialized = False
        self.__havePendingRequest = False
        self.__tileSource = MapTileSource()

        self.setTileSize(tileSize)
        self.setZValue(-1.0)

    def __del__(self):
        if self.__tile != 0:
            self.__tile = 0

    def boundingRect(self):
        size = self.tileSize()
        return QRectF(-1 * size / 2.0,
                      -1 * size / 2.0,
                      size,
                      size)

    def paint(self, painter, option, widget=None):
        if self.__tile != 0:
            painter.drawPixmap(self.boundingRect().toRect(), self.__tile)
        else:
            string = None
            if self.__tileSource is None:
                string = " No tile source defined"
            else:
                string = " Loading..."
                painter.drawText(self.boundingRect(), string, QTextOption(Qt.AlignCenter))

    def tileSize(self):
        return self.__tileSize

    def setTileSize(self, tileSize):
        if tileSize == self.__tileSize:
            return
        self.__tileSize = tileSize

    def setTile(self, x, y, z, force=False):
        if self.__tileX == x and self.__tileY == y and self.__tileZoom == z and not force and self.__initialized:
            return

        if self.__tile != 0:
            self.__tile = 0

        self.__tileX = x
        self.__tileY = y
        self.__tileZoom = z
        self.__initialized = True

        if self.__tileSource is None:
            return

        self.tileRetrieved.connect(self.handleTileRetrieved)
        # connect(_tileSource.data(),
        #         SIGNAL(tileRetrieved(quint32, quint32, quint8)),
        #         this,
        #         SLOT(handleTileRetrieved(quint32, quint32, quint8)))

        self.__havePendingRequest = True
        self.__tileSource.requestTile(x, y, z)

    def tileSource(self):
        return self.__tileSource

    def setTileSource(self, nSource):
        if not self.__tileSource is None:
            pass

        # self.tileRetrieved.disconnect(self.handleTileRetrieved)
        # self.tileRetrieved.disconnect(self.handleTileInvalidation)


        # QObject::disconnect(_tileSource.data(),
        #                     SIGNAL(tileRetrieved(quint32, quint32, quint8)),
        #                     this,
        #                     SLOT(handleTileRetrieved(quint32, quint32, quint8)))
        # QObject::disconnect(_tileSource.data(),
        #                     SIGNAL(allTilesInvalidated()),
        #                     this,
        #                     SLOT(handleTileInvalidation()))

        oldSource = self.__tileSource
        self.__tileSource = nSource

        if not self.__tileSource is None:
            pass

        self.allTilesInvalidated.connect(self.handleTileInvalidation)
        # connect(_tileSource.data(),
        #         SIGNAL(allTilesInvalidated()),
        #         this,
        #         SLOT(handleTileInvalidation()))

        self.handleTileInvalidation()

    # slots
    def handleTileRetrieved(self, x, y, z):
        if not self.__havePendingRequest:
            return
        elif self.__tileX != x or self.__tileY != y or self.__tileZoom != z:
            return

        self.__havePendingRequest = False

        if self.__tileSource is None:
            return

        image = QImage(self.__tileSource.getFinishedTile(x, y, z))

        if image == 0:
            print("Failed to get tile " + x + y + z + " from MapTileSource")
            return

        tile = QPixmap()
        tile = QPixmap.fromImage(image)

        image = 0

        if self.__tile != 0:
            print("Tile should be null, but isn't")
            self.__tile = 0

        self.__tile = tile
        self.update()

        self.tileRetrieved.disconnect(self.handleTileRetrieved)
        # QObject::disconnect(_tileSource.data(),
        #                     SIGNAL(tileRetrieved(quint32, quint32, quint8)),
        #                     this,
        #                     SLOT(handleTileRetrieved(quint32, quint32, quint8)));

    def handleTileInvalidation(self):
        if self.__initialized:
            return
        self.setTile(self.__tileX, self.__tileY, self.__tileZoom, True)
