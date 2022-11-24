from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, nodo, parent=None):
        super().__init__(parent)
        self.node = nodo
        self.content = self.node.content

        self._titulo_color = Qt.white
        self._titulo_font = QFont("Ubuntu", 10)


        self.width = 190
        self.height = 240
        self.edge_size = 10
        self.title_heigth = 26
        self._padding = 10.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFF8637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#DD121212"))

        #Iniciar título
        self.initTitulo()
        self.titulo = self.node.titulo

        #Iniciar Sockets
        self.initSockets()

        #Iniciar contenido
        self.initContent()

        self.initUI()


    @property
    def titulo(self): return self._titulo
    @titulo.setter
    def titulo(self, valor):
        self._titulo = valor
        self.titulo_item.setPlainText(self._titulo)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitulo(self):
        self.titulo_item = QGraphicsTextItem(self)
        self.titulo_item.setDefaultTextColor(self._titulo_color)
        self.titulo_item.setFont(self._titulo_font)
        self.titulo_item.setPos(self._padding,0)
        self.titulo_item.setTextWidth(
            self.width - 2 * self._padding
        )

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            self.edge_size,
            self.title_heigth + self.edge_size,
            self.width - 2*self.edge_size,
            self.height - 2 * self.edge_size - self.title_heigth
        )
        self.grContent.setWidget(self.content)

    def initSockets(self):
        pass


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        #Titulo
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_heigth, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_heigth- self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_heigth- self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        #Contenido
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_heigth, self.width, self.height - self.title_heigth, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_heigth, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_heigth, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        #Outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size) #Color del borde seleccionado o no
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
