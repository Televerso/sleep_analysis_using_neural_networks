from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)

from src.utils.trenslation_manager.translation_manager import _

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Scores label
        self.scores_label = QLabel(_("No results yet"))
        self.scores_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scores_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.scores_label)

        # Parameters table
        self.params_table = QTableWidget()
        self.params_table.setRowCount(2)
        self.params_table.setVerticalHeaderLabels([_("Parameter"), _("Value")])
        self.params_table.horizontalHeader().setVisible(False)
        layout.addWidget(self.params_table)

    def set_scores(self, scores: dict):
        text = ''
        for key, val in scores.items():
            text += key + ": " + f"{val:.3f}" + ";  "

        self.scores_label.setText(text)

    def set_parameters(self, parameters: dict):
        self.params_table.setColumnCount(len(parameters))
        for col, (key, value) in enumerate(parameters.items()):
            name_item = QTableWidgetItem(str(key))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item = QTableWidgetItem(f"{value:.2f}")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.params_table.setItem(0, col, name_item)
            self.params_table.setItem(1, col, value_item)

        # Resize columns to fit contents
        self.params_table.resizeColumnsToContents()