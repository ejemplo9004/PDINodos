import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # Configuracion
        self.tamCuadricula = 20
        self.cuadrosCuadricula = 5
        self.colorFondo = QColor("#1D1E23")
        self.colorDelgado = QColor("#18191D")
        self.colorGrueso = QColor("#0C0E0C")

        self.lapizDelgado = QPen(self.colorDelgado)
        self.lapizDelgado.setWidth(1)
        self.lapizGrueso = QPen(self.colorGrueso)
        self.lapizGrueso.setWidth(2)

        self.setBackgroundBrush(self.colorFondo)

    def setGrScene(self, ancho, alto):
        self.setSceneRect(-ancho // 2, -alto // 2, ancho, alto)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        # aca creo la cuadricula
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        firstLeft = left - (left % self.tamCuadricula)
        firstTop = top - (top % self.tamCuadricula)

        # Calcular todas las lineas a dibujar
        lineasDelgadas, lineasGruesas = [], []
        for x in range(firstLeft, right, self.tamCuadricula):
            if x % (self.tamCuadricula*self.cuadrosCuadricula) != 0:
                lineasDelgadas.append(QLine(x, top, x, bottom))
            else:
                lineasGruesas.append(QLine(x, top, x, bottom))

        for y in range(firstTop, bottom, self.tamCuadricula):
            if y % (self.tamCuadricula*self.cuadrosCuadricula) != 0:
                lineasDelgadas.append(QLine(left, y, right, y))
            else:
                lineasGruesas.append(QLine(left, y, right, y))

        # Digujar las lineas
        painter.setPen(self.lapizDelgado)
        painter.drawLines(*lineasDelgadas)

        painter.setPen(self.lapizGrueso)
        painter.drawLines(*lineasGruesas)
