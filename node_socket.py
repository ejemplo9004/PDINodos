from node_graphics_socket import QDMGraphicsSocket
LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGT_TOP = 3
RIGTH_BOTTOM = 4

class Socket():
    def __init__(self, node, index=0, position = LEFT_TOP):

        self.node = node
        self.index = index
        self.position = position

        self.grScoket = QDMGraphicsSocket(self.node.gNode)

        self.grScoket.setPos(*self.node.getSocketPosition(index, position))
