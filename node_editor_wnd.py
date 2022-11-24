from PyQt5.QtWidgets import *
from node_graphics_view import QDMGraphicsView
from node_socket import Socket
from node_node import Node
from diccionario import Diccionario
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from node_scene import Scene

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dic = Diccionario()

        self.stylesheet_filename = "qss/nodestyle.qss"
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()
    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        #Crear graficos de la escena
        self.scene = Scene()
        #self.grScene = self.scene.grScene

        node = Node(self.scene, "Morion Nodo", inputs=[1, 2, 3], outputs=[1])
        #node = Node(self.scene, "Morion Nodo", inputs=[], outputs=[])

        # Crear vista de graficos
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle(self.dic.tituloVentana) # Poner el título a la ventana desde el Diccionario
        self.show()

        #self.addDebugContent()


    def addDebugContent(self):
        verde = QBrush(Qt.green)
        oultLine = QPen(Qt.black)
        oultLine.setWidth(3)
        rect = self.grScene.addRect(-100, -100, 80, 100,  oultLine, verde)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)

        rect2 = self.grScene.addRect(-100, -100, 80, 100,  oultLine, QBrush(Qt.red))
        rect2.setFlag(QGraphicsItem.ItemIsMovable)
        rect2.setFlag(QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))