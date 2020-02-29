from PySide2.QtWidgets import *
from MapGraphics.guts.PrivateQGraphicsObject import PrivateQGraphicsObject


class PrivateQGraphicsScene(QGraphicsScene):

    def __init__(self, mgScene, infoSource, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.__mgScene = None
        self.__infoSource = infoSource
        self.__mgToqg = {}
        self.__oldSelections = []
        self.setMapGraphicsScene(mgScene)

        self.selectionChanged.connect(self.handleSelectionChanged)
        self.counter = 0

    def handleMGObjectAdded(self, added):
        if added not in self.__mgToqg.keys():
            qgObj = PrivateQGraphicsObject(added, self.__infoSource)
            self.addItem(qgObj)
            self.__mgToqg[added] = qgObj

    def handleMGObjectRemoved(self, removed):
        if not self.__mgToqg.get(removed):
            print("There is no QGraphicsObject in the scene for")
            return

        qgObj = self.__mgToqg.pop(removed)

        if not self.items().__contains__(qgObj):
            print("does not contain PrivateQGraphicsObject")
            return
        qgObj.deleteLater()
        self.removeItem(qgObj)

    def handleZoomLevelChanged(self):
        for obj in self.__mgToqg:
            self.__mgToqg[obj].handleZoomLevelChanged()

    def handleSelectionChanged(self):
        selectedList = self.selectedItems()
        selected = []
        for item in selectedList:
            selected.append(item)

        newSelections = []
        for obj in self.__mgToqg:
            casted = QGraphicsItem(obj)
            doSelect = selected.__contains__(casted) and not self.__oldSelections.__contains__(obj)
            obj.setSelected(doSelect)

            if doSelect:
                newSelections.append(obj)

        self.__oldSelections = newSelections

    def setMapGraphicsScene(self, mgScene):
        self.__mgScene = mgScene

        if self.__mgScene is None:
            print("got a null MapGraphicsScene")
            return

        self.__mgScene.objectAdded.connect(self.handleMGObjectAdded)
        self.__mgScene.objectRemoved.connect(self.handleMGObjectRemoved)
