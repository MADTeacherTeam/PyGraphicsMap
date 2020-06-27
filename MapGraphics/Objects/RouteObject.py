import math
from json import loads

from PySide2.QtCore import QPointF, QRectF, QTimer, Signal, QSizeF, QLineF
from PySide2.QtGui import QPainterPath, QPainter, QColor, Qt, QPolygonF, QTransform
from requests import get

from .CircleObject import CircleObject
from ..MapGraphicsObject import MapGraphicsObject
from ..Position import Position


class RouteObject(MapGraphicsObject):
    """Implementation of routes on map"""
    getMovementObject = Signal(object)

    def __init__(self, posBegin=None, posEnd=None, parent=None):
        super().__init__(True, parent)
        # print('create route object')
        self.__posBegin = posBegin
        self.__posEnd = posEnd
        self.__delta = 0.00005
        self.__linePoints = []
        self.points = []
        self.__drawPoints = []
        self.__route = None
        self.__zoomLvl = None
        self.boundRect = None
        # self.setZValue(3.0)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)

    def boundingRect(self):
        """Returns bounds of current item"""
        if self.boundRect is not None:
            return self.boundRect
        else:
            return QRectF(-1.0, -1.0, 2.0, 2.0)

    def setPosBegin(self, pos):
        """Set pos begin of the route"""
        self.__posBegin = CircleObject(3)
        self.__posBegin.setPos(pos)

    def setPosEnd(self, pos):
        """Set pos end of the route"""
        self.__posEnd = CircleObject(3)
        self.__posEnd.setPos(pos)
        self.boundRect = QRectF(self.__posBegin.pos(), self.__posEnd.pos())

    def posBegin(self):
        return self.__posBegin

    def posEnd(self):
        return self.__posEnd

    def getWay(self, i=1):
        """Request to OSM server to get route between two points."""
        try:
            response = get(
                'http://router.project-osrm.org/route/v1/driving/%s,%s;%s,%s?overview=full&geometries=geojson' \
                % (self.__posBegin.pos().x(), self.__posBegin.pos().y(), self.__posEnd.pos().x(),
                   self.__posEnd.pos().y()))
            content = loads(response.content)
            self.__linePoints = content['routes'][0]['geometry']["coordinates"]
            self.distance = content['routes'][0]['distance']
            self.setRoad(True)
        except Exception:
            print('waiting for response')
            i += 1
            if i >= 15:
                return
            # QTimer().singleShot(3000, self.getWay)
            self.getWay(i)

    def setRoad(self, flag=False):
        """If we need to remove extra points call with flag=True
        Count average longtitude and latitude
        Then calls render function updateRoute()"""
        if flag:
            self.__linePoints = self.simplify_points(self.__linePoints, self.__delta)
        avgLon1 = (self.__posBegin.pos().x() + self.__posEnd.pos().x()) / 2
        avgLat1 = (self.__posBegin.pos().y() + self.__posEnd.pos().y()) / 2
        self.setPos(QPointF(avgLon1, avgLat1))
        self.updateRoute()
        self.redrawRequested.emit()

    def setZoomLevel(self, nZValue):
        self.__zoomLvl = nZValue

    def ll2qgs(self, ll):
        """Converts longtitude and latitude to QGraphicsScene coords"""
        PI = 3.14159265358979323846
        deg2rad = PI / 180.0
        tilesOnOneEdge = pow(2, self.__zoomLvl)
        tileSize = 256
        x = (ll.x() + 180) * (tilesOnOneEdge * tileSize) / 360
        y = (1 - (math.log(math.tan(PI / 4 + (ll.y() * deg2rad) / 2)) / PI)) / 2 * (tilesOnOneEdge * tileSize)
        return QPointF(int(x), int(y))

    def paint(self, painter, option, widget=0):
        """Render the route item on map with pen and antialiasing"""
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = painter.pen()
        pen.setWidthF(6)
        color = QColor('blue')
        color.setAlpha(130)
        pen.setColor(color)
        painter.setPen(pen)

        self.updateRoute()
        painter.drawPath(self.__route)

    def updateRoute(self):
        """Recount points of road relatively zoomLevel and position"""
        self.__route = QPainterPath()
        qgsPos = self.ll2qgs(self.pos())
        lastPoint = Position(self.__linePoints[0][0], self.__linePoints[0][1], 0.0)

        self.__drawPoints.clear()

        temp = self.ll2qgs(lastPoint.lonLat())
        offX = temp.x() - qgsPos.x()
        offY = -(temp.y() - qgsPos.y())
        firstPoint = QPointF(offX, offY)
        self.__route.moveTo(firstPoint)
        self.__drawPoints.append(firstPoint)

        for i in range(1, len(self.__linePoints)):
            currentPoint = Position(self.__linePoints[i][0], self.__linePoints[i][1], 0.0)
            temp = self.ll2qgs(currentPoint.lonLat())
            offX = temp.x() - qgsPos.x()
            offY = -(temp.y() - qgsPos.y())
            endPoint = QPointF(offX, offY)

            self.__route.lineTo(endPoint)
            self.__drawPoints.append(endPoint)

        self.boundRect = self.__route.controlPointRect()
        # self.redrawRequested.emit()

    def linePoints(self):
        return self.__linePoints

    def simplify_points(self, pts, tolerance):
        """Remove extra points by Ramer–Douglas–Peucker algorithm"""
        import math
        anchor = 0
        floater = len(pts) - 1
        stack = []
        keep = set()

        stack.append((anchor, floater))
        while stack:
            anchor, floater = stack.pop()

            if pts[floater] != pts[anchor]:
                anchorX = float(pts[floater][0] - pts[anchor][0])
                anchorY = float(pts[floater][1] - pts[anchor][1])
                seg_len = math.sqrt(anchorX ** 2 + anchorY ** 2)
                anchorX /= seg_len
                anchorY /= seg_len
            else:
                anchorX = anchorY = seg_len = 0.0

            max_dist = 0.0
            farthest = anchor + 1
            for i in range(anchor + 1, floater):
                dist_to_seg = 0.0
                vecX = float(pts[i][0] - pts[anchor][0])
                vecY = float(pts[i][1] - pts[anchor][1])
                seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
                proj = vecX * anchorX + vecY * anchorY
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:
                    vecX = float(pts[i][0] - pts[floater][0])
                    vecY = float(pts[i][1] - pts[floater][1])
                    seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
                    proj = vecX * (-anchorX) + vecY * (-anchorY)
                    if proj < 0.0:
                        dist_to_seg = seg_len
                    else:
                        dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                    if max_dist < dist_to_seg:
                        max_dist = dist_to_seg
                        farthest = i

            if max_dist <= tolerance:
                keep.add(anchor)
                keep.add(floater)
            else:
                stack.append((anchor, farthest))
                stack.append((farthest, floater))

        keep = list(keep)
        keep.sort()
        return [pts[i] for i in keep]

    def mousePressEvent(self, event):
        """Handling mouse press to bounds of route"""
        for i in range(1, len(self.__drawPoints)):
            rectOfPoint = QRectF(QPointF(self.__drawPoints[i - 1].x(), self.__drawPoints[i - 1].y()),
                                 QPointF(self.__drawPoints[i].x(), self.__drawPoints[i].y())).normalized()
            center = rectOfPoint.center()
            rectOfPoint.setSize((rectOfPoint.size() * (-self.__zoomLvl + 19)))
            rectOfPoint.moveCenter(center)
            if rectOfPoint.contains(QPointF(event.pos().x(), -event.pos().y())):
                self.getMovementObject.emit(self)
                self.removeRequested.emit(self)
                break
        event.ignore()
