import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from node_socket import RIGT_TOP, RIGTH_BOTTOM, LEFT_BOTTOM, LEFT_TOP

EDGE_CP_ROUNDNESS = 100
class QDMGraphicsEdge(QGraphicsPathItem):

    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge
        # self._color = QColor("#747273")
        # self._color_selected = QColor("#00ff00")
        _colorActual = edge.start_socket.grScoket.getColor()
        self._color = _colorActual
        self._pen_dragging = QPen(_colorActual)
        self._pen_dragging.setStyle(Qt.DotLine)
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        self._pen.setWidthF(2)
        self._pen_selected.setWidthF(1)
        self._pen_dragging.setWidthF(1)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget= None):
        self.setPath(self.calcPath())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def intersectsWith(self, p1, p2):
        cutPath = QPainterPath(p1)
        cutPath.lineTo(p2)
        path = self.calcPath()
        return cutPath.intersects(path)

    def calcPath(self):
        # Va a calcular la ruta desde un punto A a un B
        raise NotImplemented("Este método será sobreescrito en la implementación de los hijos")


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path



class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calcPath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (RIGT_TOP, RIGTH_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_TOP, LEFT_BOTTOM)):
            cpx_s *= -1
            cpx_d *= -1

            cpy_d = ((s[1] - d[1])/math.fabs((s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.0001)) * EDGE_CP_ROUNDNESS
            cpy_s = ((d[1] - s[1])/math.fabs((d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.0001)) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(
            s[0] + cpx_s, s[1] + cpy_s,
            d[0] + cpx_d, d[1] + cpy_d,
            self.posDestination[0], self.posDestination[1]
        )
        return path
