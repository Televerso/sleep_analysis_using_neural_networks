from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QSizePolicy


class ScrollAreaForResults(QScrollArea):
    def __init__(self, parent=None):
        super(ScrollAreaForResults, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        if self.widget():
            self.widget().setMaximumWidth(self.viewport().width())

    def setWidget(self, widget):
        super().setWidget(widget)

        widget.setMaximumWidth(self.viewport().width())

