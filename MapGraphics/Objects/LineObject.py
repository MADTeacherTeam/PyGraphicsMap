from PySide2.QtCore import QRectF, QPointF
from PySide2.QtGui import QPainter
from ..guts.Conversions import Conversions
from ..MapGraphicsObject import MapGraphicsObject


class LineObject(MapGraphicsObject):
    def __init__(self, endA, endB, thickness, parent=0):
        super().__init__(False, parent)
        self.__a = endA
        self.__b = endB
        self.__thickness = max(0, min(5, thickness))
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        self.updatePositionFromEndPoints()

    def boundingRect(self):
        avgLat = (self.__a.latitude() + self.__b.latitude()) / 2
        lonPerMeter = Conversions.degreesLonPerMeter(avgLat)
        latPerMeter = Conversions.degreesLatPerMeter(avgLat)

        widthLon = abs(self.__a.longitude() - self.__b.longitude())
        heightlat = abs(self.__a.latitude() - self.__b.latitude())

        widthMeters = max(widthLon / lonPerMeter, 5)
        heightMeters = max(heightlat / latPerMeter, 5.0)

        toRet = QRectF(-1.0 * widthMeters, -1.0 * heightMeters, 2.0 * widthMeters, 2.0 * heightMeters)
        return toRet

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = painter.pen()
        pen.setWidthF(self.__thickness)
        painter.setPen(pen)
        avgLat = (self.__a.latitude() + self.__b.latitude()) / 2
        lonPerMeter = Conversions.degreesLonPerMeter(avgLat)
        latPerMeter = Conversions.degreesLatPerMeter(avgLat)
        center = self.pos()
        offsetA = self.__a.lonLat() - center
        offsetB = self.__b.lonLat() - center
        metersA = QPointF(offsetA.x() / lonPerMeter, offsetA.y() / latPerMeter)
        metersB = QPointF(offsetB.x() / lonPerMeter, offsetB.y() / latPerMeter)
        painter.drawLine(metersA, metersB)

    def thickness(self):
        return self.__thickness

    def setThickness(self, nThick):
        self.__thickness = max(0, min(5, nThick))
        self.redrawRequested.emit()

    def setEndPointA(self, pos):
        self.__a = pos
        self.updatePositionFromEndPoints()
        self.redrawRequested.emit()

    def setEndPointB(self, pos):
        self.__b = pos
        self.updatePositionFromEndPoints()
        self.redrawRequested.emit()

    def setEndPoints(self, a, b):
        self.__a = a
        self.__b = b
        self.updatePositionFromEndPoints()
        self.redrawRequested.emit()

    def updatePositionFromEndPoints(self):
        avgLon = (self.__a.longitude() + self.__b.longitude()) / 2
        avgLat = (self.__a.latitude() + self.__b.latitude()) / 2
        self.setPos(QPointF(avgLon, avgLat))
