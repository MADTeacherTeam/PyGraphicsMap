from PySide2 import QtCore, QtGui
import math

pi = 3.141592653589793238462643383
A_EARTH = 6378137
flattening = 1.0 / 298.257223563
NAV_E2 = (2.0 - flattening) * flattening
deg2rad = pi / 180.0
rad2deg = 180.0 / pi


class Conversions:
    @staticmethod
    def lla2xyz_3(wlat, wlon, walt):
        toRet = QtGui.QVector3D()

        if wlat < -90.0 or wlat > 90.0 or wlon < -180.0 or wlon > 180.0:
            print('Lat/Lon out of range', wlat, wlon)
            return toRet

        slat = math.sin(wlat * deg2rad)
        clat = math.cos(wlat * deg2rad)
        r_n = A_EARTH / math.sqrt(1.0 - NAV_E2 * slat * slat)

        toRet.setX((r_n + walt) * clat * math.cos(wlon * deg2rad))
        toRet.setY((r_n + walt) * clat * math.sin(wlon * deg2rad))
        toRet.setZ((r_n * (1.0 - NAV_E2) + walt) * slat)

        return toRet

    @staticmethod
    def lla2xyz(lla):
        return Conversions.lla2xyz_3(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude())

    @staticmethod
    def xyz2lla(v):
        return Conversions.xyz2lla_3(v.x(), v.y(), v.z())

    @staticmethod
    def xyz2lla_3(x, y, z):
        # пока так
        from MapGraphics.Position import Position
        toRet = Position()
        del Position
        toRet.setAltitude(0.0)

        if x == 0.0 and y == 0.0 and z == 0.0:
            QtCore.qWarning(b"Error: XYZ at center of the earth")
            return toRet

        if x == 0.0 and y == 0.0:
            toRet.setLongitude(0.0)
        else:
            toRet.setLongitude(math.atan2(y, x) * rad2deg)

        rhosqrd = x * x + y * y
        rho = math.sqrt(rhosqrd)
        templat = math.atan2(z, rho)
        tempalt = math.sqrt(rhosqrd + z * z) - A_EARTH
        rhoerror = 1000.0
        zerror = 1000.0

        while math.fabs(rhoerror) > 0.000001 or math.fabs(zerror) > 0.000001:
            slat = math.sin(templat)
            clat = math.cos(templat)
            q = 1.0 - NAV_E2 * slat * slat
            r_n = A_EARTH / math.sqrt(q)
            drdl = r_n * NAV_E2 * slat * clat / q

            rhoerror = (r_n + tempalt) * clat - rho
            zerror = (r_n * (1.0 - NAV_E2) + tempalt) * slat - z

            aa = drdl * clat - (r_n + tempalt) * slat
            bb = clat
            cc = (1.0 - NAV_E2) * (drdl * slat + r_n * clat)
            dd = slat

            invdet = 1.0 / (aa * dd - bb * cc)
            templat = templat - invdet * (dd * rhoerror - bb * zerror)
            tempalt = tempalt - invdet * (-1 * cc * rhoerror + aa * zerror)

        toRet.setLatitude(templat * rad2deg)
        toRet.setAltitude(tempalt)
        return toRet

    @staticmethod
    def xyz2enu_4_re(xyz, reflat, reflon, refalt):
        refxyz = Conversions.lla2xyz_3(reflat, reflon, refalt)
        diffxyz = xyz - refxyz

        R1 = Conversions.rot(90.0 + reflon, 3)
        R2 = Conversions.rot(90.0 - reflat, 1)
        R = R2 * R1

        x = R.m11() * diffxyz.x() + R.m12() * diffxyz.y() + R.m13() * diffxyz.z()
        y = R.m21() * diffxyz.x() + R.m22() * diffxyz.y() + R.m23() * diffxyz.z()
        z = R.m31() * diffxyz.x() + R.m32() * diffxyz.y() + R.m33() * diffxyz.z()

        enu = QtGui.QVector3D(x, y, z)

        return enu

    @staticmethod
    def xyz2enu_2(xyz, refLLA):
        return Conversions.xyz2enu_4_LLA(xyz,
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def xyz2enu_6(x, y, z, reflat, reflon, refalt):
        return Conversions.xyz2enu_4_re(QtGui.QVector3D(x, y, z),
                                        reflat,
                                        reflon,
                                        refalt)

    @staticmethod
    def xyz2enu_4_LLA(x, y, z, refLLA):
        return Conversions.xyz2enu_4_LLA(QtGui.QVector3D(x, y, z),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2xyz_4_re(enu, reflat, reflon, refalt):
        R1 = Conversions.rot(90.0 + reflon, 3)
        R2 = Conversions.rot(90.0 - reflat, 1)
        R = R2 * R1

        invR = R.inverted()
        if invR.isIdentity():
            QtCore.qWarning(b"Failed to invert rotation matrix --- did you enter a bad lat,lon,or alt?")
            return enu

        x = invR.m11() * enu.x() + invR.m12() * enu.y() + invR.m13() * enu.z()
        y = invR.m21() * enu.x() + invR.m22() * enu.y() + invR.m23() * enu.z()
        z = invR.m31() * enu.x() + invR.m32() * enu.y() + invR.m33() * enu.z()

        diffxyz = QtGui.QVector3D(x, y, z)

        refxyz = Conversions.lla2xyz_3(reflat, reflon, refalt)

        return diffxyz + refxyz

    @staticmethod
    def enu2xyz_2(enu, refLLA):
        return Conversions.enu2xyz_4_re(enu,
                                        refLLA.latitude(),
                                        refLLA.longitude(),
                                        refLLA.altitude())

    @staticmethod
    def enu2xyz_4_LLA(east, north, up, refLLA):
        return Conversions.enu2xyz_4_LLA(QtGui.QVector3D(east, north, up),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2lla_4_re(enu, reflat, reflon, refalt):
        xyz = Conversions.enu2xyz_4_re(enu, reflat, reflon, refalt)
        return Conversions.xyz2lla(xyz)

    @staticmethod
    def enu2lla_2(enu, refLLA):
        return Conversions.enu2lla_4_LLA(enu,
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2lla_6(east, north, up, reflat, reflon, refalt):
        return Conversions.enu2lla_4_re(QtGui.QVector3D(east, north, up),
                                        reflat,
                                        reflon,
                                        refalt)

    @staticmethod
    def enu2lla_4_LLA(east, north, up, refLLA):
        return Conversions.enu2lla_4_LLA(QtGui.QVector3D(east, north, up),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def lla2enu_6(lat, lon, alt, reflat, reflon, refalt):
        xyz = Conversions.lla2xyz_3(lat, lon, alt)
        enu = Conversions.xyz2enu_4_re(xyz, reflat, reflon, refalt)

        return enu

    @staticmethod
    def lla2enu_4_LLA(lat, lon, alt, refLLA):
        return Conversions.lla2enu_6(lat, lon, alt,
                                     refLLA.latitude(),
                                     refLLA.longitude(),
                                     refLLA.altitude())

    @staticmethod
    def lla2enu_4_re(lla, reflat, reflon, refalt):
        return Conversions.lla2enu_6(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude(),
                                     reflat,
                                     reflon,
                                     refalt)

    @staticmethod
    def lla2enu_2(lla, refLLA):
        return Conversions.lla2enu_6(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude(),
                                     refLLA.latitude(),
                                     refLLA.longitude(),
                                     refLLA.altitude())

    @staticmethod
    def degreesLatPerMeter(latitude):
        latRad = latitude * (pi / 180.0)
        meters = 111132.954 - 559.822 * math.cos(2.0 * latRad) + 1.175 * math.cos(4.0 * latRad)
        return 1.0 / meters

    @staticmethod
    def degreesLonPerMeter(latitude):
        latRad = latitude * (pi / 180.0)
        meters = (pi * A_EARTH * math.cos(latRad)) / (180.0 * math.sqrt(1.0 - NAV_E2 * pow(math.sin(latRad), 2.0)))
        return 1.0 / meters

    @staticmethod
    def rot(angle, axis):
        toRet = QtGui.QTransform()

        cang = math.cos(angle * deg2rad)
        sang = math.sin(angle * deg2rad)

        if axis == 1:
            toRet.setMatrix(1.0, 0.0, 0.0, 0.0, cang, sang, 0.0, -1 * sang, 1.0)
        elif axis == 2:
            toRet.setMatrix(cang, 0.0, -1 * sang, 0.0, 1.0, 0.0, sang, 0.0, cang)
        elif axis == 3:
            toRet.setMatrix(cang, sang, 0.0, -1 * sang, cang, 0.0, 0.0, 0.0, 1.0)
        else:
            QtCore.qWarning(b"Wrong axis")

        return toRet

    @staticmethod
    def test():
        from MapGraphics.Position import Position
        byu1 = Position(QtCore.QPointF(-111.649253, 40.249707), 1423)
        del Position
        xyz = Conversions.lla2xyz(byu1)
        byu2 = Conversions.xyz2lla(xyz)

        if QtCore.qAbs(byu2.longitude() - byu1.longitude()) > 0.001 or QtCore.qAbs(
                byu2.latitude() - byu1.latitude()) > 0.001 or QtCore.qAbs(byu2.altitude() - byu1.altitude()) > 1.0:
            QtCore.qDebug(b"Failed LLA -> XYZ -> LLA")
        else:
            QtCore.qDebug(b"Passed LLA -> XYZ -> LLA")

        enu1 = QtGui.QVector3D(5, 5, 0)
        byu3 = Conversions.enu2lla_2(enu1, byu1)
        enu3 = Conversions.lla2enu_2(byu3, byu1)

        if (enu3 - enu1).length() > 0.3:
            QtCore.qDebug(b"Failed LLA -> ENU -> LLA -> ENU")
        else:
            QtCore.qDebug(b"Passed LLA -> ENU -> LLA -> ENU")

        QtCore.qDebug(bytes(str(Conversions.degreesLatPerMeter(15.0))))
        QtCore.qDebug(bytes(str(Conversions.degreesLonPerMeter(15.0))))
