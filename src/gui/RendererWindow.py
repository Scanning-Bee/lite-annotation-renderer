import sys
import datetime

from annotator_ifc import AnnotatorInterface
import tools
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


SCALE = 300


def create_scaled_pixmap(pixmap: QPixmap) -> QPixmap:
    scaled_pixmap = pixmap.scaled(SCALE, SCALE, Qt.KeepAspectRatio, Qt.FastTransformation)

    return scaled_pixmap


class RendererWindow(QtWidgets.QMainWindow):
    active_image_path: str = None

    active_metadata_path: str = None

    annotated_image_path: str = None

    chosen_image_pixmap: QPixmap = None

    annotated_image_pixmap: QPixmap = None

    annotator_ifc: AnnotatorInterface = None

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 150, 900, 600)
        self.render_ui()
        self.annotator_ifc = AnnotatorInterface()

    def render_ui(self):
        self.setWindowTitle("Annotated Circle Renderer")

        choose_image_button = QtWidgets.QPushButton("Choose an image")
        choose_metadata_button = QtWidgets.QPushButton("Choose a metadata file")

        render_image_button = QtWidgets.QPushButton("Render the annotated image")
        reset_files_button = QtWidgets.QPushButton("Reset the files")

        choose_image_button.clicked.connect(self.open_image_dialog)
        choose_metadata_button.clicked.connect(self.open_metadata_dialog)
        render_image_button.clicked.connect(self.get_annotation)
        reset_files_button.clicked.connect(self.reset_files)

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addStretch()

        if self.chosen_image_pixmap is not None:
            label = QtWidgets.QLabel(self)

            scaled_pixmap = create_scaled_pixmap(self.chosen_image_pixmap)
            label.setPixmap(scaled_pixmap)

            panel_layout.addWidget(label)

            panel_layout.addStretch()

        if self.annotated_image_pixmap is None:
            if self.active_image_path is None:
                panel_layout.addWidget(choose_image_button)
            else:
                image_path_text = QtWidgets.QLabel(self)
                image_path_text.setText(f"Chosen Image Path: {self.active_image_path}")
                panel_layout.addWidget(image_path_text)

            if self.active_metadata_path is None:
                panel_layout.addWidget(choose_metadata_button)
            else:
                metadata_path_text = QtWidgets.QLabel(self)
                metadata_path_text.setText(f"Chosen Metadata Path: {self.active_metadata_path}")
                panel_layout.addWidget(metadata_path_text)

        else:
            label = QtWidgets.QLabel(self)

            scaled_pixmap = create_scaled_pixmap(self.annotated_image_pixmap)

            label.setPixmap(scaled_pixmap)

            annotated_image_path_text = QtWidgets.QLabel(self)
            annotated_image_path_text.setText(f"Annotated Image Path: {self.annotated_image_path}")

            panel_layout.addWidget(label)
            panel_layout.addWidget(annotated_image_path_text)

        if self.active_image_path is not None and self.active_metadata_path is not None:
            if self.annotated_image_path is None:
                panel_layout.addWidget(render_image_button)

            panel_layout.addWidget(reset_files_button)

        panel_layout.addStretch()

        final_layout = QtWidgets.QHBoxLayout()
        final_layout.addStretch()
        final_layout.addLayout(panel_layout)
        final_layout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(final_layout)

        self.show()

    def open_image_dialog(self):
        options = QtWidgets.QFileDialog.Options()

        # allow only image files, particularly jpg
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "JPG Files (*.jpg)", options=options)

        if fileName:
            print(f'selected file: {fileName}')

            self.active_image_path = fileName

            self.chosen_image_pixmap = QPixmap(fileName)

            # set image dimensions
            self.chosen_image_pixmap = self.chosen_image_pixmap.scaled(500, 500, Qt.KeepAspectRatio)

            self.render_ui()

    def open_metadata_dialog(self):
        options = QtWidgets.QFileDialog.Options()

        # allow only image files, particularly jpg
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "YAML Files (*.yaml)", options=options)

        if fileName:
            print(f'selected file: {fileName}')

            self.active_metadata_path = fileName

            self.render_ui()

    def reset_files(self):
        self.active_image_path = None
        self.active_metadata_path = None
        self.annotated_image_path = None

        self.chosen_image_pixmap = None
        self.annotated_image_pixmap = None

        self.render_ui()

    def render_image(self):
        # TODO:
        return

    def get_annotation(self):
        if self.active_metadata_path is None or self.active_image_path is None:
            return

        self.annotator_ifc.initialise_annotator(self.active_metadata_path)

        self.annotator_ifc.annotate_image_from_metadata(self.active_image_path)

        self.annotated_image_path = self.annotator_ifc.get_annotated_image_path()

        self.annotated_image_pixmap = QPixmap(self.annotated_image_path)

        self.render_ui()
