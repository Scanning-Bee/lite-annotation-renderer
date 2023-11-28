import sys
from PyQt5 import QtWidgets

from gui.RendererWindow import RendererWindow

app = QtWidgets.QApplication(sys.argv)

window = RendererWindow()

sys.exit(app.exec())
