from PyQt5 import QtCore
from .MapGraphicsObject import MapGraphicsObject


class MapGraphicsScene(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        # self.objects = []
        self.__objects = set()
        # SIGNALS
        self.objectAdded = QtCore.pyqtSignal(MapGraphicsObject)
        self.objectRemoved = QtCore.pyqtSignal(MapGraphicsObject)

    def addObject(self, object):
        if object == 0:
            return
        object.newObjectGenerated.connect(self.slot_handleNewObjectGenerated)
        object.destroyed.connect(self.slot_handleObjectDestroyed)
        self.__objects.add(object)
        print('add Object')
        self.objectAdded.emit(object)

    def removeObject(self, object):
        print('remove Object')
        self.__objects.remove(object)
        self.objectRemoved.emit(object)

    def slot_handleNewObjectGenerated(self, newObject):
        print('handleNewObjectGenerated')
        self.addObject(newObject)

    def slot_handleObjectDestroyed(self, object):
        self.removeObject(object)

    def __del__(self):
        self.__objects.clear()
