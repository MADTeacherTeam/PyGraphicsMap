from PyQt5 import QtCore
from enum import Enum


class MapGraphicsObject(QtCore.QObject):
    class MapGraphicsObjectFlag(Enum):
        ObjectIsMovable = 0x01
        ObjectIsSelectable = 0x02
        ObjectIsFocusable = 0x04

    def __init__(self, sizeIsZoomInvariant=False, parent=None):
        super.__init__()
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

        # QtCore.Qtimer.singleShot(1, self, signal(setConstrucred))

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
            # this->parentChanged();
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(parentChanged))
            pass

    def setPos(self, nPos):
        if nPos == self.__pos:
            return
        self.__pos = nPos

        if self.__constructed:
            # poschanged
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(posChanged))
            pass

    def setRotation(self, nRotation):
        if nRotation == self.__rotation:
            return
        self.__rotation = nRotation

        if self.__constructed:
            # rorationchanged
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(rotationChanged))
            pass

    def setVisible(self, nVisible):
        if nVisible == self.__visible:
            return
        self.__visible = nVisible

        if self.__constructed:
            # visibleChanged()
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(visibleChanged()))
            pass

    def setLongitude(self, nLongitude):
        self.setPos(QtCore.QPointF(nLongitude, self.__pos.y()))

    def setLatitude(self, nLatitude):
        self.setPos(QtCore.QPointF(self.__pos.x(), nLatitude))

    def setZValue(self, nZValue):
        self.__zValue = nZValue
        if self.__constructed:
            # zValueChanged
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(zValueChanged))
            pass

    def setSelected(self, sel):
        if self.__selected == sel:
            return
        self.__selected = sel

        if self.__constructed:
            # selectedChanged()
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(selectedChanged()))
            pass

    def setToolTip(self, toolTip):
        self.__toolTip = toolTip
        # this->toolTipChanged(toolTip);

    def setFlag(self, flag, enabled):
        if enabled:
            self.__flag = self.__flag | flag
        else:
            self.__flag = self.__flag & (~flag)

        # this->flagsChanged();

    def setFlags(self, flags):
        self.__flags = flags

        if self.__constructed:
            # this->flagsChanged();
            pass
        else:
            # QtCore.QTimer.singleShot(1, self, signal(flagsChanged()))
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
                # this->keyFocusRequested();
                pass
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def wheelEvent(self, event):
        event.ignore()

    def slot_setConstructed(self):
        self.__constructed = True
