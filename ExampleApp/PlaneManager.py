from opensky_api.opensky_api import OpenSkyApi
from ExampleApp.PlaneObject import PlaneObject
from PySide2.QtCore import QPointF, QTimer, QObject, QThread


class PlaneManager(QObject):
    # updateSignal = Signal()

    def __init__(self, scene):
        super().__init__()
        self.__scene = scene
        self.api = OpenSkyApi('login', 'password')  # enter your login and password of opensky
        self.__planeObjects = {}
        self.__planeCounter = 500
        self.timerCreatePlanes = QTimer()

        # self.createPlanes()

    def createPlanes(self):
        if self.__planeObjects:
            self.reposPlaneObjects()
        else:
            self.fillPlaneObjectDict()

        self.timerCreatePlanes.singleShot(5000, self.createPlanes)

    def fillPlaneObjectDict(self):
        states = self.api.get_states()
        if not states:
            print('No states from replay')
            return
        i = 0
        for plane in states.states:
            if plane.longitude and plane.latitude:
                if plane.heading:
                    self.__planeObjects[plane.icao24] = PlaneObject(
                        QPointF(float(plane.longitude), float(plane.latitude)), plane.heading)
                else:
                    self.__planeObjects[plane.icao24] = PlaneObject(QPointF(float(plane.longitude),
                                                                            float(plane.latitude)))
                self.__scene.addObject(self.__planeObjects[plane.icao24])
                i = i + 1
                if i == self.__planeCounter:
                    break

    def reposPlaneObjects(self):
        states = self.api.get_states()
        if not states:
            print('No states from replay')
            return
        for plane in states.states:
            if self.__planeObjects.__contains__(plane.icao24):
                if plane.longitude and plane.latitude:
                    self.__planeObjects[plane.icao24].setPos(QPointF(float(plane.longitude), float(plane.latitude)))
                    if plane.heading:
                        self.__planeObjects[plane.icao24].setRotation(plane.heading)
                    else:
                        self.__planeObjects[plane.icao24].setRotation(0)
                    self.__planeObjects[plane.icao24].redrawRequested.emit()
                else:
                    self.__planeObjects.pop(plane.icao24)
            else:
                if self.__planeObjects.__len__() < self.__planeCounter:
                    if plane.longitude and plane.latitude:
                        if plane.heading:
                            self.__planeObjects[plane.icao24] = PlaneObject(
                                QPointF(float(plane.longitude), float(plane.latitude)), plane.heading)
                        else:
                            self.__planeObjects[plane.icao24] = PlaneObject(QPointF(float(plane.longitude),
                                                                                    float(plane.latitude)))
                    self.__scene.addObject(self.__planeObjects[plane.icao24])
