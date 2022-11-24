from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.radio = 6
        self.outline_width = 2
        self._color_background = QColor("#FFFF7700")
        self._color_outline = QColor("FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        #Pintar el circulo
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radio, -self.radio, 2*self.radio, 2*self.radio)

    def boundingRect(self):
        return QRectF(
            -self.radio - self.outline_width,
            -self.radio - self.outline_width,
            2*(self.radio+self.outline_width),
            2*(self.radio+self.outline_width)
        )