from ..MapTileSource import MapTileSource
from math import log, tan, atan, sinh
from PyQt5.QtCore import qDebug, QPointF, Qt
from PyQt5.QtGui import QImage, qRgba, QPainter

PI = 3.14159265358979323846
deg2rad = PI / 180.0
rad2deg = 180.0 / PI


class GridTileSource(MapTileSource):
    def __init__(self):
        super().__init__()
        self.setCacheMode(MapTileSource.CacheMode.NoCaching)

    def __del__(self):
        qDebug(self, "destructing")

    def ll2qgs(self, ll, zoomLevel):
        tilesOnOneEdge = pow(2, zoomLevel)
        tileSize = self.tileSize()
        x = (ll.x() + 180.0) * (tilesOnOneEdge * tileSize) / 360.0
        y = (1 - (log(tan(PI / 4.0 + (ll.y() * deg2rad) / 2)) / PI)) / 2.0 * (tilesOnOneEdge * tileSize)
        return QPointF(int(x), int(y))

    def qgs2ll(self, qgs, zoomLevel):
        tilesOnOneEdge = pow(2.0, zoomLevel)
        tileSize = self.tileSize()
        longitude = (qgs.x() * (360.0 / (tilesOnOneEdge * tileSize))) - 180.0
        latitude = rad2deg * (atan(sinh((1.0 - qgs.y() * (2.0 / (tilesOnOneEdge * tileSize))) * PI)))
        return QPointF(longitude, latitude)

    def tilesOnZoomLevel(self, zoomLevel):
        return pow(4.0, zoomLevel)

    def minZoomLevel(self, ll):
        return 0

    def maxZoomLevel(self, ll):
        return 50

    def name(self):
        return "Grid Tiles"

    def tileFileExtension(self):
        return ".png"

    def fetchTile(self, x, y, z):
        leftScenePixel = x * self.tileSize()
        topScenePixel = y * self.tileSize()
        rightScenePixel = leftScenePixel + self.tileSize()
        bottomScenePixel = topScenePixel + self.tileSize()
        toRet = QImage(self.tileSize(), self.tileSize(), QImage.Format_ARGB32_Premultiplied)
        toRet.fill(qRgba(0, 0, 0, 0))
        painter = QPainter(toRet)
        painter.setPen(Qt.black)
        everyNDegrees = 10.0
        # Longitude
        for lon in range(-180, 180, everyNDegrees):
            geoPos = QPointF(lon, 0)
            qgsScenePos = self.ll2qgs(geoPos, z)
            if qgsScenePos.x() < leftScenePixel or qgsScenePos.x() > rightScenePixel:
                continue
            painter.drawLine(qgsScenePos.x() - leftScenePixel, 0, qgsScenePos.x() - leftScenePixel, self.tileSize())
        # Latitude

        for lat in range(-90, 90, everyNDegrees):
            geoPos = QPointF(0, lat)
            qgsScenePos = self.ll2qgs(geoPos, z)
            if (qgsScenePos.y() < topScenePixel or qgsScenePos.y() > bottomScenePixel):
                continue
            painter.drawLine(0, qgsScenePos.y() - topScenePixel, self.tileSize(), qgsScenePos.y() - topScenePixel)

        painter.end()
        self._prepareNewlyReceivedTile(x, y, z, toRet)

    def tileSize(self):
        return 256
