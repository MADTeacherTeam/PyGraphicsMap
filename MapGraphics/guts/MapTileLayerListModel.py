from PySide2.QtGui import *
from PySide2.QtCore import *

from MapGraphics.tileSources.CompositeTileSource import CompositeTileSource


class MapTileLayerListModel(QAbstractListModel):
    def __init__(self, composite, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.__composite = composite

        if self.__composite is None:
            return
        raw = self.__composite

        raw.sourcesChanged.connect(self.handleCompositeSourcesChanged)
        raw.sourceAdded.connect(self.handleCompositeSourcesAdded)
        raw.sourceRemoved.connect(self.handleCompositeSourcesRemoved)
        # connect(raw,
        #         SIGNAL(sourcesChanged()),
        #         this,
        #         SLOT(handleCompositeSourcesChanged()));
        # connect(raw,
        #         SIGNAL(sourceAdded(int)),
        #         this,
        #         SLOT(handleCompositeSourcesAdded(int)));
        # connect(raw,
        #         SIGNAL(sourceRemoved(int)),
        #         this,
        #         SLOT(handleCompositeSourcesRemoved(int)));

    def rowCount(self, parent=QModelIndex()):
        # Q_UNUSED(parent);
        if self.__composite is None:
            return
        return self.__composite.numSources()

    def data(self, index, role=Qt.DisplayRole):
        # TODO QVariant comment for run
        # if not index.isValid():
        #     return "Invalid index"
        # if index.row() >= self.rowCount():
        #     return QVariant("Index out of bounds")
        # if self.__composite is None:
        #     return QVariant("Null composite")
        #
        # if role == Qt.DisplayRole:
        #     i = index.row()
        #     tileSource = self.__composite.getSource(i)
        #     if tileSource is None:
        #         return QVariant("Error: Null source")
        #     else:
        #         return tileSource.name()
        # else:
        #     return QVariant()
        pass

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def handleCompositeSourcesChanged(self):
        topleft = self.index(0)
        bottomright = self.index(self.rowCount())
        self.dataChanged(topleft, bottomright)

    def handleCompositeSourcesAdded(self, index):
        self.beginInsertRows(QModelIndex(), index, index)
        self.endInsertRows()

    def handleCompositeSourcesRemoved(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self.endRemoveRows()
