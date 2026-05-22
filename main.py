import sys
from PySide6.QtWidgets import QApplication

from src.controllers.MainController import MainController
from src.models.MainModel import MainModel
from src.views.MainWindow import MainWindow


def main(*args, **kwargs):
    app = QApplication(sys.argv)
    view = MainWindow()
    model = MainModel()
    controller = MainController(view, model)
    view.show()

    sys.exit(app.exec())
    pass

if __name__ == '__main__':
    main()
