from PyQt5 import QtCore
from enum import Enum


class MapGraphicsObject(QtCore.QObject):
    class MapGraphicsObjectFlag(Enum):
        ObjectIsMovable = 0x01
        ObjectIsSelectable = 0x02
        ObjectIsFocusable = 0x04

    def __init__(self, sizeIsZoomInvariant=False, parent=None):
        super().__init__()
        self.__enabled = True
        self.__opacity = 1.0
        self.setParent(parent)
        self.__pos = QtCore.QPointF(0.0, 0.0)
        self.__rotation = 0.0
        self.__visible = True
        self.__zValue = 0.0
        self.__selected = False

        self.__sizeIsZoomInvariant = sizeIsZoomInvariant
        self.__constructed = False
        # SIGNALS
        self.enabledChanged = QtCore.pyqtSignal()
        self.opacityChanged = QtCore.pyqtSignal()
        self.parentChanged = QtCore.pyqtSignal()
        self.posChanged = QtCore.pyqtSignal()
        self.rotationChanged = QtCore.pyqtSignal()
        self.visibleChanged = QtCore.pyqtSignal()
        self.zValueChanged = QtCore.pyqtSignal()
        self.toolTipChanged = QtCore.pyqtSignal(str)
        self.flagsChanged = QtCore.pyqtSignal()
        self.selectedChanged = QtCore.pyqtSignal()
        self.newObjectGenerated = QtCore.pyqtSignal(MapGraphicsObject)
        self.redrawRequested = QtCore.pyqtSignal()
        self.keyFocusRequested = QtCore.pyqtSignal()
        ##############################################################################################################
        QtCore.QTimer().singleShot(1, self.slot_setConstructed())

    def boundingRect(self):
        pass

    def contains(self, geoPos):
        geoRect = self.boundingRect()
        return geoRect.contains(geoPos)

    def paint(self, painter, option, widget=0):
        pass

    def setParent(self, nParent):
        self.__parent = nParent
        if self.__constructed:
            self.parentChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self, self.parentChanged)
            pass

    def setPos(self, nPos):
        if nPos == self.__pos:
            return
        self.__pos = nPos

        if self.__constructed:
            self.posChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.posChanged)
            pass

    def setRotation(self, nRotation):
        if nRotation == self.__rotation:
            return
        self.__rotation = nRotation

        if self.__constructed:
            self.rotationChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.rotationChanged)
            pass

    def setVisible(self, nVisible):
        if nVisible == self.__visible:
            return
        self.__visible = nVisible

        if self.__constructed:
            self.visibleChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.visibleChanged)
            pass

    def setLongitude(self, nLongitude):
        self.setPos(QtCore.QPointF(nLongitude, self.__pos.y()))

    def setLatitude(self, nLatitude):
        self.setPos(QtCore.QPointF(self.__pos.x(), nLatitude))

    def setZValue(self, nZValue):
        self.__zValue = nZValue
        if self.__constructed:
            self.zValueChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.zValueChanged)
            pass

    def setSelected(self, sel):
        if self.__selected == sel:
            return
        self.__selected = sel

        if self.__constructed:
            self.selectedChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.selectedChanged())
            pass

    def setToolTip(self, toolTip):
        self.__toolTip = toolTip
        self.toolTipChanged.emit(toolTip)

    def setFlag(self, flag, enabled):
        if enabled:
            self.__flag = self.__flag | flag
        else:
            self.__flag = self.__flag & (~flag)

        self.flagsChanged.emit();

    def setFlags(self, flags):
        self.__flags = flags

        if self.__constructed:
            self.flagsChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.flagsChanged)
            pass

    def contextMenuEvent(self, event):
        event.ignore()

    def itemChange(self, change, value):

        return value

    def keyPressEvent(self, event):
        event.ignore()

    def keyReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        if self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable or self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable:
            event.accept()
            if self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable:
                self.keyFocusRequested.emit()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def wheelEvent(self, event):
        event.ignore()

    def slot_setConstructed(self):
        self.__constructed = True

    def pos(self):
        return self.__pos
