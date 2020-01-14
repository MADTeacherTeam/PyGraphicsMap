from PyQt5 import QtCore, QtGui, QtNetwork

DEFAULT_USER_AGENT = QtCore.QByteArray(b'MapGraphic')

# QHash<QThread *, MapGraphicsNetwork *> MapGraphicsNetwork::_instances = QHash<QThread *, MapGraphicsNetwork*>();
# QMutex MapGraphicsNetwork::_mutex;


class MapGraphicsNetwork:
    def getInstance(self):
        lock = QtCore.QMutexLocker(self.__mutex)
        current = QtCore.QThread.currentThread()
        if current in self.__instances:
            self.__instances[current] = MapGraphicsNetwork()
        return self.__instances.get(current)

    def __del__(self):
        self.__manager = 0

    def get(self, request):
        request.setRawHeader("User-Agent", self.__userAgent)
        toRet = QtNetwork.QNetworkReply(self.__manager.get(request))
        return toRet

    def setUserAgent(self, agent):
        self.__userAgent = agent

    def userAgent(self):
        return self.__userAgent

    def __init__(self):
        self.__instances = {}
        self.__mutex = QtCore.QMutex()
        self.__manager = QtNetwork.QNetworkAccessManager()
        self.__userAgent = QtCore.QByteArray()
        self.setUserAgent(DEFAULT_USER_AGENT)