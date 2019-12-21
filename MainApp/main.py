from PyQt5 import QtWidgets
from MainApp.MainWindow import Ui_MainWindow
import sys


class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


app = QtWidgets.QApplication([])
application = myWindow()
application.show()

sys.exit(app.exec())
