from ..MapTileSource import MapTileSource
from PyQt5.QtCore import QMutex, qDebug, QMutexLocker, qWarning, QPointF, Qt
from PyQt5.QtGui import QImage, QPainter, QTextOption


class CompositeTileSource(MapTileSource):
    def __init__(self):
        super.__init__()
        self.__childSources = []
        self.__childOpacities = []
        self.__childEnabledFlags = []
        self.__pendingTiles = {}
        self.__globalMutex = QMutex(QMutex.Recursive)
        self.setCacheMode(MapTileSource.CacheMode.NoCaching)

    def __del__(self):
        self.__globalMutex.lock()
        qDebug(self, "destructing")
        self.clearPendingTiles()
        tileSourceThreads = []
        for source in self.__childSources:
            tileSourceThreads.append(source.thread())
        self.__childSources.clear()
        numThreads = len(tileSourceThreads)
        for i in range(0, numThreads):
            thread = tileSourceThreads[i]
            thread.wait(10000)
        self.__globalMutex.unlock()

    def ll2qgs(self, ll, zoomLevel):
        lock = QMutexLocker(self.__globalMutex)
        if not self.__childSources:
            qWarning("Composite tile source is empty --- results undefined")
            return QPointF(0, 0)
        return self.__childSources[0].ll2qgs(ll, zoomLevel)

    def qgs2ll(self, qgs, zoomLevel):
        lock = QMutexLocker(self.__globalMutex)
        if not self.__childSources:
            qWarning("Composite tile source is empty --- results undefined")
            return QPointF(0, 0)
        return self.___childSources[0].qgs2ll(qgs, zoomLevel)

    def tilesOnZoomLevel(self, zoomLevel):
        lock = QMutexLocker(self.__globalMutex)
        if not self.__childSources:
            return 1
        else:
            return self.__childSources[0].tilesOnZoomLevel(zoomLevel)

    def tileSize(self):
        lock = QMutexLocker(self.__globalMutex)
        if not self.__childSources:
            return 256
        else:
            return self.__childSources[0].tileSize()

    def minZoomLevel(self, ll):
        lock = QMutexLocker(self.__globalMutex)
        highest = 0
        for source in self.__childSources:
            current = source.minZoomLevel(ll)
            if (current > highest):
                highest = current
        return highest

    def maxZoomLevel(self, ll):
        lock = QMutexLocker(self.__globalMutex)
        lowest = 50
        for source in self.__childSources:
            current = source.maxZoomLevel(ll)
            if (current < lowest):
                lowest = current
        return lowest

    def name(self):
        return "Composite Tile Source"

    def tileFileExtension(self):
        return ".jpg"

    def addSourceTop(self, source, opacity):
        lock = QMutexLocker(self.__globalMutex)
        if not source:
            return
        self.doChildThreading(source)
        self.__childSources.insert(0, source)
        self.__childOpacities.insert(0, opacity)
        self.__childEnabledFlags.insert(0, True)
        # connect(source.data(),SIGNAL(tileRetrieved(quint32,quint32,quint8)),this,SLOT(handleTileRetrieved(quint32,quint32,quint8)));
        # SINAL sourceAdded(0) sourcesChanged allTilesInvalidated

    def addSourceBottom(self, source, opacity):
        lock = QMutexLocker(self.__globalMutex)
        if not source:
            return
        self.doChildThreading(source)
        self.__childSources.append(source)
        self.__childOpacities.append(opacity)
        self.__childEnabledFlags.append(True)
        # connect(source.data(), SIGNAL(tileRetrieved(quint32,quint32,quint8)),this,SLOT(handleTileRetrieved(quint32,quint32,quint8)))
        # SINAL sourceAdded(0) sourcesChanged allTilesInvalidated

    def moveSource(self, From, to):
        if From < 0 or to < 0:
            return
        lock = QMutexLocker(self.__globalMutex)
        size = self.numSources()
        if From >= size or to >= size:
            return
        self.__childSources[From], self.__childSources[to] = self.__childSources[to], self.__childSources[From]
        self.__childOpacities[From], self.__childOpacities[to] = self.__childOpacities[to], self.__childOpacities[From]
        self.__childEnabledFlags[From], self.__childEnabledFlags[to] = self.__childEnabledFlags[to], \
                                                                       self.__childEnabledFlags[From]
        # SINAL sourceAdded(0) sourcesChanged allTilesInvalidated

    def removeSource(self, index):
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return
        self.__childSources.pop(index)
        self.__childOpacities.pop(index)
        self.__childEnabledFlags.pop(index)
        self.clearPendingTiles()
        # SINAL sourceAdded(0) sourcesChanged allTilesInvalidated

    def clearPendingTiles(self):
        pass

    def numSources(self):
        lock = QMutexLocker(self.__globalMutex)
        return len(self.__childSources)

    def getSource(self, index):
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return MapTileSource()
        return self.__childSources[index]

    def getOpacity(self, index):
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return 0
        return self.__childOpacities[index]

    def setOpacity(self, index, opacity):
        opacity = min(1, max(0, opacity))
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return
        if self.__childOpacities == opacity:
            return
        self.__childOpacities[index] = opacity
        # SIGNAL sourcesChanged,allTilesInvalidated

    def getEnabledFlag(self, index):
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return 0
        return self.__childEnabledFlags[index]

    def setEnabledFlag(self, index, isEnabled):
        lock = QMutexLocker(self.__globalMutex)
        if index < 0 or index >= len(self.__childSources):
            return
        if self.__childEnabledFlags[index] == isEnabled:
            return
        self.__childEnabledFlags[index] = isEnabled
        # SIGNAL sourcesChanged,allTilesInvalidated

    def fetchTile(self, x, y, z):
        lock = QMutexLocker(self.__globalMutex)
        if not self.__childSources:
            toRet = QImage(self.tileSize(), self.tileSize(), QImage.Format_ARGB32_Premultiplied)
            painter = QPainter(toRet)
            painter.fillRect(toRet.rect(), Qt.white)
            painter.drawText(toRet.rect(), "Composite Source Empty", QTextOption(Qt.AlignCenter))
            painter.end()
            self._prepareNewlyReceivedTile(x, y, z, toRet)
            return
        cacheID = MapTileSource._createCacheID(x, y, z)
        if cacheID in self.__pendingTiles:
            tiles = self.__pendingTiles[cacheID]
            tiles.clear()
        else:
            self.__pendingTiles[cacheID] = {}
            for i in range(len(self.__childSources)):
                child = self.__childSources[i]
                child.requestTile(x, y, z)

    def doChildThreading(self, source):
        pass

    def clearPendingTiles(self):
        pass
