from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
class Node():
    def __init__(self, scene, titulo = "Nodo Morion"):
        self.scene = scene
        self.titulo = titulo

        self.content = QDMNodeContentWidget()
        self.gNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.gNode)

        self.inputs = []
        self.outputs = []



