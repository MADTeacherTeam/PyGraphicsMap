from abc import ABC, abstractmethod


class PrivateQGraphicsInfoSource(ABC):
    """Abstract class which inherited by MapGraphicsView as an implementation
    of the "dependency inversion" design pattern.

    PrivateQGraphicsObject and PrivateQGraphicsScene can get information from MapGraphicsView by this interface"""
    # dependency inversion pattern
    @abstractmethod
    def zoomLevel(self):
        pass

    @abstractmethod
    def tileSource(self):
        pass
