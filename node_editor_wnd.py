from PyQt5.QtWidgets import *
from node_graphics_scene import QDMGraphicsScene


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        #Crear graficos de la escena
        self.grScene = QDMGraphicsScene()

        # Crear vista de graficos
        self.view = QGraphicsView(self)
        self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("PDI Nodos")
        self.show()