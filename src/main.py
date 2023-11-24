import sys
import datetime
from tools import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class Window(QtWidgets.QMainWindow):
    activeImageFileName: str = None

    pixmap: QPixmap = None

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 150, 900, 600)
        self.render_ui()

    def render_ui(self):
        self.setWindowTitle("Annotated Circle Renderer")

        file_dialog_button = QtWidgets.QPushButton("Choose an image")
        render_image_button = QtWidgets.QPushButton("Render the annotated image")
        remove_file_button = QtWidgets.QPushButton("Remove the image")

        file_dialog_button.clicked.connect(self.open_file_dialog)
        render_image_button.clicked.connect(self.render_image)
        remove_file_button.clicked.connect(self.remove_file)

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addStretch()

        if self.pixmap is not None:
            label = QtWidgets.QLabel(self)
            label.setPixmap(self.pixmap)
            panel_layout.addWidget(label)

            panel_layout.addWidget(render_image_button)
            panel_layout.addWidget(remove_file_button)
            panel_layout.addStretch()
        else:
            panel_layout.addWidget(file_dialog_button)
            panel_layout.addStretch()

        final_layout = QtWidgets.QHBoxLayout()
        final_layout.addStretch()
        final_layout.addLayout(panel_layout)
        final_layout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(final_layout)

        self.show()

    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()

        # allow only image files, particularly jpg
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPG Files (*.jpg)", options=options)

        if fileName:
            print(f'selected file: {fileName}')

            self.activeImageFileName = fileName

            self.pixmap = QPixmap(fileName)

            # set image dimensions
            self.pixmap = self.pixmap.scaled(500, 500, Qt.KeepAspectRatio)

            self.render_ui()

    def remove_file(self):
        self.activeImageFileName = None
        self.pixmap = None

        self.render_ui()

    def render_image(self):
        if self.activeImageFileName is None:
            return

        get_annotation(self.activeImageFileName)

        self.render_ui()


class ScrollLabel(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QtWidgets.QWidget(self)
        self.setWidget(content)
        layout = QtWidgets.QVBoxLayout(content)
        self.label = QtWidgets.QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        self.back_button = QtWidgets.QPushButton("Back")
        layout.addWidget(self.label)

        self.show()


app = QtWidgets.QApplication(sys.argv)

window = Window()

sys.exit(app.exec())
