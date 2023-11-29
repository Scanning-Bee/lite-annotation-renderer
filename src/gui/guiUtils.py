from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.constants import SCALE


def create_scaled_pixmap(pixmap: QPixmap) -> QPixmap:
    scaled_pixmap = pixmap.scaled(SCALE, SCALE, Qt.KeepAspectRatio, Qt.FastTransformation)

    return scaled_pixmap
