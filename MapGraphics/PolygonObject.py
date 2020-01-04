from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import pyqtSignal
from .MapGraphicsObject import MapGraphicsObject
from .Position import Position
from .guts import Conversions

class posChanged(QtCore.QObject):
    signalPosChanged=pyqtSignal()

class PolygonObject(MapGraphicsObject):
    def __init__(self,geoPoly,fillColor,parent):
        super.__init__(parent)
        self.newObjectGenerated=pyqtSignal
        self.__geoPoly=geoPoly
        self.__fillColor=fillColor
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable,False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable)
        self.setGeoPoly()
        self.__editCircles=[]
        self.__addVertexCircles=[]

    def __del__(self):
        QtCore.qDebug(self+"destroying")
        for each in self.__editCircles:
            self.destroyEditCircle(each)
        self.__editCircles.clear()

    def boundingRect(self):
        latLonRect=self.__geoPoly.boundingRect()
        latLonCenter=latLonRect.center()
        latLonCenterPos=Position()
        latLonCenterPos.constr_two_arg(latLonCenter,0.0)
        topLeftPos=Position()
        topLeftPos.constr_two_arg(latLonRect.topLeft(),0.0)
        bottomRightPos=Position()
        bottomRightPos.constr_two_arg(latLonRect.bottomRight(),0.0)
        topLeftENU=Conversions.lla2xyz(topLeftPos,latLonCenterPos).toPointF()
        bottomRightENU=Conversions.lla2enu(bottomRightPos,latLonCenterPos).toPointF()
        return QtCore.QRectF(topLeftENU,bottomRightENU)

    def contains(self,geoPos):
        return self.__geoPoly.containsPoint(geoPos,QtCore.Qt.OddEvenFill)

    def paint(self,painter,option,widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing,True)
        enuPoly=QtGui.QPolygonF()
        latLonCenterPos=Position()
        latLonCenterPos.constr_two_arg(self.__geoPoly.boundingRect().center(),0)
        for latLon in self.__geoPoly:
            latLonPos=Position()
            latLonPos.constr_two_arg(latLon,0)
            enu=Conversions.lla2enu(latLonPos,latLonCenterPos).toPointF()
            enuPoly<<enu
        painter.setBrush(self.__fillColor)
        painter.drawPolygon(enuPoly)
        if not self.__editCircles:
            for i in range(self.__geoPoly.size()):
                circle=self.constructEditCircle()
                circle.setPos(self.__geoPoly.at(i))
                self.__editCircles.append(circle)

                current=self.__geoPoly.at(i)
                next=self.__geoPoly.at((i+1)%self.__geoPoly.size())
                avg=QtCore.QPointF((current.x() + next.x())/2,(current.y()+next.y()/2))
                betweener=self.__constructAddVertexCircle()
                betweener.setPos(avg)
                self.__addVertexCircles.append(betweener)


    def setPos(self,nPos):
        if nPos!=self.__geoPoly.boundingRect().center():
            diff=nPos-self.pos()
            for circle in self.__editCircles:
                circle.setPos(circle.pos()+diff)
            self.__fixAddVertexCirclePos()
        self.setPos(nPos)
        #self.comunicate=posChanged()
        #self.comunicate.signalPosChanged=
        #self.communicate.signalPosChanged.emit()

    def __fixAddVertexCirclePos(self):
        for i in range(self.__geoPoly.size()):
            current=self.__geoPoly.at(i)
            next=self.__geoPoly.at((i+1)% self.__geoPoly.size())
            avg=QtCore.QPointF((current.x() + next.x())/2.0,(current.y() + next.y())/2.0)
            self.__addVertexCircles.at(i).setPos(avg)

    def pos(self):
        return self.__pos
    def __constructAddVertexCircle(self):
        toRet=CircleObject(3,True,QtGui.QColor(100,100,100,255))
        toRet.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable,False)
        toRet.selectedChanged.connect(self.__handleAddVertexCircleSelected())
        self.newObjectGenerated(toRet)
        toRet.setToolTip("Single-click (don't drag!) to add vertex.")
        return toRet



    def constructEditCircle(self):
        toRet=CircleObject(8)
        toRet.posChanged.connect(self.handleEditCirclePosChanged())
        toRet.destroyed.connect(self.__handleEditCircleDestroyed())
        self.newObjectGenerated(toRet).emit()
        return  toRet
    def destroyEditCircle(self,obj):
        obj.posChanged.disconnect()
        obj.destroyed.disconnect()
        obj.deleteLater()

    def setGeoPoly(self,newPoly):
        if newPoly==self.__geoPoly:
            return
        self.__geoPoly=newPoly
        for obj in self.__editCircles:
            self.destroyEditCircle(obj)
        for obj in self.__addVertexCircles:
            self.__destroyAddVertexCircle(obj)
        self.__editCircles.clear()
        self.__addVertexCircles.clear()
        self.setPos(newPoly.boundingRect().center())
        self.polygonChanged(newPoly)

    def setFillColor(self,color):
        if self.__fillColor==color:
            return
        self.__fillColor=color
        #SIGNAL redrawRequested
    def mousePressEvent(self,ev):
        geoPos=ev.scenePos()
        if self.__geoPoly.containsPoint(geoPos,QtCore.Qt.OddEvenFill):
            self.mousePressEvent(ev)
        else:
            ev.ignore()
    def keyReleaseEvent(self,event):
        if(event.matches(QtGui.QKeySequence.Delete)):
            self.deleteLater()
            event.accept()
        else:
            event.ignore()

    def handleEditCirclePosChanged(self):
        sender=QtCore.QObject.sender()
        if sender==0:
            return
        circle=sender
        if circle==0:
            return
        if circle not in self.__editCircles:
            return
        index=self.__editCircles.index(circle)
        newPos=circle.pos()
        self.__geoPoly.replace(index,newPos)
        self.setPos(self.__geoPoly.boundingRect().center())
        self.__fixAddVertexCirclePos()
        #SIGNAL this->polygonChanged(this->geoPoly())

    def __handleAddVertexCircleSelected(self):
        sender=QtCore.QObject.sender()
        if sender==0:
            return
        circle=sender
        if circle==0:
            return
        if not circle.isSelected():
            return
        circle.setSelected(False)
        geoPos=circle.pos()
        if circle not in self.__addVertexCircles:
            return
        index=self.__addVertexCircles.index(circle)
        index+=1
        self.__geoPoly.insert(index,geoPos)
        editCircle=self.__constructEditCircle()
        editCircle.setPos(geoPos)
        self.__editCircles.insert(index,editCircle)
        editCircle.setSelected(True)
        addVertexCircle=self.__constructAddVertexCircle()
        current=self.__geoPoly.at(index-1)
        next=self.__geoPoly.at(index)
        avg=QtCore.QPointF((current.x() + next.x())/2.0,(current.y() + next.y())/2.0)
        addVertexCircle.setPos(avg)
        self.__addVertexCircles.insert(index,addVertexCircle)
        self.__fixAddVertexCirclePos()
        #SIGNAL polygonChanged(this->geoPoly());

    def __handleEditCircleDestroyed(self):
        sender=QtCore.QObject.sender()
        if sender==0:
            QtCore.qWarning("Can't process desyroyed edit circle. Sender is null")
            return
        circle=sender
        if circle not in self.__editCircles:
            QtCore.qWarning("Can't process destroyed edit circle. Not contained in edit circle list")
            return
        index=self.__editCircles.index(circle)
        self.__geoPoly.remove(index)
        self.__editCircles.remove(circle)
        self.__addVertexCircles.pop(index).deleteLater()
        self.__fixAddVertexCirclePos()
        # SIGNAL redrawRequested
        self.setPos(self.__geoPoly.boundingRect().center())

    def __destroyAddVertexCircle(self,obj):
        obj.selectedChanged.disconnect()
        obj.deleteLater()
    def geoPoly(self):
        return self.__geoPoly