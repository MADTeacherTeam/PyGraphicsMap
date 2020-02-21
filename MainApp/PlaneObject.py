from MapGraphics.MapGraphicsObject import MapGraphicsObject
from PySide2.QtGui import QImage
from PySide2.QtCore import QRectF


class PlaneObject(MapGraphicsObject):
    def __init__(self, pos, rot=None, parent=None):
        super().__init__(True, parent)
        self.__image = QImage('../images/planeImage.png')
        self.__sizeInMeters = QRectF(self.__image.width() / 2, self.__image.height() / 2,
                                     self.__image.width() / 15, self.__image.height() / 15)

        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        self.setPlane(pos, self.__sizeInMeters, rot)

    def boundingRect(self):
        return self.__sizeInMeters

    def paint(self, painter, option, widget=0):
        painter.drawImage(self.__sizeInMeters, self.__image)

    def setPlane(self, pos, sizeInMeters, rotation=None):
        width = sizeInMeters.width()
        height = sizeInMeters.height()
        self.__sizeInMeters = QRectF(-0.5 * width,
                                     -0.5 * height,
                                     width, height)
        self.redrawRequested.emit()
        self.setPos(pos)
        if rotation:
            self.setRotation(rotation)