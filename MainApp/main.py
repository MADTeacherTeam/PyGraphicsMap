from PyQt5 import QtWidgets
from MainApp.MainWindow import Ui_MainWindow
import sys
from MapGraphics.MapGraphicsScene import MapGraphicsScene


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())
