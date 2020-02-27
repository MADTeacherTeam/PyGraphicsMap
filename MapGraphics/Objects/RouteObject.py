from ..MapGraphicsObject import MapGraphicsObject
from PySide2.QtCore import QPointF, QLineF, QRectF, QTimer
from .LineObject import LineObject
from ..Position import Position
from requests import get
from json import loads
from .CircleObject import CircleObject


class RouteObject(MapGraphicsObject):
    def __init__(self, posBegin=None, posEnd=None, parent=None):
        super().__init__(True, parent)
        self.__posBegin = posBegin
        self.__posEnd = posEnd

        self.__thickness = max(0, min(5, 2))
        self.__lines = []
        self.__linePoints = []
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        # self.getWay()
        # self.setRoad()

    def boundingRect(self):
        toRet = QRectF(-1.0, -1.0, 2.0, 2.0)
        return toRet

    def setPosBegin(self, pos):
        self.__posBegin = CircleObject(3)
        self.__posBegin.setPos(pos)
        # self.__posBegin = pos

    def setPosEnd(self, pos):
        self.__posEnd = CircleObject(3)
        self.__posEnd.setPos(pos)
        # self.__posEnd = pos

    def posBegin(self):
        return self.__posBegin

    def posEnd(self):
        return self.__posEnd

    def lines(self):
        return self.__lines

    def __del__(self):
        self.__lines.clear()

    def getWay(self):
        response = get('http://router.project-osrm.org/route/v1/driving/%s,%s;%s,%s?overview=full&geometries=geojson' \
                       % (self.__posBegin.pos().x(), self.__posBegin.pos().y(), self.__posEnd.pos().x(), self.__posEnd.pos().y()))
        content = loads(response.content)
        try:
            self.__linePoints = content['routes'][0]['geometry']["coordinates"]
            self.setRoad()
        except Exception:
            print('waiting for response')
            QTimer().singleShot(3000, self.getWay)

    def setRoad(self):
        # lastPoint = None
        # for coord in self.__linePoints:
        #     if lastPoint == None:
        #         lastPoint = Position(coord[0], coord[1], 0.0)
        #         continue
        #     currentPoint = Position(coord[0], coord[1], 0.0)
        #     line = LineObject(lastPoint, currentPoint, 0.0)
        #     # self.newObjectGenerated.emit(line)
        #     self.__lines.append(line)
        #     lastPoint = currentPoint

        for i in range(1, len(self.__linePoints)):
            lastPoint = Position(self.__linePoints[i-1][0], self.__linePoints[i-1][1], 0.0)
            currentPoint = Position(self.__linePoints[i][0], self.__linePoints[i][1], 0.0)
            line = LineObject(lastPoint, currentPoint, 0.0)
            self.newObjectGenerated.emit(line)
            self.__lines.append(line)

    def paint(self, painter, option, widget=0):
        for each in self.__lines:
            painter.drawLine(each)

    def checkObject(self, obj):
        if obj in self.__lines:
            return True
