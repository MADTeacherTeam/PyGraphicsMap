import math
from enum import Enum

from PySide2.QtCore import QPointF, QUrl, QDateTime, QRegExp, QByteArray
from PySide2.QtGui import QImage
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply

from MapGraphics.guts.MapGraphicsNetwork import MapGraphicsNetwork
from ..MapTileSource import MapTileSource

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

        self.__instances = {}
        self.setCacheMode(MapTileSource.CacheMode.DiskAndMemCaching)

    def __del__(self):
        super().__del__()
        MapTileSource.__del__(self)

    def name(self):
        """Return name of map graphics cache directory"""
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            return "OpenStreetMap Tiles"
        else:
            return "Unknown Tiles"

    def ll2qgs(self, ll, zoomLevel):
        """Converts longitude and latitude to QGraphicsScene coords"""
        tilesOnOneEdge = pow(2, zoomLevel)
        tileSize = self.tileSize()
        x = (ll.x() + 180) * (tilesOnOneEdge * tileSize) / 360
        y = (1 - (math.log(math.tan(PI / 4 + (ll.y() * deg2rad) / 2)) / PI)) / 2 * (tilesOnOneEdge * tileSize)
        return QPointF(int(x), int(y))

    def qgs2ll(self, qgs, zoomLevel):
        """Converts QGraphicsScene coords to longitude and latitude"""
        tilesOnOneEdge = pow(2, zoomLevel)
        tileSize = self.tileSize()
        longitude = (qgs.x() * (360 / (tilesOnOneEdge * tileSize))) - 180
        latitude = rad2deg * (math.atan(math.sinh((1 - qgs.y() * (2 / (tilesOnOneEdge * tileSize))) * PI)))
        return QPointF(longitude, latitude)

    def tilesOnZoomLevel(self, zoomLevel):
        return pow(4, zoomLevel)

    def minZoomLevel(self, ll=QPointF()):
        return 0

    def maxZoomLevel(self, ll=QPointF()):
        return 18

    def tileSize(self):
        return 256

    def tileFileExtension(self):
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            return "png"
        else:
            return "jpg"

    def fetchTile(self, x, y, z):
        """Request OSM server to get tile of x,y,z pos"""
        network, self.__instances = MapGraphicsNetwork.getInstance(self.__instances)
        host = ""
        if self.__tileType == OSMTileSource.OSMTileType.OSMTiles:
            host = "http://b.tile.openstreetmap.org"
            url = "/%1/%2/%3.png"
        cacheID = self.createCacheID(x, y, z)
        if cacheID in self.__pendingRequests:
            return
        self.__pendingRequests.add(cacheID)
        fetchURL = "/" + str(z) + "/" + str(x) + "/" + str(y) + ".png"
        request = QNetworkRequest(QUrl(host + fetchURL))
        reply = network.get(request)
        self.__pendingReplies[reply] = cacheID

        reply.finished.connect(self.handleNetworkRequestFinished)

    def handleNetworkRequestFinished(self):
        """After request finished, we need to set expireTime of tile"""
        sender = self.sender()
        reply = sender
        if not isinstance(reply, QNetworkReply):
            print("QNetworkReply cast failure")
            return
        reply.deleteLater()
        if reply not in self.__pendingReplies:
            print("Unknown QNetworkReply")
            return
        cacheID = self.__pendingReplies[reply]
        self.__pendingRequests.remove(cacheID)
        if reply.error() != QNetworkReply.NoError:
            print("Network Error:" + reply.errorString())
            return
        x = [1]
        y = [1]
        z = [1]
        if not MapTileSource._cacheID2xyz(cacheID, x, y, z):
            print("Failed to convert cacheID" + cacheID + "back to xyz")
            return
        bytes = reply.readAll()
        image = QImage()
        if not image.loadFromData(bytes):
            print("Failed to make QImage from network bytes")
            return
        expireTime = QDateTime()
        if reply.hasRawHeader(QByteArray(b"Cache-Control")):
            cacheControl = reply.rawHeader(QByteArray(b"Cache-Control"))
            maxAgeFinder = QRegExp("max-age=(\\d+)")
            if maxAgeFinder.indexIn(str(cacheControl)) != -1:
                if maxAgeFinder.cap(1).isdigit():
                    delta = int(maxAgeFinder.cap(1))
                    if isinstance(delta, int):
                        expireTime = QDateTime.currentDateTimeUtc().addSecs(delta)

        self._prepareNewlyReceivedTile(x[0], y[0], z[0], image, expireTime)
