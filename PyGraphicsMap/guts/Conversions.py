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
        """convert latitude, longitude, altitude to QVector3D(XYZ)"""
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
        """convert QVector3D(latitude, longitude, altitude) to  QVector3D(XYZ)"""
        return Conversions.lla2xyz_3(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude())

    @staticmethod
    def xyz2lla(v):
        """convert QVector3D(XYZ) to QVector3D(latitude, longitude, altitude)"""
        return Conversions.xyz2lla_3(v.x(), v.y(), v.z())

    @staticmethod
    def xyz2lla_3(x, y, z):
        """convert X, Y, Z to Position"""
        # пока так
        from PyGraphicsMap.Position import Position
        toRet = Position()
        del Position
        toRet.setAltitude(0.0)

        if x == 0.0 and y == 0.0 and z == 0.0:
            print("Error: XYZ at center of the earth")
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
        """convert QVector3D(XYZ), reflat, reflon, refalt to QVector3d(enu)"""
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
        """convert QVector3D(XYZ), Position to QVector3d(enu)"""
        return Conversions.xyz2enu_4_LLA(xyz,
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def xyz2enu_6(x, y, z, reflat, reflon, refalt):
        """convert X, Y, Z, reflat, reflon, refalt to to QVector3d(enu)"""
        return Conversions.xyz2enu_4_re(QtGui.QVector3D(x, y, z),
                                        reflat,
                                        reflon,
                                        refalt)

    @staticmethod
    def xyz2enu_4_LLA(x, y, z, refLLA):
        """"convert X, Y, Z, Position to QVector3d(enu)"""
        return Conversions.xyz2enu_4_LLA(QtGui.QVector3D(x, y, z),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2xyz_4_re(enu, reflat, reflon, refalt):
        """convert enu, reflat, reflon, refalt to QVector3D(XYZ)"""
        R1 = Conversions.rot(90.0 + reflon, 3)
        R2 = Conversions.rot(90.0 - reflat, 1)
        R = R2 * R1

        invR = R.inverted()
        invR = invR[0]
        if invR.isIdentity():
            print("Failed to invert rotation matrix --- did you enter a bad lat,lon,or alt?")
            return enu

        x = invR.m11() * enu.x() + invR.m12() * enu.y() + invR.m13() * enu.z()
        y = invR.m21() * enu.x() + invR.m22() * enu.y() + invR.m23() * enu.z()
        z = invR.m31() * enu.x() + invR.m32() * enu.y() + invR.m33() * enu.z()

        diffxyz = QtGui.QVector3D(x, y, z)

        refxyz = Conversions.lla2xyz_3(reflat, reflon, refalt)

        return diffxyz + refxyz

    @staticmethod
    def enu2xyz_2(enu, refLLA):
        """convert enu, Position to QVector3D(XYZ)"""
        return Conversions.enu2xyz_4_re(enu,
                                        refLLA.latitude(),
                                        refLLA.longitude(),
                                        refLLA.altitude())

    @staticmethod
    def enu2xyz_4_LLA(east, north, up, refLLA):
        """covert east, north, up, Position to QVector3D(XYZ)"""
        return Conversions.enu2xyz_4_LLA(QtGui.QVector3D(east, north, up),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2lla_4_re(enu, reflat, reflon, refalt):
        """convert enu, reflat, reflon, refalt to Position"""
        xyz = Conversions.enu2xyz_4_re(enu, reflat, reflon, refalt)
        return Conversions.xyz2lla(xyz)

    @staticmethod
    def enu2lla_2(enu, refLLA):
        """convert enu, Position to Position"""
        return Conversions.enu2lla_4_LLA(enu,
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def enu2lla_6(east, north, up, reflat, reflon, refalt):
        """convert east, north, up, reflat, reflon, refalt to Posiition"""
        return Conversions.enu2lla_4_re(QtGui.QVector3D(east, north, up),
                                        reflat,
                                        reflon,
                                        refalt)

    @staticmethod
    def enu2lla_4_LLA(east, north, up, refLLA):
        """convert east, north, up,Position to Position"""
        return Conversions.enu2lla_4_re(QtGui.QVector3D(east, north, up),
                                         refLLA.latitude(),
                                         refLLA.longitude(),
                                         refLLA.altitude())

    @staticmethod
    def lla2enu_6(lat, lon, alt, reflat, reflon, refalt):
        """convert lat, lon, alt, reflat, reflon, refalt to QVector3D(enu)"""
        xyz = Conversions.lla2xyz_3(lat, lon, alt)
        enu = Conversions.xyz2enu_4_re(xyz, reflat, reflon, refalt)

        return enu

    @staticmethod
    def lla2enu_4_LLA(lat, lon, alt, refLLA):
        """convert lat, lon, alt, Position to QVector3D(enu)"""
        return Conversions.lla2enu_6(lat, lon, alt,
                                     refLLA.latitude(),
                                     refLLA.longitude(),
                                     refLLA.altitude())

    @staticmethod
    def lla2enu_4_re(lla, reflat, reflon, refalt):
        """convert Position, reflat, reflon, refalt to QVector3D(enu)"""
        return Conversions.lla2enu_6(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude(),
                                     reflat,
                                     reflon,
                                     refalt)

    @staticmethod
    def lla2enu_2(lla, refLLA):
        """convert Position(lla), Position(refLLA) to QVector3D(enu)"""
        return Conversions.lla2enu_6(lla.latitude(),
                                     lla.longitude(),
                                     lla.altitude(),
                                     refLLA.latitude(),
                                     refLLA.longitude(),
                                     refLLA.altitude())

    @staticmethod
    def degreesLatPerMeter(latitude):
        """convert Latitude degrees to metres"""
        latRad = latitude * (pi / 180.0)
        meters = 111132.954 - 559.822 * math.cos(2.0 * latRad) + 1.175 * math.cos(4.0 * latRad)
        return 1.0 / meters

    @staticmethod
    def degreesLonPerMeter(latitude):
        """convert Longitude degrees to metres"""
        latRad = latitude * (pi / 180.0)
        meters = (pi * A_EARTH * math.cos(latRad)) / (180.0 * math.sqrt(1.0 - NAV_E2 * pow(math.sin(latRad), 2.0)))
        return 1.0 / meters

    @staticmethod
    def rot(angle, axis):
        """convert angle, axis to QTransform"""
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
            print("Wrong axis")

        return toRet