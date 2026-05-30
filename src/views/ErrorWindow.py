import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QPushButton, QLabel,
    QVBoxLayout, QDialog
)

from src.utils.file_functions.get_root_path import get_root_path
from src.utils.trenslation_manager.translation_manager import _

class ErrorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(_("Error"))
        icon_path = os.path.join(get_root_path(), "resources", "icons", "error.ico")
        self.setWindowIcon(QIcon(icon_path))
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
