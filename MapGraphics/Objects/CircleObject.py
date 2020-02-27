from PySide2.QtCore import QRectF, QPointF
from PySide2.QtGui import QColor, QPainter, QKeySequence
from ..MapGraphicsObject import MapGraphicsObject


class CircleObject(MapGraphicsObject):
    def __init__(self, radius, sizeIsZoomInvariant=True, fillColor=QColor(0, 1, 1, 0), parent=None):
        super().__init__(sizeIsZoomInvariant, parent)
        self.__fillColor = fillColor
        self.__radius = max(radius, 0.01)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)

    def __del__(self):
        print('del circle object')

    def boundingRect(self):
        return QRectF(-1 * self.__radius, -1 * self.__radius, 2 * self.__radius, 2 * self.__radius)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(self.__fillColor)
        painter.drawEllipse(QPointF(0, 0), self.__radius, self.__radius)

    def radius(self):
        return self.__radius

    def setRadius(self, radius):
        self.__radius = radius
        self.redrawRequested.emit()

    def keyReleaseEvent(self, event):
        if event.matches(QKeySequence.Delete):
            self.deleteLater()
            event.accept()
        else:
            event.ignore()
