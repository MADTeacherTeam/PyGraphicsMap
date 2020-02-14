from PySide2 import QtCore
from .MapGraphicsObject import MapGraphicsObject


class MapGraphicsScene(QtCore.QObject):
    objectAdded = QtCore.Signal(MapGraphicsObject)
    objectRemoved = QtCore.Signal(MapGraphicsObject)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.__objects = set()

    def addObject(self, object):
        if object == 0:
            return
        object.newObjectGenerated.connect(self.slot_handleNewObjectGenerated)
        object.destroyed.connect(self.slot_handleObjectDestroyed)

        self.__objects.add(object)
        self.objectAdded.emit(object)

    def removeObject(self, object):
        if object in self.__objects:
            self.__objects.remove(object)
            print('remove Object')
            self.objectRemoved.emit(object)

    def slot_handleNewObjectGenerated(self, newObject):
        print('handleNewObjectGenerated')
        self.addObject(newObject)

    def slot_handleObjectDestroyed(self, object):
        self.removeObject(object)

    def __del__(self):
        print("del MapGragphics scene")
        self.__objects.clear()
