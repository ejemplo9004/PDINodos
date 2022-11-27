from node_graphics_socket import QDMGraphicsSocket
LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGT_TOP = 3
RIGTH_BOTTOM = 4

DEBUG = False
class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type = 0):

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.grScoket = QDMGraphicsSocket(self.node.gNode, self.socket_type)

        self.grScoket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    def getSocketPosition(self):
        if DEBUG: print("    GSP: ", self.index, self.position, "node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position)
        return res

    def setConnectedEdge(self, edge=None):
        self.edge = edge
    def hasEdge(self):
        return self.edge is not None