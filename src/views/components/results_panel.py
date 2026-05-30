from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QSizePolicy, QHBoxLayout, QHeaderView
)
from matplotlib.pyplot import table

from src.utils.trenslation_manager.translation_manager import _
from src.views.components.hypnogram_widget import HypnogramWidget
from src.views.utils.is_system_dark_mode import is_system_dark_mode


class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # hypnogram
        self.hypnogram = HypnogramWidget(is_system_dark_mode())
        layout.addWidget(self.hypnogram)

        # Parameters table
        self.params_table = QTableWidget()
        self.params_table.setRowCount(2)
        self.params_table.setVerticalHeaderLabels([_("Parameter"), _("Value")])
        self.params_table.horizontalHeader().setVisible(False)
        self.params_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.params_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.params_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.params_table.wheelEvent = lambda event: event.ignore()
        layout.addWidget(self.params_table)

        # Scores label
        self.scores_label = QLabel(_("No results yet"))
        self.scores_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scores_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.scores_label)


        # Data tables
        table_space_widget = QWidget()
        table_space_layout = QHBoxLayout()

        # Pose table
        self.pose_table = QTableWidget()
        self.pose_table.setColumnCount(2)
        self.pose_table.setRowCount(10)
        self.pose_table.setHorizontalHeaderLabels([_("Time"), _("Pose")])
        self.pose_table.verticalHeader().setVisible(False)
        self.pose_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pose_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pose_table.wheelEvent = lambda event: event.ignore()
        table_space_layout.addWidget(self.pose_table)

        # Stage table
        self.stage_table = QTableWidget()
        self.stage_table.setColumnCount(2)
        self.stage_table.setRowCount(10)
        self.stage_table.setHorizontalHeaderLabels([_("Time"), _("Stage")])
        self.stage_table.verticalHeader().setVisible(False)
        self.stage_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.stage_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.stage_table.wheelEvent = lambda event: event.ignore()
        table_space_layout.addWidget(self.stage_table)

        table_space_widget.setLayout(table_space_layout)
        layout.addWidget(table_space_widget)

        self.setMinimumHeight(800)
        layout.addStretch()

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
            self.params_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        # Resize table height
        header_height = self.params_table.horizontalHeader().height()
        row_count = self.params_table.rowCount()
        row_height = self.params_table.rowHeight(0) if row_count > 0 else 30
        total_height = header_height + (row_count * row_height) + 4

        self.params_table.setMinimumHeight(total_height)
        self.params_table.setMaximumHeight(total_height)


    def set_stages(self, stages: dict):
        self.stage_table.setRowCount(len(stages))
        stage_map = {'WAKE': _("awake"), 'REM': _("REM stage"), 'NREM': _("NREM stages"), 'START': _('start'), 'END': _('end')}

        for row, (key, value) in enumerate(stages.items()):
            name_item = QTableWidgetItem(str(key))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item = QTableWidgetItem(stage_map[value])
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.stage_table.setItem(row, 0, name_item)
            self.stage_table.setItem(row, 1, value_item)

        ResultsPanel._resize_table_to_content(self.stage_table)

    def set_poses(self, poses: dict):
        self.pose_table.setRowCount(len(poses))
        pose_map = {'0' : _("left log"), '1': _("right log"), '2': _("supine"), 'START': _('start'), 'END': _('end')}

        for row, (key, value) in enumerate(poses.items()):
            name_item = QTableWidgetItem(str(key))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item = QTableWidgetItem(pose_map[str(value)])
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.pose_table.setItem(row, 0, name_item)
            self.pose_table.setItem(row, 1, value_item)

        ResultsPanel._resize_table_to_content(self.pose_table)

    def update_panel(self, results: dict):
        self.hypnogram.plot(results["stages"])
        self.set_scores(results["scores"])
        self.set_parameters(results["parameters"])
        self.set_stages(results["stages"])
        self.set_poses(results["poses"])


    @staticmethod
    def _resize_table_to_content(table: QTableWidget):
        # Calculate total width from all columns
        total_width = table.verticalHeader().width() + 4  # Row numbers + padding
        for col in range(table.columnCount()):
            total_width += table.columnWidth(col)

        if total_width >= table.viewport().width():
            total_width = table.viewport().width()

        # Calculate total height from all rows
        header_height = table.horizontalHeader().height()
        row_count = table.rowCount()
        row_height = table.rowHeight(0) if row_count > 0 else 30
        total_height = header_height + (row_count * row_height) + 4

        # Apply sizes
        table.setMinimumSize(total_width, total_height)
        table.setMaximumSize(total_width, total_height)

        # Let it expand if more space is available
        table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
