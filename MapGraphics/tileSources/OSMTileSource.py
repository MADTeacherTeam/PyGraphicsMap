from ..MapTileSource import MapTileSource
from enum import Enum
from PySide2.QtCore import qDebug, QPointF, QUrl, QObject, qWarning, QDateTime, QRegExp, Slot
from PySide2.QtGui import QImage
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply
import math
from MapGraphics.guts.MapGraphicsNetwork import MapGraphicsNetwork

PI = 3.14159265358979323846
deg2rad = PI / 180.0
rad2deg = 180.0 / PI


class OSMTileSource(MapTileSource):
    class OSMTileType(Enum):
        OSMTiles = 0x01

    def __init__(self, tileType):
        super(OSMTileSource, self).__init__()
        self.__tileType = None
        self.__pendingRequests = set()
        self.__pendingReplies = {}
        self.__tileType = tileType
        self.setCacheMode(MapTileSource.CacheMode.DiskAndMemCaching)

    def __del__(self):
        qDebug(b"Destructing OSMTileSource")

    def name(self):
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            return "OpenStreetMap Tiles"
        else:
            return "Unknown Tiles"

    def ll2qgs(self, ll, zoomLevel):
        tilesOnOneEdge = pow(2, zoomLevel)
        tileSize = self.tileSize()
        x = (ll.x() + 180) * (tilesOnOneEdge * tileSize) / 360
        y = (1 - (math.log(math.tan(PI / 4 + (ll.y() * deg2rad) / 2)) / PI)) / 2 * (tilesOnOneEdge * tileSize)
        return QPointF(int(x), int(y))

    def qgs2ll(self, qgs, zoomLevel):
        tilesOnOneEdge = pow(2, zoomLevel)
        tileSize = self.tileSize()
        longitude = (qgs.x() * (360 / (tilesOnOneEdge * tileSize))) - 180
        latitude = rad2deg * (math.atan(math.sinh((1 - qgs.y() * (2 / (tilesOnOneEdge * tileSize))) * PI)))
        return QPointF(longitude, latitude)

    def tilesOnZoomLevel(self, zoomLevel):
        return pow(4, zoomLevel)

    def minZoomLevel(self, ll):
        return 0

    def maxZoomLevel(self, ll):
        return 18

    def tileSize(self):
        return 256

    def tileFileExtension(self):
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            return "png"
        else:
            return "jpg"

    def fetchTile(self, x, y, z):
        network = MapGraphicsNetwork.getInstance()
        host = ""
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            host = "http://b.tile.openstreetmap.org"
            url = "/%1/%2/%3.png"
        cacheID = self._createCacheID(x, y, z)
        if cacheID in self.__pendingRequests:
            return
        self.__pendingRequests.add(cacheID)
        fetchURL = "/" + str(z) + "/" + str(x) + "/" + str(y) + ".png"
        request = QNetworkRequest(QUrl(host + fetchURL))
        reply = network.get(request)
        self.__pendingReplies[reply] = cacheID

        # SIGNAL connect(reply,IGNAL(finished()),this,SLOT(handleNetworkRequestFinished()))
        reply.finished.connect(self.handleNetworkRequestFinished)

    def handleNetworkRequestFinished(self):
        sender = self.sender()
        reply = sender
        if not isinstance(reply, QNetworkReply):
            qWarning(b"QNetworkReply cast failure")
            return
        reply.deleteLater()
        if reply not in self.__pendingReplies:
            qWarning(b"Unknown QNetworkReply")
            return
        cacheID = self.__pendingReplies[reply]
        self.__pendingRequests.remove(cacheID)
        if reply.error() != QNetworkReply.NoError:
            qDebug(b"Network Error:" + reply.errorString())
            return
        x = [1]
        y = [1]
        z = [1]
        if not MapTileSource._cacheID2xyz(cacheID, x, y, z):
            qWarning(b"Failed to convert cacheID" + cacheID + b"back to xyz")
            return
        bytes = reply.readAll()
        image = QImage()
        if not image.loadFromData(bytes):
            qWarning(b"Failed to make QImage from network bytes")
            return
        expireTime = QDateTime
        if reply.hasRawHeader("Cache-Control"):
            cacheControl = reply.rawHeader("Cache-Control")
            maxAgeFinder = QRegExp("max-age=(\\d+)")
            if maxAgeFinder.indexIn(cacheControl) != -1:
                ok = False
                # TODO toULongLong
                delta = maxAgeFinder.cap(1).toULongLong(ok)
                if ok:
                    QDateTime.currentDateTimeUtc().addSecs(delta)

        self._prepareNewlyReceivedTile(x, y, z, image, expireTime)
