from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt


class PrivateQGraphicsView(QGraphicsView):
    hadMouseDoubleClickEvent = pyqtSignal(QMouseEvent)
    hadMouseMoveEvent = pyqtSignal(QMouseEvent)
    hadMousePressEvent = pyqtSignal(QMouseEvent)
    hadMouseReleaseEvent = pyqtSignal(QMouseEvent)
    hadContextMenuEvent = pyqtSignal(QContextMenuEvent)
    hadWheelEvent = pyqtSignal(QWheelEvent)

    # signals
    # void
    # hadMouseDoubleClickEvent(QMouseEvent * event);
    # void
    # hadMouseMoveEvent(QMouseEvent * event);
    # void
    # hadMousePressEvent(QMouseEvent * event);
    # void
    # hadMouseReleaseEvent(QMouseEvent * event);
    # void
    # hadContextMenuEvent(QContextMenuEvent *);
    # void hadWheelEvent(QWheelEvent *);

    def __init__(self, parent=None):
        QGraphicsView.__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(scene, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mouseDoubleClickEvent(self, event):
        event.setAccepted(False)
        self.hadMouseDoubleClickEvent(event)
        if not event.isAccepted():
            QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        event.setAccepted(False)
        self.hadMouseMoveEvent(event)
        if not event.isAccepted():
            QGraphicsView.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        event.setAccepted(False)
        self.hadMousePressEvent(event)
        if not event.isAccepted():
            QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        event.setAccepted(False)
        self.hadMouseReleaseEvent(event)
        if not event.isAccepted():
            QGraphicsView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        event.setAccepted(False)
        self.hadContextMenuEvent(event)
        if not event.isAccepted():
            QGraphicsView.contextMenuEvent(self, event)

    def wheelEvent(self, event):
        event.setAccepted(False)
        self.hadWheelEvent(event)
        if not event.isAccepted():
            QGraphicsView.wheelEvent(self, event)
