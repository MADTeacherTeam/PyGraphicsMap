from MapGraphics.MapTileSource import MapTileSource
from abc import ABC, abstractmethod


class PrivateQGraphicsInfoSource(ABC):
    # dependency inversion pattern
    @abstractmethod
    def zoomLevel(self):
        pass

    @abstractmethod
    def tileSource(self):
        pass
