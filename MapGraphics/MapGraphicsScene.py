from PySide2 import QtCore
from .MapGraphicsObject import MapGraphicsObject
from enum import Enum
from .Objects.MarkObject import MarkObject
from .Objects.CircleObject import CircleObject
from .Objects.RouteObject import RouteObject
from .Objects.LineObject import LineObject
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
        self.__objects = {CircleObject.__name__: [],
                          LineObject.__name__: [],
                          MarkObject.__name__: [],
                          RouteObject.__name__: []}
        self.__creationMode = MapGraphicsScene.ObjectCreationMode.NoCreation
        self.tempObj = None

    def addObject(self, object):

        if object == 0 or object in self.__objects[object.__class__.__name__]:
            return

        object.newObjectGenerated.connect(self.handleNewObjectGenerated)
        # object.destroyed.connect(self.handleObjectDestroyed)

        object.removeRequested.connect(self.deleteObject)

        self.__objects[object.__class__.__name__].append(object)
        self.objectAdded.emit(object)

    def removeObject(self, object):
        if object in self.__objects[object.__class__.__name__]:
            self.__objects[object.__class__.__name__].remove(object)
            print('remove Object')
            self.objectRemoved.emit(object)

    def handleNewObjectGenerated(self, newObject):
        print('handleNewObjectGenerated')
        self.addObject(newObject)

    def handleObjectDestroyed(self, object):
        self.removeObject(object)

    def __del__(self):
        print("del MapGragphics scene")
        self.__objects.clear()

    def setCreationMode(self, mode):
        self.__creationMode = mode
        self.creationModeChanged.emit(self.__creationMode)

    def getCreationMode(self):
        return self.__creationMode

    def getObjects(self):
        return self.__objects

    def createObject(self, obj=None):
        if self.__creationMode == MapGraphicsScene.ObjectCreationMode.MarkCreation:
            self.tempObj = MarkObject()
            self.objectAdded.emit(self.tempObj)
        elif self.__creationMode == MapGraphicsScene.ObjectCreationMode.RouteCreation:
            self.tempObj = RouteObject(obj)
            # self.tempObj.newObjectGenerated.connect(self.handleNewObjectGenerated)
            self.objectAdded.emit(self.tempObj)
        else:
            self.clearTempObject()

    def deleteObject(self, object):
        if self.__creationMode == MapGraphicsScene.ObjectCreationMode.MarkRemove:
            if isinstance(object, MarkObject):
                # object.setVisible(False)
                self.removeObject(object)
        elif self.__creationMode == MapGraphicsScene.ObjectCreationMode.RouteRemove:
            self.removeObject(object.posBegin())
            self.removeObject(object.posEnd())
            self.removeObject(object)

    def setObjectMovable(self, type, flag=True):
        for obj in self.__objects[type]:
            obj.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, flag)

    def clearTempObject(self, fromWidget=False):
        if self.tempObj:
            if fromWidget:
                self.objectRemoved.emit(self.tempObj)
            self.tempObj = None
