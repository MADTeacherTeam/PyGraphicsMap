from PySide2 import QtCore
from .MapGraphicsObject import MapGraphicsObject
from enum import Enum
from .Objects.MarkObject import MarkObject
from .Objects.CircleObject import CircleObject
from .Objects.RouteObject import RouteObject
# from MapGraphics.MapGraphicsView import MapGraphicsView
import copy


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
        self.__objects = {}
        self.__creationMode = MapGraphicsScene.ObjectCreationMode.NoCreation
        self.tempObj = None

    def addObject(self, object):
        # if isinstance(object, RouteObject):
        #     self.__objects.add(object)
        #     self.objectAdded.emit(object)
        #
        #     self.tempObj = None
        #     self.createObject()
        #     return

        object = copy.copy(object)
        if object == 0:
            return

        object.newObjectGenerated.connect(self.slot_handleNewObjectGenerated)
        object.destroyed.connect(self.slot_handleObjectDestroyed)

        object.removeRequested.connect(self.deleteObject)

        if object.__class__.__name__ in self.__objects.keys():
            self.__objects[object.__class__.__name__].append(object)
        else:
            self.__objects[object.__class__.__name__] = [object]

        # self.__objects[object.__class__.__name__] = object
        self.objectAdded.emit(object)

        self.objectRemoved.emit(self.tempObj)
        self.tempObj = None
        self.createObject()

    def removeObject(self, object):
        if object in self.__objects[object.__class__.__name__]:
            self.__objects[object.__class__.__name__].remove(object)
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
            self.objectAdded.emit(self.tempObj)
        # elif self.__creationMode == MapGraphicsScene.ObjectCreationMode.RouteCreation:
        #     if self.tempObj is None:
        #         self.tempObj = []
        #     elif len(self.tempObj) >= 2:
        #         self.tempObj = RouteObject(self.tempObj[-2], self.tempObj[-1])
        #         self.addObject(self.tempObj)
        else:
            self.tempObj = None

    def deleteObject(self, object):
        if self.__creationMode == MapGraphicsScene.ObjectCreationMode.MarkRemove:
            if isinstance(object, MarkObject):
                # object.setVisible(False)
                self.removeObject(object)

    def setObjectMovable(self, type, flag=True):
        for obj in self.__objects[type]:
            obj.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, flag)

