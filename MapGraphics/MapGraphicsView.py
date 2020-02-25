from PySide2.QtCore import QTimer, qDebug, QCoreApplication, QPoint, QPointF, qWarning, Signal, QThread, QEventLoop
from PySide2.QtWidgets import QWidget, QGraphicsView, QVBoxLayout
from PySide2.QtGui import QCursor, QPolygonF, QPolygon
from .guts.MapTileGraphicsObject import MapTileGraphicsObject
from .guts.PrivateQGraphicsInfoSource import PrivateQGraphicsInfoSource
from .guts.PrivateQGraphicsScene import PrivateQGraphicsScene
from .guts.PrivateQGraphicsView import PrivateQGraphicsView
from enum import Enum
from queue import Queue
from math import sqrt, inf
from MapGraphics.Objects.MarkObject import MarkObject


class MapGraphicsView(QWidget):
    __metaclass__ = PrivateQGraphicsInfoSource
    zoomLevelChanged = Signal(int)

    class DragMode(Enum):
        NoDrag = 0
        ScrollHandDrag = 1
        RubberBandDrag = 2

    class ZoomMode(Enum):
        CenterZoom = 0
        MouseZoom = 1

    def __init__(self, scene=None, parent=None):
        QWidget.__init__(self, parent)
        self.__tileSource = None
        self.__dragMode = None
        self.tileSourceThread = QThread()
        self.tileSourceThread.start()
        self.__tileObjects = set()
        self.setScene(scene)
        self.__zoomLevel = 2
        self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)
        self.__tempCenterPointQGS = None

        QTimer.singleShot(1000, self.renderTiles)

        self.__scene.creationModeChanged.connect(self.setDragModeByScene)

    def __del__(self):
        print("Destructing MapGraphicsView")
        self.__tileObjects.clear()

    def stopViewThreads(self):
        if self.__tileSource:
            self.__tileSource.saveCacheExpirationsToDisk()
        self.tileSourceThread.quit()
        self.tileSourceThread.wait()

    def center(self):
        centerGeoPos = self.mapToScene(QPoint(int(self.width() / 2), int(self.height() / 2)))
        return centerGeoPos

    def centerOn(self, pos):
        if not self.__tileSource:
            return
        qgsPos = self.__tileSource.ll2qgs(pos, self.zoomLevel())
        self.__childView.centerOn(qgsPos)

    def centerOn2(self, longitude, latitude):
        self.centerOn(QPointF(longitude, latitude))

    def centerOn1(self, item):
        if item:
            self.centerOn(item.pos())

    def mapToScene(self, viewPos):
        if not self.__tileSource:
            print("No tile source --- Transformation cannot work")
            return QPointF(0, 0)
        qgsScenePos = self.__childView.mapToScene(viewPos)
        zoom = self.zoomLevel()
        return self.__tileSource.qgs2ll(qgsScenePos, zoom)

    def dragMode(self):
        return self.__dragMode

    def setDragMode(self, mode):
        self.__dragMode = mode
        if self.__dragMode == MapGraphicsView.DragMode.NoDrag:
            qgvDragMode = QGraphicsView.NoDrag
        elif self.__dragMode == MapGraphicsView.DragMode.ScrollHandDrag:
            qgvDragMode = QGraphicsView.ScrollHandDrag
        else:
            qgvDragMode = QGraphicsView.RubberBandDrag
        if not self.__childView:
            return
        self.__childView.setDragMode(qgvDragMode)

    def setDragModeByScene(self, mode):
        if mode == self.__scene.ObjectCreationMode.MarkCreation:
            self.setDragMode(MapGraphicsView.DragMode.NoDrag)
        elif mode == self.__scene.ObjectCreationMode.RouteCreation:
            self.setDragMode(MapGraphicsView.DragMode.NoDrag)
        elif mode == self.__scene.ObjectCreationMode.MarkRemove:
            self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)
        else:
            self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)

    def scene(self):
        return self.__scene

    def setScene(self, scene):
        childScene = PrivateQGraphicsScene(scene, self, self)
        self.zoomLevelChanged.connect(childScene.handleZoomLevelChanged)
        childView = PrivateQGraphicsView(self, childScene)
        childView.hadMouseDoubleClickEvent.connect(self.handleChildMouseDoubleClick)
        childView.hadMouseMoveEvent.connect(self.handleChildMouseMove)
        childView.hadMousePressEvent.connect(self.handleChildMousePress)
        childView.hadMouseReleaseEvent.connect(self.handleChildMouseRelease)
        childView.hadWheelEvent.connect(self.handleChildViewScrollWheel)
        childView.hadContextMenuEvent.connect(self.handleChildViewContextMenu)

        #########################################################################################################
        # if self.layout()!=0:
        # delete layout
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(childView)
        childView.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.__childView = childView
        self.__childScene = childScene
        self.__scene = scene

        self.resetQGSSceneSize()
        self.setDragMode(self.dragMode())
        self.renderTiles()

    def tileSource(self):
        return self.__tileSource

    def setTileSource(self, tSource):
        self.__tileSource = tSource
        if self.__tileSource:
            self.__tileSource.moveToThread(self.tileSourceThread)
            self.__tileSource.destroyed.connect(self.tileSourceThread.quit)
            self.tileSourceThread.finished.connect(self.tileSourceThread.deleteLater)
        for tileObject in self.__tileObjects:
            tileObject.setTileSource(tSource)

        self.renderTiles()

    def zoomLevel(self):
        return self.__zoomLevel

    def setZoomLevel(self, nZoom, zMode=ZoomMode.CenterZoom):
        if not self.__tileSource:
            return
        centerGeoPos = self.mapToScene(QPoint(int(self.width() / 2), int(self.height() / 2)))
        mousePoint = self.__childView.mapToScene(self.__childView.mapFromGlobal(QCursor.pos()))
        sceneRect = self.__childScene.sceneRect()
        try:
            xRatio = mousePoint.x() / sceneRect.width()
        except ZeroDivisionError:
            xRatio = inf
        try:
            yRatio = mousePoint.y() / sceneRect.height()
        except ZeroDivisionError:
            yRatio = inf
        centerPos = self.__childView.mapToScene(
            QPoint(int(self.__childView.width() / 2), int(self.__childView.height() / 2)))
        offset = mousePoint - centerPos
        nZoom = min(self.__tileSource.maxZoomLevel(), max(self.__tileSource.minZoomLevel(), nZoom))

        if self.__zoomLevel == nZoom:
            return
        self.__zoomLevel = nZoom
        for tileObject in self.__tileObjects:
            tileObject.setVisible(False)
        self.resetQGSSceneSize()

        sceneRect = self.__childScene.sceneRect()
        mousePoint = QPointF(sceneRect.width() * xRatio, sceneRect.height() * yRatio) - offset
        if zMode == MapGraphicsView.ZoomMode.MouseZoom:
            self.__childView.centerOn(mousePoint)
        else:
            self.centerOn(centerGeoPos)
        self.renderTiles()
        self.zoomLevelChanged.emit(nZoom)

    def zoomIn(self, zMode):
        if not self.__tileSource:
            return

        if self.zoomLevel() < self.__tileSource.maxZoomLevel():
            self.setZoomLevel(self.zoomLevel() + 1, zMode)

    def zoomOut(self, zMode):
        if not self.__tileSource:
            return

        if self.zoomLevel() > self.__tileSource.minZoomLevel():
            self.setZoomLevel(self.zoomLevel() - 1, zMode)

    def handleChildMouseDoubleClick(self, event):
        event.setAccepted(False)

    def handleChildMouseMove(self, event):
        if self.__scene.tempObj:
            mousePoint = self.mapToScene(self.__childView.mapFromGlobal(QCursor.pos()))
            self.__scene.tempObj.setPos(mousePoint)
            self.__scene.tempObj.setMark()
            # self.__scene.objectAdded.emit(self.__scene.tempObj)
        if self.__childView and self.__tileSource:
            centerPointQGS = self.__childView.mapToScene(int(self.__childView.width() / 2.0),
                                                         int(self.__childView.height() / 2.0))
            if (abs(centerPointQGS.x() - self.__tempCenterPointQGS.x()) > 40) or (
                    abs(centerPointQGS.y() - self.__tempCenterPointQGS.y()) > 40):
                self.renderTiles()
        event.setAccepted(False)

    def handleChildMousePress(self, event):
        event.setAccepted(False)

    def handleChildMouseRelease(self, event):
        if self.__scene.getCreationMode() == self.__scene.ObjectCreationMode.MarkCreation:
            mousePoint = self.mapToScene(self.__childView.mapFromGlobal(QCursor.pos()))
            self.__scene.tempObj.setPos(mousePoint)
            self.__scene.tempObj.setMark()
            self.__scene.addObject(self.__scene.tempObj)
            self.__scene.createObject()
        # self.requestObjectCreation.emit()
        # elif self.__scene.getCreationMode() == self.__scene.ObjectCreationMode.RouteCreation:
        #     mousePoint = self.mapToScene(self.__childView.mapFromGlobal(QCursor.pos()))
        #     self.__scene.tempObj.append(mousePoint)
        #     self.__scene.createObject()
        event.setAccepted(False)

    def handleChildViewContextMenu(self, event):
        event.setAccepted(False)

    def handleChildViewScrollWheel(self, event):
        event.setAccepted(False)
        self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)
        if event.delta() > 0:
            self.zoomIn(MapGraphicsView.ZoomMode.MouseZoom)
        else:
            self.zoomOut(MapGraphicsView.ZoomMode.MouseZoom)

    def renderTiles(self):
        if not self.__scene:
            print("No MapGraphicsScene to render")
            return
        if not self.__tileSource:
            print("No MapTileSource to render")
            return
        self.doTileLayout()

    def doTileLayout(self):
        centerPointQGS = self.__childView.mapToScene(int(self.__childView.width() / 2.0),
                                                     int(self.__childView.height() / 2.0))
        self.__tempCenterPointQGS = centerPointQGS
        viewportPolygonQGV = QPolygon()
        viewportPolygonQGV << QPoint(0, 0) \
        << QPoint(0, self.__childView.height()) \
        << QPoint(self.__childView.width(), self.__childView.height()) \
        << QPoint(self.__childView.width(), 0)
        viewportPolygonQGS = self.__childView.mapToScene(viewportPolygonQGV)
        boundingRect = viewportPolygonQGS.boundingRect()
        exaggeratedBoundingRect = boundingRect
        exaggeratedBoundingRect.setSize(boundingRect.size() * 2.0)
        exaggeratedBoundingRect.moveCenter(boundingRect.center())
        freeTiles = Queue()
        placesWhereTilesAre = []
        for tileObject in self.__tileObjects:
            if not tileObject.isVisible() or not exaggeratedBoundingRect.contains(tileObject.pos()):
                freeTiles.put(tileObject)
                tileObject.setVisible(False)
            else:
                placesWhereTilesAre.append(tileObject.pos())

        tileSize = self.__tileSource.tileSize()
        tilesPerRow = sqrt(self.__tileSource.tilesOnZoomLevel(self.zoomLevel()))
        tilesPerCol = tilesPerRow
        # TODO div 2 delete
        perSide = int(max(boundingRect.width() / tileSize / 2, boundingRect.height() / tileSize / 2) + 3)
        xc = int(max(0, (centerPointQGS.x() / tileSize) - perSide / 2))
        yc = int(max(0, (centerPointQGS.y() / tileSize) - perSide / 2))
        xMax = int(min(tilesPerRow, xc + perSide))
        yMax = int(min(yc + perSide, int(tilesPerCol)))
        for x in range(xc, xMax, 1):
            for y in range(yc, yMax, 1):
                scenePos = QPointF(x * tileSize + tileSize / 2, y * tileSize + tileSize / 2)
                tileIsThere = False
                for pos in placesWhereTilesAre:
                    if pos == scenePos:
                        tileIsThere = True
                if tileIsThere:
                    continue
                if freeTiles.empty():
                    tileObject = MapTileGraphicsObject(tileSize)
                    tileObject.setTileSource(self.__tileSource)
                    self.__tileObjects.add(tileObject)
                    self.__childScene.addItem(tileObject)
                    freeTiles.put(tileObject)
                tileObject = freeTiles.get()
                if tileObject.pos() != scenePos:
                    tileObject.setPos(scenePos)
                if not tileObject.isVisible():
                    tileObject.setVisible(True)
                # print('from MapGraphicsView ' + str(x) + str(y) + str(self.zoomLevel()))
                tileObject.setTile(x, y, self.zoomLevel())
        # print('delete ', len(self.__tileObjects))
        while freeTiles.qsize() > 2:
            tileObject = freeTiles.get()
            self.__tileObjects.remove(tileObject)
            # self.__childScene.removeItem(tileObject)
        # print('after delete', len(self.__tileObjects))

    def resetQGSSceneSize(self):
        if not self.__tileSource:
            return
        dimension = sqrt(self.__tileSource.tilesOnZoomLevel(self.zoomLevel())) * self.__tileSource.tileSize()
        if self.__childScene.sceneRect().width() != dimension:
            self.__childScene.setSceneRect(0, 0, dimension, dimension)
