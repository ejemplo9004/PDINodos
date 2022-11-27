from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGT_TOP, RIGTH_BOTTOM


class Node():
    def __init__(self, scene, titulo="Nodo Morion", inputs=[], outputs=[]):
        self.scene = scene
        self.titulo = titulo
        self.socket_spacing = 21

        self.content = QDMNodeContentWidget()
        self.gNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.gNode)
        # self.initInputOutputs(inputs, outputs)

        # Crear sockets de entradas y salidas
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGTH_BOTTOM, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.gNode.pos() # viene de Qt

    def setPos(self, x, y):
        self.gNode.setPos(x, y)
    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.gNode.width

        if position in (LEFT_TOP, RIGT_TOP):
            y = self.gNode.title_heigth + self.gNode.edge_size + self.gNode._padding + index * self.socket_spacing
        else:
            y = self.gNode.height - self.gNode.edge_size - self.gNode._padding - index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for soket in self.inputs + self.outputs:
            if soket.hasEdge():
                soket.edge.updatePositions()