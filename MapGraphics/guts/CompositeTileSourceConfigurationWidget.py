from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QItemSelectionModel, QModelIndex, QAbstractItemModel

from MapGraphics.guts.MapTileSourceDelegate import MapTileSourceDelegate
from MapGraphics.guts.MapTileLayerListModel import MapTileLayerListModel
from MapGraphics.guts.CompositeTileSourceConfigurationWidgetUi import Ui_CompositeTileSourceConfigurationWidget
from MapGraphics.tileSources.OSMTileSource import OSMTileSource
from MapGraphics.tileSources.CompositeTileSource import CompositeTileSource


class CompositeTileSourceConfigurationWidget(QWidget):
    currentChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, composite, parent=None):
        QWidget.__init__(self, parent, None)
        self.__ui = Ui_CompositeTileSourceConfigurationWidget()
        self.__composite = CompositeTileSource(composite)
        self.__ui.setupUi(self)
        self.init()

    def __del__(self):
        pass

    def setComposite(self, nComposite):
        self.__composite = nComposite
        self.init()

    def handleCurrentSelectionChanged(self, current, previous):
        enableGUI = current.isValid()

        self.__ui.removeSourceButton.setEnabled(enableGUI)
        self.__ui.opacitySlider.setEnabled(enableGUI)

        if self.__composite is None:
            return

        self.__ui.moveDownButton.setEnabled(enableGUI and (self.__composite.numSources() - 1) > current.row())
        self.__ui.moveUpButton.setEnabled(enableGUI and 0 < current.row())

        if enableGUI:
            opacityFloat = self.__composite.getOpacity(current.row())
            self.__ui.opacitySlider.setValue(opacityFloat * 100)

    def handleCompositeChange(self):
        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())
        index = QModelIndex(selModel.currentIndex())

        if self.__composite is None:
            return

        opacityFloat = self.__composite.getOpacity(index.row())
        self.__ui.opacitySlider.setValue(opacityFloat * 100)

    def addOSMTileLayer(self):
        if self.__composite is None:
            return

        source = OSMTileSource(OSMTileSource.OSMTileType.OSMTiles)
        self.__composite.addSourceTop(source)

    def on_removeSourceButton_clicked(self):
        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())
        index = QModelIndex(selModel.currentIndex())

        if self.__composite is None:
            return

        self.__composite.removeSource(index.row())

        selModel.clear()

    def on_opacitySlider_valueChanged(self, value):
        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())
        index = QModelIndex(selModel.currentIndex())

        if not index.isValid():
            return
        if self.__composite is None:
            return

        opacityFloat = value / 100.0
        self.__composite.setOpacity(index.row(), opacityFloat)

    def on_moveDownButton_clicked(self):
        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())
        index = QModelIndex(selModel.currentIndex())

        if not index.isValid():
            return
        if self.__composite is None:
            return

        numberOfLayers = self.__composite.numSources()
        currentIndex = index.row()
        desiredIndex = min(numberOfLayers - 1, currentIndex + 1)
        self.__composite.moveSource(currentIndex, desiredIndex)
        selModel.setCurrentIndex(selModel.model().index(desiredIndex, 0), QItemSelectionModel.SelectCurrent)

    def on_moveUpButton_clicked(self):
        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())
        index = QModelIndex(selModel.currentIndex())

        if not index.isValid():
            return
        if self.__composite is None:
            return

        currentIndex = index.row()
        desiredIndex = max(0, currentIndex - 1)
        self.__composite.moveSource(currentIndex, desiredIndex)
        selModel.setCurrentIndex(selModel.model().index(desiredIndex, 0), QItemSelectionModel.SelectCurrent)

    def init(self):
        delegato = MapTileSourceDelegate(self.__composite, self)
        model = MapTileLayerListModel(self.__composite, self)

        oldModel = QAbstractItemModel(self.__ui.listView.model())
        oldDelegate = QAbstractItemDelegate(self.__ui.listView.itemDelegate())

        self.__ui.listView.setModel(model)
        self.__ui.listView.setItemDelegate(delegato)

        # if (oldModel != 0)
        #     delete
        #     oldModel;
        # if (oldDelegate != 0)
        #     delete
        #     oldDelegate;

        selModel = QItemSelectionModel(self.__ui.listView.selectionModel())

        self.currentChanged.connect(self.handleCurrentSelectionChanged)
        # connect(selModel,
        #         SIGNAL(currentChanged(QModelIndex, QModelIndex)),
        #         this,
        #         SLOT(handleCurrentSelectionChanged(QModelIndex, QModelIndex)));

        menu = QMenu(self.__ui.addSourceButton)
        openStreetMapTilesAction = QAction("OpenStreetMap Tiles", self)
        openStreetMapTilesAction.triggered.connect(self.addOSMTileLayer)
        menu.addAction(openStreetMapTilesAction)  # SLOT(addOSMTileLayer())
        self.__ui.addSourceButton.setMenu(menu)
