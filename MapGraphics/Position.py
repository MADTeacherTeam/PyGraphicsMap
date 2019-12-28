from PyQt5 import QtCore,QtGui
import math
class Position():
    def __init__(self):
        self.__lonLat=QtCore.QPointF(0.0,0.0)
        self.__altitude=0

    def constr_three_arg(self,longitude,latitude,altitude):
        self.__lonLat=QtCore.QPointF(longitude,latitude)
        self.__altitude=altitude

    def constr_two_arg(self,lonLat,altitude):
        self.__lonLat=lonLat
        self.__altitude=altitude

    def constr_one_arg(self,other):
        self.__lonLat=other.__lonLat
        self.__altitude=other.__altitude

    def __eq__(self, other):
        return (self.__lonLat==other.__lonLat and self.__altitude==other.__altitude)

    def __ne__(self, other):
        return not(self==other)

    def longitude(self):
        return self.__lonLat.x()

    def latitude(self):
        return  self.__lonLat.y()

    def altitude(self):
        return  self.__altitude

    def lonLat(self):
        return  self.__lonLat

    def setLongitude(self,longitude):
        self.__lonLat.setX(longitude)

    def setLatitude(self,latitude):
        self.__lonLat.setY(latitude)

    def setAltitude(self,altitude):
        self.__altitude=altitude

    def flatDistanceEstimate(self,other):
        offsetMeters=self.flatOffsetMeters(other)
        return  offsetMeters.length()


    def flatOffsetMeters(self,dest):
        avgLat=(self.latitude()+ dest.latitude())/2.0
        lonPerMeter=Conversions.degreesLonPerMeter(avgLat)
        latPerMeter=Conversions.degreesLatPerMeter(avgLat)
        lonDiffMeters=(dest.longitude()-self.longitude())/lonPerMeter
        latDiffMeters=(dest.latitude()-self.latitude())/latPerMeter
        return QtGui.QVector2D(lonDiffMeters, latDiffMeters)

    def flatOffsetToPosition(self,offset):
        lonPerMeter=Conversions.degreesLonPerMeter(self.latitude())
        latPerMeter = Conversions.degreesLatPerMeter(self.latitude())
        obj=Position()
        obj.constr_two_arg(self.longitude() + offset.x() * lonPerMeter,self.latitude() + offset.y() * latPerMeter)
        return obj

    def flatManhattanEstimate(self,other):
        offsetMeters=self.flatOffsetMeters(other)
        return abs(offsetMeters.x())+abs(offsetMeters.y())

    def angleTo(self,dest):
        offsetMeters = self.flatOffsetMeters(dest)
        return math.atan2(offsetMeters.y(), offsetMeters.x())

    @staticmethod
    def Position2ENU(refPos,pos):
        return Conversions.lla2enu(pos.latitude(), pos.longitude(),pos.altitude(),refPos.latitude(),refPos.longitude(),refPos.altitude())

    @staticmethod
    def fromENU(refPos,enu):
        cPos=Conversions.enu2lla(enu,refPos.latitude(),refPos.longitude(),refPos.altitude())
        return cPos

    #OVERLOAD OPERATOR >>

def qHash(pos):
    return pos.lonLat().x() + pos.lonLat().y() + pos.altitude()