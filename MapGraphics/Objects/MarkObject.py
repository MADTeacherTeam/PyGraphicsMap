from ..MapGraphicsObject import MapGraphicsObject
from PySide2.QtGui import QImage
from PySide2.QtCore import QRectF
from copy import deepcopy


class MarkObject(MapGraphicsObject):
    """Implementation of colored marks on map"""
    def __init__(self, img=0, rot=180, parent=None):
        # TODO zoomLevelChanged marks dont change pos
        super().__init__(True, parent)
        self.imageList = ['../images/mark0.png', '../images/mark1.png', '../images/mark2.png']
        self.__image = QImage(self.imageList[img])
        self.__sizeInMeters = QRectF(self.__image.width() / 2, self.__image.height() / 2,
                                     self.__image.width() / 15, self.__image.height() / 15)

        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        # self.setMark(self.pos(), self.__sizeInMeters, rot)

    def __del__(self):
        # print('Delete MarkObject')
        pass

    def changeImage(self, img=0):
        """Change color of mark by taking new image"""
        self.__image = QImage(self.imageList[img])
        self.__sizeInMeters = QRectF(self.__image.width() / 2, self.__image.height() / 2,
                                     self.__image.width() / 15, self.__image.height() / 15)
        self.redrawRequested.emit()

    def boundingRect(self):
        """Returns bounds of current item"""
        return self.__sizeInMeters

    def paint(self, painter, option, widget=0):
        """Install image of rendered item"""
        painter.drawImage(self.__sizeInMeters, self.__image)

    def setMark(self, rotation=180):
        """Reset mark's size for correct value"""
        width = self.__sizeInMeters.width()
        height = self.__sizeInMeters.height()
        self.__sizeInMeters = QRectF(-0.5 * width,
                                     -0.5 * height,
                                     width, height)
        self.redrawRequested.emit()
        # self.setPos(pos)
        if rotation:
            self.setRotation(rotation)

    def mouseMoveEvent(self, event):
        self.redrawRequested.emit()
        self.setPos(event.scenePos())
