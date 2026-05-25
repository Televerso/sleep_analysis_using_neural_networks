from PySide6.QtWidgets import (
    QPushButton, QLabel,
    QVBoxLayout, QDialog
)
from src.utils.trenslation_manager.translation_manager import _

class ErrorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(_("Error"))
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
