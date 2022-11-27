from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QDMGraphicsEdge(QGraphicsPathItem):


    def __init__(self, edge, parent = None):
        super().__init__(parent)
        self.edge = edge
        self._color = QColor("#747273")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        self._pen.setWidthF(3)
        self._pen_selected.setWidthF(4)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget: None):
        self.updatePath()
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        # Va a calcular la ruta desde un punto A a un B
        raise NotImplemented("Este método será sobreescrito en la implementación de los hijos")

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= -1


        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(
            s[0]+dist, s[1],
            d[0] - dist, d[1],
            self.posDestination[0], self.posDestination[1]
        )
        self.setPath(path)
