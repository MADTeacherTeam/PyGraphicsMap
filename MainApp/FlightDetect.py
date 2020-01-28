from opensky_api.opensky_api import OpenSkyApi
from MapGraphics.CircleObject import CircleObject
from MapGraphics.MapGraphicsObject import MapGraphicsObject
from PySide2.QtCore import QPointF, QTimer
from PySide2.QtGui import QPainter, QColor
from datetime import datetime, time


class FlightDetect:
    def __init__(self, scene):
        self.__scene = scene
        self.api = OpenSkyApi()
        self.__planeObjects = []

    def createPlanes(self):
        states = self.api.get_states()
        i = 0
        for state in states.states:
            toRet = CircleObject(1)
            if isinstance(toRet, CircleObject):
                toRet.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
                print("(%r, %r, %r)" % (state.latitude, state.longitude, state.icao24))
                if state.longitude and state.latitude:
                    pos = QPointF(float(state.longitude), float(state.latitude))
                    toRet.setPos(pos)
                    toRet.paint(QPainter(), True)
                    self.__planeObjects.append(toRet)
                    self.__scene.addObject(toRet)
                    i = i + 1
                if i == 1500:
                    break
        QTimer().singleShot(10000, self.delPlanes)
        QTimer().singleShot(11000, self.createPlanes)

    def delPlanes(self):
        for row in self.__planeObjects:
            # self.__planeObjects.remove(row)
            self.__scene.removeObject(row)
        self.__planeObjects.clear()









