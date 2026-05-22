import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel,
    QLineEdit, QProgressBar, QScrollArea, QFrame, QVBoxLayout, QTableWidget,
    QSizePolicy, QTableWidgetItem, QFileDialog
)
from PySide6.QtCore import Qt, Signal

class ErrorWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error")
        self.setMinimumSize(300, 200)

        layout = QVBoxLayout()
        self.error_label = QLabel("Error")
        layout.addWidget(self.error_label)

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self._click_ok)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def _click_ok(self):
        self.close()

    def set_error_msg(self, error_msg):
        self.error_label.setText(error_msg)
