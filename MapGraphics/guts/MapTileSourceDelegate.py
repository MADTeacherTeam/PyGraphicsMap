from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from MapGraphics.tileSources.CompositeTileSource import CompositeTileSource


class MapTileSourceDelegate(QStyledItemDelegate):
    def __init__(self, composite, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.__composite = composite

    def paint(self, painter, option, index):
        if self.__composite is None:
            return

        childSource = self.__composite.getSource(index.row())
        if childSource is None:
            return

        painter.save()

        palette = QPalette(option.palette)
        rect = QRect(option.rect)
        rect.setWidth(rect.width() - 2)

        backgroundBrush = QBrush(palette.base())
        borderColor = palette.text().color()
        textColor = palette.text().color()
        if option.state and QStyle.State_Selected:
            backgroundBrush = palette.highlight()

        painter.fillRect(rect, backgroundBrush)

        painter.setPen(borderColor)
        painter.drawRect(rect)

        nameFont = QFont(painter.font())
        otherFont = QFont(painter.font())
        nameFont.setPointSize(nameFont.pointSize() + 2)
        nameFont.setBold(True)

        textRect = rect
        textRect.adjust(1, 0, -1, 0)
        nameString = childSource.name()
        painter.setPen(textColor)
        painter.setFont(nameFont)

        painter.drawText(textRect, nameString, QTextOption(Qt.AlignLeft | Qt.AlignTop))

        opacityString = "Opacity: " + str(self.__composite.getOpacity(index.row())).format('f', 2)
        painter.setPen(textColor)
        painter.setFont(otherFont)
        painter.drawText(textRect, opacityString, QTextOption(Qt.AlignLeft | Qt.AlignVCenter))

        state = "Enabled"
        if not self.__composite.getEnabledFlag(index.row()):
            state = "Disabled"
        stateString = "Status: " + state
        painter.setPen(textColor)
        painter.setFont(otherFont)
        painter.drawText(textRect, stateString, QTextOption(Qt.AlignLeft | Qt.AlignBottom))

        painter.restore()

    def sizeHint(self, option, index):
        toRet = QSize()
        toRet.setWidth(150)
        toRet.setHeight(50)

        return toRet
