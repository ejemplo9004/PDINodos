from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.zoomInFactor = 1.25
        self.zoom = 7
        self.zoomStep = 1
        self.zoomRange = [0, 10]

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
        return super().mousePressEvent(event)

    def sueltaBotonDerecho(self, event):
        return super().mouseReleaseEvent(event)

    def presionaBotonIzquierdo(self, event):
        return super().mousePressEvent(event)

    def sueltaBotonIzquierdo(self, event):
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoomOutFactor = 1/self.zoomInFactor


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


