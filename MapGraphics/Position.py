from PySide2 import QtCore, QtGui
import math
from MapGraphics.guts.Conversions import Conversions


class Position():
    def __init__(self, *args):
        len = args.__len__()
        if len == 0:
            self.__lonLat = QtCore.QPointF(0.0, 0.0)
            self.__altitude = 0
        elif len == 1 and isinstance(args[0], Position):
            self.constr_one_arg(args[0])
        elif (len == 2 and isinstance(args[0], QtCore.QPointF) and isinstance(args[1], (int, float))) \
                or (len == 1 and isinstance(args[0], QtCore.QPointF)):
            if len == 2:
                self.constr_two_arg(args[0], args[1])
            else:
                self.constr_two_arg(args[0])
        elif (len == 3 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)) and isinstance(
                args[2], (int, float))) \
                or (len == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float))):
            if len == 3:
                self.constr_three_arg(args[0], args[1], args[2])
            else:
                self.constr_three_arg(args[0], args[1])
        else:
            print('Wrong len in init of Position class')

    def constr_three_arg(self, longitude, latitude, altitude=0.0):
        self.__lonLat = QtCore.QPointF(longitude, latitude)
        self.__altitude = altitude

    def constr_two_arg(self, lonLat, altitude=0.0):
        self.__lonLat = lonLat
        self.__altitude = altitude

    def constr_one_arg(self, other):
        self.__lonLat = other.__lonLat
        self.__altitude = other.__altitude

    def __eq__(self, other):
        if other is None:
            return False
        return self.__lonLat == other.__lonLat and self.__altitude == other.__altitude

    def __ne__(self, other):
        return not (self == other)

    def longitude(self):
        """return longitude"""
        return self.__lonLat.x()

    def latitude(self):
        """return latitude"""
        return self.__lonLat.y()

    def altitude(self):
        """return altitude"""
        return self.__altitude

    def lonLat(self):
        """return QPointF(longitude,latitude)"""
        return self.__lonLat

    def setLongitude(self, longitude):
        self.__lonLat.setX(longitude)

    def setLatitude(self, latitude):
        self.__lonLat.setY(latitude)

    def setAltitude(self, altitude):
        self.__altitude = altitude

    def flatDistanceEstimate(self, other):
        """estimate distance offset"""
        offsetMeters = self.flatOffsetMeters(other)
        return offsetMeters.length()

    def flatOffsetMeters(self, dest):
        """calculating the offset"""
        avgLat = (self.latitude() + dest.latitude()) / 2.0
        lonPerMeter = Conversions.degreesLonPerMeter(avgLat)
        latPerMeter = Conversions.degreesLatPerMeter(avgLat)
        lonDiffMeters = (dest.longitude() - self.longitude()) / lonPerMeter
        latDiffMeters = (dest.latitude() - self.latitude()) / latPerMeter
        return QtGui.QVector2D(lonDiffMeters, latDiffMeters)

    def flatOffsetToPosition(self, offset):
        """calculating the offset relative to the position"""
        lonPerMeter = Conversions.degreesLonPerMeter(self.latitude())
        latPerMeter = Conversions.degreesLatPerMeter(self.latitude())
        obj = Position()
        obj.constr_two_arg(self.longitude() + offset.x() * lonPerMeter, self.latitude() + offset.y() * latPerMeter)
        return obj

    def flatManhattanEstimate(self, other):
        offsetMeters = self.flatOffsetMeters(other)
        return abs(offsetMeters.x()) + abs(offsetMeters.y())

    def angleTo(self, dest):
        """calculation of the angle of inclination"""
        offsetMeters = self.flatOffsetMeters(dest)
        return math.atan2(offsetMeters.y(), offsetMeters.x())

    @staticmethod
    def Position2ENU(refPos, pos):
        """convert Position(refPos), Position(pos) to QVector3D(enu)"""
        return Conversions.lla2enu_6(pos.latitude(), pos.longitude(), pos.altitude(), refPos.latitude(),
                                     refPos.longitude(), refPos.altitude())

    @staticmethod
    def fromENU(refPos, enu):
        """convert Position(refPos), QVector3D(enu) to Position"""
        cPos = Conversions.enu2lla_4_re(enu, refPos.latitude(), refPos.longitude(), refPos.altitude())
        return cPos


def qHash(pos):
    """return summer of latitude, longitude, altitude"""
    return pos.lonLat().x() + pos.lonLat().y() + pos.altitude()
