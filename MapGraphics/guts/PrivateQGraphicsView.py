from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class PrivateQGraphicsView(QGraphicsView):
    hadMouseDoubleClickEvent = Signal(QMouseEvent)
    hadMouseMoveEvent = Signal(QMouseEvent)
    hadMousePressEvent = Signal(QMouseEvent)
    hadMouseReleaseEvent = Signal(QMouseEvent)
    hadContextMenuEvent = Signal(QContextMenuEvent)
    hadWheelEvent = Signal(QWheelEvent)

    def __init__(self, parent=None, scene=None):
        if scene is None:
            super(PrivateQGraphicsView, self).__init__(parent)
        else:
            super(PrivateQGraphicsView, self).__init__(scene, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        event.setAccepted(False)
        self.hadMouseDoubleClickEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        event.setAccepted(False)
        self.hadMouseMoveEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        event.setAccepted(False)
        self.hadMousePressEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        event.setAccepted(False)
        self.hadMouseReleaseEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        event.setAccepted(False)
        self.hadContextMenuEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.contextMenuEvent(self, event)

    def wheelEvent(self, event):
        event.setAccepted(False)
        self.hadWheelEvent.emit(event)
        if not event.isAccepted():
            QGraphicsView.wheelEvent(self, event)
