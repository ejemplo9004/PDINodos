from node_graphics_scene import QDMGraphicsScene

class Scene():
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.ancho, self.alto = 64000, 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.ancho, self.alto)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

