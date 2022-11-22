from node_graphics_node import QDMGraphicsNode

class Node():
    def __init__(self, scene, titulo = "Nodo Morion"):
        self.scene = scene
        self.titulo = titulo

        self.gNode = QDMGraphicsNode(self, self.titulo)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.gNode)

        self.inputs = []
        self.outputs = []



