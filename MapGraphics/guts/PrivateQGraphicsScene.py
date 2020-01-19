from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MapGraphics.guts.PrivateQGraphicsObject import PrivateQGraphicsObject


class PrivateQGraphicsScene(QGraphicsScene):
    def __init__(self, mgScene, infoSource, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.__mgScene = None
        self.__infoSource = infoSource  # мб конструктор
        self.__mgToqg = {}
        self.__oldSelections = []
        self.setMapGraphicsScene(mgScene)

        # connect(this,
        #         SIGNAL(selectionChanged()),
        #         this,
        #         SLOT(handleSelectionChanged()));

    def handleMGObjectAdded(self, added):
        qgObj = PrivateQGraphicsObject(added, self.__infoSource)
        self.addItem(qgObj)
        self.__mgToqg[added] = qgObj

    def handleMGObjectRemoved(self, removed):
        if not self.__mgToqg.get(removed):
            qWarning("There is no QGraphicsObject in the scene for")
            return

        qgObj = QGraphicsObject(self.__mgToqg.pop(removed))

        # if not self.items().__contains__(qgObj):
        #     qWarning("does not contain PrivateQGraphicsObject")
        #     return
        # qgObj.deleteLater()
        # self.removeItem(qgObj)

    def handleZoomLevelChanged(self):
        for obj in self.__mgToqg:
            obj.handleZoomLevelChanged()

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
            qWarning("got a null MapGraphicsScene")
            return

        # connect(_mgScene.data(),
        #         SIGNAL(objectAdded(MapGraphicsObject *)),
        #         this,
        #         SLOT(handleMGObjectAdded(MapGraphicsObject *)));
        # connect(_mgScene.data(),
        #         SIGNAL(objectRemoved(MapGraphicsObject *)),
        #         this,
        #         SLOT(handleMGObjectRemoved(MapGraphicsObject *)));
