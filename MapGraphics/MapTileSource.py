from PySide2 import QtCore
from PySide2.QtGui import QImage
from enum import Enum
import numpy as np

MAPGRAPHICS_CACHE_FOLDER_NAME = ".MapGraphicsCache"
DEFAULT_CACHE_DAYS = 7
MAX_DISK_CACHE_READ_ATTEMPTS = 100000


class MapTileSource(QtCore.QObject):
    # SIGNALS
    tileRetrieved = QtCore.Signal(int, int, int)
    tileRequested = QtCore.Signal(int, int, int)
    allTilesInvalidated = QtCore.Signal()

    class CacheMode(Enum):
        NoCaching = 1
        DiskAndMemCaching = 2

    def __init__(self):
        super(MapTileSource, self).__init__()
        self.__cacheExpirationsFile = ""
        self.__tempCacheLock = QtCore.QMutex()
        self.__tempCache = {}
        self.__memoryCache = {}
        self.__cacheExpirations = {}
        self.__cacheExpirationsLoaded = False
        self.setCacheMode(self.CacheMode.DiskAndMemCaching)

        self.tileRequested.connect(self.startTileRequest)
        self.allTilesInvalidated.connect(self.clearTempCache)

    def setCacheMode(self, nMode):
        self.__cacheMode = nMode

    def __del__(self):
        pass

    def saveCacheExpirationsToDisk(self):
        if (not self.__cacheExpirationsLoaded) or (not self.__cacheExpirationsFile):
            return
        fp = QtCore.QFile(self.__cacheExpirationsFile)
        if not fp.open(QtCore.QIODevice.Truncate | QtCore.QIODevice.WriteOnly):
            print("Failed to open cache expiration file for writing:")
            fp.errorString()
            return
        np.save(fp, self.__cacheExpirations)
        # stream = QtCore.QDataStream(fp)
        # for row in self.__cacheExpirations:
        #     forStream = self.__cacheExpirations[row].toString()
        #     stream << (row + ' ' + forStream + '\n')
        # stream << QtCore.QByteArray(self.__cacheExpirations)
        print("Cache expirations saved to " + self.__cacheExpirationsFile)

    def requestTile(self, x, y, z):
        self.tileRequested.emit(x, y, z)

    @staticmethod
    def createCacheID(x, y, z):
        toRet = str(x) + ',' + str(y) + ',' + str(z)
        return toRet

    def getFinishedTile(self, x, y, z):
        cacheID = self.createCacheID(x, y, z)
        lock = QtCore.QMutexLocker(self.__tempCacheLock)
        if not (cacheID in self.__tempCache):
            print("getFinishedTile() called, but the tile is not present")
            return 0
        return self.__tempCache[cacheID]

    def cacheMode(self):
        return self.__cacheMode

    def startTileRequest(self, x, y, z):
        if self.cacheMode() == self.CacheMode.DiskAndMemCaching:
            cacheID = self.createCacheID(x, y, z)
            cached = self._fromMemCache(cacheID)
            if not cached:
                cached = self._fromDiskCache(cacheID)
            if cached:
                self.__prepareRetrievedTile(x, y, z, cached)
                return
        self.fetchTile(x, y, z)

    def clearTempCache(self):
        self.__tempCache.clear()

    def _fromMemCache(self, cacheID):
        toRet = 0
        if cacheID in self.__memoryCache:
            expireTime = self._getTileExpirationTime(cacheID)
            # TODO fix expireTime comming empty _fromMemCache
            if not isinstance(expireTime, QtCore.QDateTime):
                print('Wrong type in fromMemCache, MapTileSource')
                return
            if QtCore.QDateTime.currentDateTime().secsTo(expireTime) <= 0:
                self.__memoryCache.pop(cacheID, None)
            else:
                toRet = QImage(self.__memoryCache.get(cacheID))
        return toRet

    def _fromDiskCache(self, cacheID):
        x = [1]
        y = [1]
        z = [1]
        if not self._cacheID2xyz(cacheID, x, y, z):
            return 0
        path = self.__getDiskCacheFile(x[0], y[0], z[0])
        fp = QtCore.QFile(path)
        if not fp.exists():
            return 0
        expireTime = self._getTileExpirationTime(cacheID)
        # TODO fix expireTime comming empty _fromDiskCache
        if not isinstance(expireTime, QtCore.QDateTime):
            print('Wrong type in fromDiskCache, MapTileSource')
            return
        if QtCore.QDateTime.currentDateTimeUtc().secsTo(expireTime) <= 0:
            if not QtCore.QFile.remove(path):
                print("Failed to remove old cache file" + path)
            return 0
        if not fp.open(QtCore.QFile.ReadOnly):
            print("Failed to open" + QtCore.QFileInfo(fp.fileName()).baseName() + "from cache")
            return 0
        counter = 0
        data = QtCore.QByteArray()
        while len(data) < fp.size():
            data += fp.read(20480)
            if counter + 1 >= MAX_DISK_CACHE_READ_ATTEMPTS:
                counter += 1
                print("Reading cache file" + fp.fileName() + "took too long. Aborting.")
                return 0
            else:
                counter += 1
        image = QImage()
        # Check load image
        if not image.loadFromData(data):
            return 0
        return image

    def __prepareRetrievedTile(self, x, y, z, image):
        if image == 0:
            return
        lock = QtCore.QMutexLocker(self.__tempCacheLock)
        self.__tempCache[self.createCacheID(x, y, z)] = image
        # for row in self.__tempCache:
        #     print(row)
        lock.unlock()
        self.tileRetrieved.emit(x, y, z)

    def fetchTile(self, x, y, z):
        pass

    @staticmethod
    def _cacheID2xyz(string, x, y, z):
        # All var is list for link,x,y,z=x[0],y[0],z[0]
        list = string.split(',')
        if len(list) != 3:
            print("Bad cacheID" + string + "cannot convert")
            return False
        ok = True
        x[0] = abs(int(list[0]))
        if not ok:
            return False
        y[0] = abs(int(list[1]))
        if not ok:
            return False
        z[0] = abs(int(list[2]))
        return ok

    def _getTileExpirationTime(self, cacheID):
        self.__loadCacheExpirationsFromDisk()
        if cacheID in self.__cacheExpirations:
            expireTime = self.__cacheExpirations.get(cacheID)
        else:
            print(
                "Tile " + str(cacheID) + " has unknown expire time. Resetting to default of " + str(DEFAULT_CACHE_DAYS)  + " days.")
            expireTime = QtCore.QDateTime.currentDateTimeUtc().addDays(DEFAULT_CACHE_DAYS)
            self.__cacheExpirations[cacheID] = expireTime
        return expireTime

    def _setTileExpirationTime(self, cacheID, expireTime):
        self.__loadCacheExpirationsFromDisk()
        if expireTime is None:
            expireTime = QtCore.QDateTime.currentDateTimeUtc().addDays(DEFAULT_CACHE_DAYS)
        self.__cacheExpirations[cacheID] = expireTime

    def _toMemCache(self, cacheID, toCache, expireTime):
        if toCache == 0:
            return
        if cacheID in self.__memoryCache:
            return
        self._setTileExpirationTime(cacheID, expireTime)
        copy = QImage(toCache)
        self.__memoryCache[cacheID] = copy

    def __getDiskCacheFile(self, x, y, z):
        toRet = self.__getDiskCacheDirectory(x, y, z).absolutePath() + "/" + str(y) + '.' + self.tileFileExtension()
        return toRet

    def _toDiskCache(self, cacheID, toCache, expireTime):
        x = [1]
        y = [1]
        z = [1]
        if not self._cacheID2xyz(cacheID, x, y, z):
            return
        filePath = self.__getDiskCacheFile(x[0], y[0], z[0])
        fp = QtCore.QFile(filePath)
        if fp.exists():
            return
        self._setTileExpirationTime(cacheID, expireTime)
        format = None
        quality = 100
        if not toCache.save(filePath, format, quality):
            print("Failed to put") #  + self.name() + str(x[0]) + str(y[0]) + str(z[0]) + "into disk cache"

    def name(self):
        pass

    def _prepareNewlyReceivedTile(self, x, y, z, image, expireTime=QtCore.QDateTime()):
        cacheID = self.createCacheID(x, y, z)
        if self.cacheMode() == self.CacheMode.DiskAndMemCaching:
            self._toMemCache(cacheID, image, expireTime)
            self._toDiskCache(cacheID, image, expireTime)
        self.__prepareRetrievedTile(x, y, z, image)

    def __loadCacheExpirationsFromDisk(self):
        if self.__cacheExpirationsLoaded:
            return
        self.__cacheExpirationsLoaded = True
        dir = self.__getDiskCacheDirectory(0, 0, 0)
        path = dir.absolutePath() + "/" + "cacheExpirations.db"
        self.__cacheExpirationsFile = path
        fp = QtCore.QFile(path)
        if not fp.exists():
            return
        if not fp.open(QtCore.QIODevice.ReadOnly):
            print("Failed to open cache expiration file for reading:" + fp.errorString())
            return
        self.__cacheExpirations = np.load(path, allow_pickle=True).item()
        # stream = QtCore.QDataStream(fp)
        # for row in self.__cacheExpirations:
        #     stream >> row
        # stream >> self.__cacheExpirations

    def __getDiskCacheDirectory(self, x, y, z):
        pathString = QtCore.QDir.homePath() + "/" + MAPGRAPHICS_CACHE_FOLDER_NAME + "/" + self.name() + "/" + str(
            z) + "/" + str(x)
        toRet = QtCore.QDir(pathString)
        if not toRet.exists():
            if not toRet.mkpath(toRet.absolutePath()):
                print("Failed to create cache directory" + toRet.absolutePath())
        return toRet

    def tileFileExtension(self):
        pass

    def minZoomLevel(self, ll=QtCore.QPointF()):
        pass

    def maxZoomLevel(self, ll=QtCore.QPointF()):
        pass
