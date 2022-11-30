from node_graphics_scene import QDMGraphicsScene
from collections import OrderedDict
from node_serializable import Serializable
import json
class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width, self.scene_height = 64000, 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print("Guardando en ", filename)

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def serialize(self):
        nodes = []
        edges = []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges)
        ])

    def deserialize(self, data, hashmap={}):
        print("deserializando data", data)
        return False