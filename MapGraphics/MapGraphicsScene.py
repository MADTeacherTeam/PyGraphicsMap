from PySide2 import QtCore
from .MapGraphicsObject import MapGraphicsObject
from enum import Enum
from .Objects.MarkObject import MarkObject
from .Objects.CircleObject import CircleObject
from .Objects.RouteObject import RouteObject
# from MapGraphics.MapGraphicsView import MapGraphicsView


class MapGraphicsScene(QtCore.QObject):
    objectAdded = QtCore.Signal(MapGraphicsObject)
    objectRemoved = QtCore.Signal(MapGraphicsObject)

    creationModeChanged = QtCore.Signal(object)

    class ObjectCreationMode(Enum):
        NoCreation = 0
        MarkCreation = 1
        RouteCreation = 2
        MarkRemove = 3
        RouteRemove = 4

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.__objects = set()
        self.__creationMode = MapGraphicsScene.ObjectCreationMode.NoCreation
        self.tempObj = None

    def addObject(self, object):
        if isinstance(object, RouteObject):
            self.__objects.add(object)
            self.objectAdded.emit(object)

            self.tempObj = None
            self.createObject()
            return

        if object == 0:
            return
        object.newObjectGenerated.connect(self.slot_handleNewObjectGenerated)
        object.destroyed.connect(self.slot_handleObjectDestroyed)

        self.__objects.add(object)
        self.objectAdded.emit(object)

        self.tempObj = None
        self.createObject()

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

    def setCreationMode(self, mode):
        self.__creationMode = mode
        self.creationModeChanged.emit(self.__creationMode)

    def getCreationMode(self):
        return self.__creationMode

    def createObject(self):
        if self.__creationMode == MapGraphicsScene.ObjectCreationMode.MarkCreation:
            self.tempObj = MarkObject()
        # elif self.__creationMode == MapGraphicsScene.ObjectCreationMode.RouteCreation:
        #     if self.tempObj is None:
        #         self.tempObj = []
        #     elif len(self.tempObj) == 2:
        #         self.tempObj = RouteObject(self.tempObj[0], self.tempObj[1])
        #         self.addObject(self.tempObj)
        else:
            self.tempObj = None
        pass
