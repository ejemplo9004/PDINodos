from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_edge import Edge
from node_graphics_cutline import QDMCutLine

DEBUG = True
MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_TRESHOLD = 10


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.last_bim_click_scene_pos = None
        self.dragEdge = None
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.editingFlag = False

        self.zoomInFactor = 1.25
        self.zoom = 7
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # Linea de corte de Edges
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)

    def initUI(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def distanceBetweenClickAndReleaseIsOf(self, event):
        # Verifica la distancia entre donde se presiono y solto el click
        new_bim_release_scene_pos = self.mapToScene(event.pos())
        dist_scene_pos = new_bim_release_scene_pos - self.last_bim_click_scene_pos;
        dist_scn = (dist_scene_pos.x() * dist_scene_pos.x() + dist_scene_pos.y() * dist_scene_pos.y())
        if dist_scn > EDGE_DRAG_START_TRESHOLD * EDGE_DRAG_START_TRESHOLD:
            return True
        return False

    def edgeDragStart(self, item):
        if DEBUG: print("Inicia el drag de un socket")
        if DEBUG: print(" Asigna socket inicial a: ", item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None)
        if DEBUG: print("Creando nuevo Edge")

    def edgeDragEnd(self, item):
        # Identidica que si se suelta el mouse y estaba arrastrando, finaliza con o sin socket
        if DEBUG: print("Finaliza el drag")
        self.mode = MODE_NOOP
        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                if DEBUG: print("  Asignar el socket final")

                if item.socket.hasEdge():
                    item.socket.edge.remove()

                if self.previousEdge is not None:
                    self.previousEdge.remove()
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)

                self.dragEdge.updatePositions()
                return True

        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket_edge = self.previousEdge

        return False

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.presionaBotonDerecho(event)
        elif event.button() == Qt.LeftButton:
            self.presionaBotonIzquierdo(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.sueltaBotonDerecho(event)
        elif event.button() == Qt.LeftButton:
            self.sueltaBotonIzquierdo(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def presionaBotonDerecho(self, event):
        super().mousePressEvent(event)

        item = self.itemEnClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): print("RMB Debug:", item.edge, "conecta sockets:",
                                                        item.edge.start_socket, "<-->", item.edge.end_socket)
            if type(item) is QDMGraphicsSocket: print("RMB Debug:", item.socket, "has edge:", item.socket.edge)

            if item == None:
                print("ESCENA:")
                print("  Nodos:")
                for node in self.grScene.scene.nodes: print("   -", node)
                print("  Edges:")
                for edges in self.grScene.scene.edges: print("   -", edges)

    def sueltaBotonDerecho(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super(QDMGraphicsView, self).keyPressEvent(event)
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.saveToFile("grafo.json.txt")
        elif event.key() == Qt.Key_O and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.loadFromFile("grafo.json.txt")
        else:
            super().keyPressEvent(event)
    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix+1]
            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.ShiftModifier: out += "Shift "
        if event.modifiers() & Qt.AltModifier: out += "Alt "
        if event.modifiers() & Qt.ControlModifier: out += "Ctrl "
        return out

    def presionaBotonIzquierdo(self, event):

        item = self.itemEnClick(event)

        self.last_bim_click_scene_pos = self.mapToScene(event.pos())

        # logica principal
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(),
                                        event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)

    def itemEnClick(self, event):
        return self.itemAt(event.pos())

    def sueltaBotonIzquierdo(self, event):
        item = self.itemEnClick(event)

        # Logica principal
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOf(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoomOutFactor = 1 / self.zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        if not clamped:
            self.scale(zoomFactor, zoomFactor)
