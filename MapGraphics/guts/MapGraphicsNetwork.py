from PySide2 import QtCore, QtGui, QtNetwork

DEFAULT_USER_AGENT = QtCore.QByteArray(b'MapGraphic')


# QHash<QThread *, MapGraphicsNetwork *> MapGraphicsNetwork::_instances = QHash<QThread *, MapGraphicsNetwork*>();
# QMutex MapGraphicsNetwork::_mutex;


class MapGraphicsNetwork:
    @staticmethod
    def getInstance(instances):
        """Write thread and MapGraphicsNetwork to current instances"""
        __instances = instances
        __mutex = QtCore.QMutex()
        lock = QtCore.QMutexLocker(__mutex)
        current = QtCore.QThread.currentThread()
        if current not in __instances:
            __instances[current] = MapGraphicsNetwork()
        return __instances.get(current), __instances

    def __del__(self):
        self.__manager = 0

    def get(self, request):
        """Get new request by QNetworkAccessManager, return: QNetworkReply"""
        request.setRawHeader(QtCore.QByteArray(b"User-Agent"), QtCore.QByteArray(self.__userAgent))
        toRet = self.__manager.get(request)
        return toRet

    def setUserAgent(self, agent):
        self.__userAgent = agent

    def userAgent(self):
        return self.__userAgent

    def __init__(self):
        self.__manager = QtNetwork.QNetworkAccessManager()
        self.__userAgent = QtCore.QByteArray()
        self.setUserAgent(DEFAULT_USER_AGENT)
