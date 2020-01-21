from PyQt5.QtCore import QTimer, qDebug, QCoreApplication, QPoint, QPointF, qWarning, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout
from PyQt5.Qt import QEventLoop
from PyQt5.QtGui import QCursor,QPolygonF
from .guts.MapTileGraphicsObject import MapTileGraphicsObject
from .guts.PrivateQGraphicsInfoSource import PrivateQGraphicsInfoSource
from .guts.PrivateQGraphicsScene import PrivateQGraphicsScene
from .guts.PrivateQGraphicsView import PrivateQGraphicsView
from enum import Enum
from queue import Queue
from math import sqrt


class MapGraphicsView(QWidget, PrivateQGraphicsInfoSource):
    class DragMode(Enum):
        NoDrag = 0
        ScrollHandDrag = 1
        RubberBandDrag = 2

    class ZoomMode(Enum):
        CenterZoom = 0
        MouseZoom = 1

    def __init__(self, scene=0, parent=0):
        QWidget.__init__(self, parent, None)
        self.setScene(scene)
        self.__zoomLevel = 2
        self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)
        renderTimer = QTimer(self)
        renderTimer.timeout.connect(self.renderTiles)
        renderTimer.start(200)
        self.__tileObjects = set()
        self.zoomLevelChanged = pyqtSignal(int)

    def __del__(self):
        qDebug(self, "Destructing")
        for tileObject in self.__tileObjects:
            if self.__childScene:
                self.__childScene.removeItem(tileObject)
        self.__tileObjects.clear()
        if self.__tileSource:
            tileSourceThread = self.__tileSource.thread()
            self.__tileSource = 0
            count = 0
            maxCount = 100
            while (tileSourceThread and not tileSourceThread.wait(100)):
                QCoreApplication.processEvents(QEventLoop.ExcludeSocketNotifiers | QEventLoop.ExcludeUserInputEvents)
                count += 1
                if count == maxCount:
                    break

    def center(self):
        centerGeoPos = self.mapToScene(QPoint(self.width() / 2, self.height() / 2))
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
            qWarning("No tile source --- Transformation cannot work")
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

    def scene(self):
        return self.__scene

    def setScene(self, scene):
        childScene = PrivateQGraphicsScene(scene, self, self)
        self.zoomLevelChanged.connect(childScene.handleZoomLevelChanged)
        childView = PrivateQGraphicsView(childScene, self)
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

    def tileSource(self):
        return self.__tileSource

    def setTileSource(self, tSource):
        self.__tileSource = tSource
        if self.__tileSource:
            tileSourceThread = QThread()
            tileSourceThread.start()
            self.__tileSource.moveToThread(tileSourceThread)
            self.__tileSource.destroyed.connect(tileSourceThread.quit)
            tileSourceThread.finished.connect(tileSourceThread.deleteLater)
        for tileObject in self.__tileObjects:
            tileObject.setTileSource(tSource)

    def zoomLevel(self):
        return self.__zoomLevel

    def setZoomLevel(self, nZoom, zMode):
        if not self.__tileSource:
            return
        centerGeoPos = self.mapToScene(QPoint(self.width() / 2, self.height() / 2))
        mousePoint = self.__childView.mapToScene(self.__childView.mapFromGlobal(QCursor.pos()))
        sceneRect = self.__childScene.sceneRect()
        xRatio = mousePoint.x() / sceneRect.width()
        yRatio = mousePoint.y() / sceneRect.height()
        centerPos = self.__childView.mapToScene(QPoint(self.__childView.width() / 2, self.__childView.height() / 2))
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
        self.zoomLevelChanged.emit(nZoom)

    def zoomIn(self, zMode):
        if not self.__tileSource:
            return

        if self.zoomLevel()<self.maxZoomLevel():
            self.setZoomLevel(self.zoomLevel()+1,zMode)


    def zoomOut(self,zMode):
        if not self.__tileSource:
            return

        if self.zoomLevel()>self.minZoomLevel():
            self.setZoomLevel(self.zoomLevel()-1,zMode)

    def handleChildMouseDoubleClick(self,event):
        event.setAccepted(False)

    def handleChildMouseMove(self,event):
        event.setAccepted(False)

    def handleChildMousePress(self,event):
        event.setAccepted(False)

    def handleChildMouseRelease(self,event):
        event.setAccepted(False)

    def handleChildViewContextMenu(self,event):
        event.setAccepted(False)

    def handleChildViewScrollWheel(self,event):
        event.setAccepted(False)
        self.setDragMode(MapGraphicsView.DragMode.ScrollHandDrag)
        if event.delta()>0:
            self.zoomIn(MapGraphicsView.ZoomMode.MouseZoom)
        else:
            self.zoomOut(MapGraphicsView.ZoomMode.MouseZoom)

    def renderTiles(self):
        if not self.__scene:
            qDebug("No MapGraphicsScene to render")
            return
        if not self.__tileSource:
            qDebug("No MapTileSource to render")
            return
        self.doTileLayout()


    def doTileLayout(self):
        centerPointQGS=self.__childView.mapToScene(self.__childView.width()/2.0,self.__childView.height()/2.0)
        viewportPolygonQGV=QPolygonF()
        viewportPolygonQGV<<QPoint(0,0)<<QPoint(0,self.__childView.height())<<QPoint(self.__childView.width(),self.__childView.height())<<QPoint(self.__childView.width(),0)
        viewportPolygonQGS=self.__childView.mapToScene(viewportPolygonQGV)
        boundingRect=viewportPolygonQGS.boundingRect()
        exaggeratedBoundingRect = boundingRect
        exaggeratedBoundingRect.setSize(boundingRect.size() * 2.0)
        exaggeratedBoundingRect.moveCenter(boundingRect.center())
        freeTiles=Queue()
        placesWhereTilesAre=set()
        for tileObject in self.__tileObjects:
            if not tileObject.isVisible() or not tileObject.pos() in exaggeratedBoundingRect:
                freeTiles.put(tileObject)
                tileObject.setVisible(False)
            else:
                placesWhereTilesAre.add(tileObject.pos())

        tileSize=self.__tileSource.tileSize()
        tilesPerRow=sqrt(self.__tileSource.tilesOnZoomLevel(self.zoomLevel()))
        tilesPerCol = tilesPerRow
        perSide=max(boundingRect.width()/tileSize,boundingRect.height()/tileSize)+3
        xc=max(0,(centerPointQGS.x() / tileSize) - perSide/2)
        yc=max(0,(centerPointQGS.y() / tileSize) - perSide/2)
        xMax=min(tilesPerRow,xc + perSide)
        yMax=min(yc + perSide,tilesPerCol)
        for x in range(xc,xMax,1):
            for y in range(yc,yMax,1):
                scenePos=QPointF(x*tileSize + tileSize/2,y*tileSize + tileSize/2)
                tileIsThere =False
                if scenePos in placesWhereTilesAre:
                    tileIsThere=True
                if tileIsThere:
                    continue
                if not freeTiles:
                    tileObject=MapTileGraphicsObject(tileSize)
                    tileObject.setTileSource(self.__tileSource)
                    self.__tileObjects.add(tileObject)
                    self.__childScene=tileObject
                tileObject=freeTiles.get()
                if tileObject.pos()!=scenePos:
                    tileObject.setPos(scenePos)
                if tileObject.isVisible()!=True:
                    tileObject.setVisible(True)
                tileObject.setTile(x,y,self.zoomLevel())
        while freeTiles.qsize()>2:
            tileObject=freeTiles.get()
            self.__tileObjects.remove(tileObject)
            self.__childScene.removeItem(tileObject)

    def resetQGSSceneSize(self):
        if not self.__tileSource:
            return
        dimension=sqrt(self.__tileSource.tilesOnZoomLevel(self.zoomLevel()))* self.__tileSource.tileSize()
        if self.__childScene.sceneRect().width()!=dimension:
            self.__childScene.setSceneRect(0,0,dimension,dimension)



