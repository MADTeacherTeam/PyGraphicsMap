from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, qWarning, QRectF, QPointF

from MapGraphics.MapGraphicsObject import MapGraphicsObject
from MapGraphics.guts.PrivateQGraphicsInfoSource import PrivateQGraphicsInfoSource
from MapGraphics.Position import Position
from MapGraphics.guts.Conversions import Conversions


class PrivateQGraphicsObject(QGraphicsObject):
    enabledChanged = Signal()
    opacityChanged = Signal()
    parentChanged = Signal()
    posChanged = Signal()
    rotationChanged = Signal()
    visibleChanged = Signal()
    zValueChanged = Signal()
    selectedChanged = Signal()
    toolTipChanged = Signal(str)
    flagsChanged = Signal()
    keyFocusRequested = Signal()
    redrawRequested = Signal()
    destroyed = Signal()

    def __init__(self, mgObj, infoSource, parent=None):
        QGraphicsObject.__init__(self, parent)
        self.__unconvertedSceneMouseCoordinates = {}
        self.__mgObj = None
        self.__infoSource = infoSource

        self.setMGObj(mgObj)
        self.setZValue(5.0)

        # self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

    def __del__(self):
        pass

    def boundingRect(self):
        toRet = QRectF(-1.0, -1.0, 2.0, 2.0)
        if self.__mgObj is None:
            print("Warning:" + "could not get bounding rect as MapGraphicsObject is null")
            return toRet

        if self.__mgObj.sizeIsZoomInvariant():
            return self.__mgObj.boundingRect()

        enuRect = QRectF(self.__mgObj.boundingRect())

        latLonCenter = QPointF(self.__mgObj.pos())
        latLonCenterPos = Position(latLonCenter, 0.0)
        leftLatLon = QPointF(Conversions.enu2lla_4_LLA(enuRect.left(),
                                                       0.0,
                                                       0.0,
                                                       latLonCenterPos.lonLat()))
        upLatLon = QPointF(Conversions.enu2lla_4_LLA(0.0,
                                                     enuRect.top(),
                                                     0.0,
                                                     latLonCenterPos.lonLat()))

        lonWidth = 2.0 * (latLonCenter.x() - leftLatLon.x())
        latHeight = 2.0 * (upLatLon.y() - latLonCenter.y())

        latLonRect = QRectF(leftLatLon.x(), upLatLon.y(), lonWidth, latHeight)

        tileSource = self.__infoSource.tileSource()
        if tileSource is None:
            print(self + "can't do bounding box conversion, null tile source.")
            return toRet

        zoomLevel = self.__infoSource.zoomLevel()
        topLeft = QPointF(tileSource.ll2qgs(latLonRect.topLeft(), zoomLevel))
        bottomRight = QPointF(tileSource.ll2qgs(latLonRect.bottomRight(), zoomLevel))

        toRet = QRectF(topLeft, bottomRight)
        toRet.moveCenter(QPointF(0, 0))
        return toRet

    def contains(self, point):
        if self.__mgObj is None:
            return False

        scenePoint = QPointF(self.mapToScene(point))

        tileSource = self.__infoSource.tileSource()
        if tileSource is None:
            print("can't do bounding box conversion, null tile source.")
            return False
        geoPoint = QPointF(tileSource.qgs2ll(scenePoint, self.__infoSource.zoomLevel()))

        return self.__mgObj.contains(geoPoint)

    def paint(self, painter, option, widget=None):
        if self.__mgObj is None:
            print("could not paint as our MapGraphicsObject is null")
            return

        painter.save()
        painter.scale(1.0, -1.0)

        if not self.__mgObj.sizeIsZoomInvariant():
            enuRect = QRectF(self.__mgObj.boundingRect())
            desiredWidthMeters = enuRect.width()
            desiredHeightMeters = enuRect.height()
            pixelRect = QRectF(self.boundingRect())
            widthPixels = pixelRect.width()
            heightPixels = pixelRect.height()

            scaleX = widthPixels / desiredWidthMeters
            scaleY = heightPixels / desiredHeightMeters

            painter.scale(scaleX, scaleY)
        self.__mgObj.paint(painter, option, widget)
        painter.restore()

        if self.isSelected():
            painter.drawRect(self.boundingRect())

    def setSelected(self, selected):
        QGraphicsItem.setSelected(self, selected)
        self.__mgObj.setSelected(self.isSelected())

    def contextMenuEvent(self, event):
        if self.__mgObj is None:
            return

        qgsScenePos = QPointF(event.scenePos())
        tileSource = self.__infoSource.tileSource()
        geoScenePos = tileSource.qgs2ll(qgsScenePos, self.__infoSource.zoomLevel())
        event.setScenePos(geoScenePos)

        self.__mgObj.contextMenuEvent(event)

        event.setScenePos(qgsScenePos)

        if not event.isAccepted():
            QGraphicsObject.contextMenuEvent(event)

    def itemChange(self, change, value):
        if self.__mgObj is None:
            return value

        if change == QGraphicsItem.ItemPositionChange:
            scenePos = QPointF(value.toPointF())
            tileSource = self.__infoSource.tileSource()
            if tileSource is None:
                geoPos = QPointF(tileSource.qgs2ll(scenePos, self.__infoSource.zoomLevel()))

                self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)
                self.__mgObj.setPos(geoPos)
                self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        return self.__mgObj.itemChange(change, value)

    def keyPressEvent(self, event):
        if self.__mgObj is None:
            return

        self.__mgObj.keyPressEvent(event)

        if not event.isAccepted():
            QGraphicsObject.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if self.__mgObj is None:
            return

        self.__mgObj.keyReleaseEvent(event)

        if not event.isAccepted():
            QGraphicsObject.keyReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.__mgObj is None:
            return

        self.convertSceneMouseEventCoordinates(event)
        self.__mgObj.mouseDoubleClickEvent(event)
        self.unconvertSceneMouseEventCoorindates(event)

        if not event.isAccepted():
            QGraphicsObject.mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        if self.__mgObj is None:
            return

        self.convertSceneMouseEventCoordinates(event)
        self.__mgObj.mouseMoveEvent(event)
        self.unconvertSceneMouseEventCoorindates(event)

        if not event.isAccepted():
            QGraphicsObject.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.__mgObj is None:
            return

        self.convertSceneMouseEventCoordinates(event)
        self.__mgObj.mousePressEvent(event)
        self.unconvertSceneMouseEventCoorindates(event)

        if not event.isAccepted():
            QGraphicsObject.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mgObj is None:
            return

        self.convertSceneMouseEventCoordinates(event)
        self.__mgObj.mouseReleaseEvent(event)
        self.unconvertSceneMouseEventCoorindates(event)

        if not event.isAccepted():
            QGraphicsObject.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if self.__mgObj is None:
            return

        qgsScenePos = QPointF(event.scenePos())
        tileSource = self.__infoSource.tileSource()
        geoScenePos = QPointF(tileSource.qgs2ll(qgsScenePos, self.__infoSource.zoomLevel()))
        event.setScenePos(geoScenePos)

        self.__mgObj.wheelEvent(event)

        event.setScenePos(qgsScenePos)

        if not event.isAccepted():
            QGraphicsObject.wheelEvent(event)

    # public slot
    def handleZoomLevelChanged(self):
        self.handlePosChanged()

    # private slots
    def handleEnabledChanged(self):
        self.setEnabled(self.__mgObj.enabled())

    def handleOpacityChanged(self):
        self.setOpacity(self.__mgObj.opacity())

    def handleParentChanged(self):
        pass
        # Need more complicated logic here that involves PrivateQGraphicsScene

    def handlePosChanged(self):
        geoPos = QPointF(self.__mgObj.pos())
        tileSource = self.__infoSource.tileSource()
        if tileSource is None:
            return

        zoomLevel = self.__infoSource.zoomLevel()
        qgsPos = QPointF(tileSource.ll2qgs(geoPos, zoomLevel))

        self.setFlag(QGraphicsObject.ItemSendsScenePositionChanges, False)
        self.setPos(qgsPos)
        self.setFlag(QGraphicsObject.ItemSendsScenePositionChanges, True)

    def handleRotationChanged(self):
        self.setRotation(self.__mgObj.rotation())

    def handleVisibleChanged(self):
        self.setVisible(self.__mgObj.visible())

    def handleZValueChanged(self):
        self.setZValue(self.__mgObj.zValue())

    def handleMGSelectedChanged(self):
        if self.__mgObj.isSelected() == self.isSelected():
            return

        self.setSelected(self.__mgObj.isSelected())
        self.__mgObj.__selected = self.isSelected()

        self.update()

    def handleMGToolTipChanged(self, toolTip):
        self.setToolTip(toolTip)

    def handleMGFlagsChanged(self):
        flags = MapGraphicsObject.MapGraphicsObjectFlag(self.__mgObj.flags())
        movable = False
        selectable = False
        focusable = False

        if flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable:
            movable = True
        if flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable:
            selectable = True
        if flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable:
            focusable = True

        self.setFlag(QGraphicsObject.ItemIsMovable, movable)
        self.setFlag(QGraphicsObject.ItemIsSelectable, selectable)
        self.setFlag(QGraphicsObject.ItemIsFocusable, focusable)

    def updateAllFromMG(self):
        self.handleEnabledChanged()
        self.handleOpacityChanged()
        self.handleParentChanged()
        self.handlePosChanged()
        self.handleRotationChanged()
        self.handleVisibleChanged()
        self.handleZValueChanged()
        self.handleMGSelectedChanged()
        self.handleMGFlagsChanged()

    def handleRedrawRequested(self):
        self.update()

    def handleKeyFocusRequested(self):
        self.setFocus()

    # private func
    def setMGObj(self, mgObj):
        self.__mgObj = mgObj

        if self.__mgObj is None:
            return

        self.enabledChanged.connect(self.handleEnabledChanged)
        # connect(_mgObj,
        #         SIGNAL(enabledChanged()),
        #         this,
        #         SLOT(handleEnabledChanged()));

        self.opacityChanged.connect(self.handleOpacityChanged)
        # connect(_mgObj,
        #         SIGNAL(opacityChanged()),
        #         this,
        #         SLOT(handleOpacityChanged()));

        self.parentChanged.connect(self.handleParentChanged)
        # connect(_mgObj,
        #         SIGNAL(parentChanged()),
        #         this,
        #         SLOT(handleParentChanged()));

        self.posChanged.connect(self.handlePosChanged)
        # connect(_mgObj,
        #         SIGNAL(posChanged()),
        #         this,
        #         SLOT(handlePosChanged()));

        self.rotationChanged.connect(self.handleRotationChanged)
        # connect(_mgObj,
        #         SIGNAL(rotationChanged()),
        #         this,
        #         SLOT(handleRotationChanged()));

        self.visibleChanged.connect(self.handleVisibleChanged)
        # connect(_mgObj,
        #         SIGNAL(visibleChanged()),
        #         this,
        #         SLOT(handleVisibleChanged()));

        self.zValueChanged.connect(self.handleZValueChanged)
        # connect(_mgObj,
        #         SIGNAL(zValueChanged()),
        #         this,
        #         SLOT(handleZValueChanged()));

        self.selectedChanged.connect(self.handleMGSelectedChanged)
        # connect(_mgObj,
        #         SIGNAL(selectedChanged()),
        #         this,
        #         SLOT(handleMGSelectedChanged()));

        self.toolTipChanged.connect(self.handleMGToolTipChanged)
        # connect(_mgObj,
        #         SIGNAL(toolTipChanged(QString)),
        #         this,
        #         SLOT(handleMGToolTipChanged(QString)));

        self.flagsChanged.connect(self.handleMGFlagsChanged)
        # connect(_mgObj,
        #         SIGNAL(flagsChanged()),
        #         this,
        #         SLOT(handleMGFlagsChanged()));

        self.keyFocusRequested.connect(self.handleKeyFocusRequested)
        # connect(_mgObj,
        #         SIGNAL(keyFocusRequested()),
        #         this,
        #         SLOT(handleKeyFocusRequested()));

        self.redrawRequested.connect(self.handleRedrawRequested)
        # connect(_mgObj,
        #         SIGNAL(redrawRequested()),
        #         this,
        #         SLOT(handleRedrawRequested()));

        self.updateAllFromMG()

        self.destroyed.connect(self.deleteLater)
        # connect(mgObj,
        #         SIGNAL(destroyed()),
        #         this,
        #         SLOT(deleteLater()));

    def convertSceneMouseEventCoordinates(self, event):
        qgsScenePos = QPointF(event.scenePos())
        tileSource = self.__infoSource.tileSource()
        geoPos = tileSource.qgs2ll(qgsScenePos, self.__infoSource.zoomLevel())

        self.__unconvertedSceneMouseCoordinates[event] = qgsScenePos

        event.setScenePos(geoPos)

    def unconvertSceneMouseEventCoorindates(self, event):
        qgsScenePos = QPointF()
        if self.__unconvertedSceneMouseCoordinates.get(event):
            qgsScenePos = self.__unconvertedSceneMouseCoordinates.get(event)
        else:
            print("didn't have original scene mouse coordiantes stored for un-conversion")
            tileSource = self.__infoSource.tileSource()
            qgsScenePos = tileSource.ll2qgs(event.scenePos(), self.__infoSource.zoomLevel())

        event.setScenePos(qgsScenePos)
