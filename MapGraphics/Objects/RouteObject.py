from ..MapGraphicsObject import MapGraphicsObject
from PySide2.QtCore import QPointF,QLineF
from .LineObject import LineObject
from ..Position import Position
from requests import get
from json import loads


class RouteObject(MapGraphicsObject):
    def __init__(self, posBegin, posEnd, parent=None):
        super().__init__(True, parent)
        self.__posBegin = posBegin
        self.__posEnd = posEnd

        self.__thickness = max(0, min(5, 2))
        self.__lines = []
        self.__linePoints = []
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        self.getWay()
        self.setRoad()

    def getWay(self):
        response = get('http://router.project-osrm.org/route/v1/driving/%s,%s;%s,%s?overview=full&geometries=geojson' \
                   % (self.__posBegin.x(), self.__posBegin.y(), self.__posEnd.x(), self.__posEnd.y()))
        content = loads((response.content))
        self.__linePoints = content['routes'][0]['geometry']["coordinates"]

    def setRoad(self):
        cnt = 0
        lastPoint = None
        for coord in self.__linePoints:
            if lastPoint == None:
                cnt += 1
                lastPoint = Position(coord[0],coord[1],0.0)
                continue
            currentPoint = Position(coord[0],coord[1],0.0)
            line=LineObject(lastPoint,currentPoint,2)
            self.__lines.append(line)
            lastPoint = currentPoint
            cnt+=1
            if cnt==200:
                break

    def ListLine(self):
        return self.__lines
