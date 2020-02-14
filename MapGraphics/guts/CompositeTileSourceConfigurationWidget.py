from MapGraphics.guts.CompositeTileSourceConfigurationWidget_ui import Ui_CompositeTileSourceConfigurationWidget
from PySide2.QtWidgets import QWidget, QMenu


class CompositeTileSourceConfigurationWidget(QWidget):
    def __init__(self, parent=0):
        super().__init__(parent)
        self.ui = Ui_CompositeTileSourceConfigurationWidget()
        self.ui.setupUi(self)

