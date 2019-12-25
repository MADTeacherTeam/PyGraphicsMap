from PyQt5 import QtCore


class MapGraphicsScene(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        # self.objects = []
        self.__objects = set()

    def addObject(self, object):
        if object == 0:
            return

        self.__objects.add(object)
        print('add Object')
        # generate signal object added
        pass

    def removeObject(self, object):
        print('remove Object')
        self.__objects.remove(object)
        # generate object remove
        pass

    def slot_handleNewObjectGenerated(self, newObject):
        print('handleNewObjectGenerated')
        self.addObject(newObject)
        pass

    def slot_handleObjectDestroyed(self, object):
        self.removeObject(object)
        pass

    def __del__(self):
        self.__objects.clear()
