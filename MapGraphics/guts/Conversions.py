from PyQt5 import QtCore
import math
import numpy as np

pi = 3.141592653589793238462643383
A_EARTH = 6378137
flattening = 1.0/298.257223563
NAV_E2 = (2.0-flattening)*flattening
deg2rad = pi/180.0
rad2deg = 180.0/pi


class Conversions:
    def lla2xyz(self, wlat, wlon, walt):
        toRet = []

        if wlat < -90.0 or wlat > 90.0 or wlon < -180.0 or wlon > 180.0:
            print('Lat/Lon out of range', wlat, wlon)
            return toRet

        slat = math.sin(wlat*deg2rad)
        clat = math.cos(wlat*deg2rad)
        r_n = A_EARTH/math.sqrt(1.0 - NAV_E2*slat*slat)

        toRet.append((r_n + walt)*clat*math.cos(wlon*deg2rad))
        toRet.append((r_n + walt)*clat*math.sin(wlon*deg2rad))
        toRet.append((r_n*(1.0 - NAV_E2) + walt)*slat)

        return toRet

    def lla2xyz(self, lla):
        return self.lla2xyz(lla.latitude(),
                            lla.longitude(),
                            lla.altitude())

    def xyz2lla(self, v):
        return self.xyz2lla()

    # def xyz2lla(self, x, y, z):
