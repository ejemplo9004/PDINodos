from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from collections import OrderedDict
from node_serializable import Serializable


class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Morion ensayo de etiqueta")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QDMTextEdit("Fooo"))

    def setEditingFlag(self, valor):
        self.node.scene.grScene.views()[0].editingFlag = valor

    def serialize(self):
        return OrderedDict([
            # ('id', self.id),
        ])

    def deserialize(self, data, hashmap={}):
        return False


class QDMTextEdit(QTextEdit):
    def focusInEvent(self, e: QFocusEvent):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(e)

    def focusOutEvent(self, e: QFocusEvent):
        self.parentWidget().setEditingFlag(False)
        super(QDMTextEdit, self).focusOutEvent(e)
