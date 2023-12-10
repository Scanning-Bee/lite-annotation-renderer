import os

from gui.AnnotationEditor import AnnotationEditor
from gui.constants import SCALE, PROPORTION
from gui.utils import create_scaled_pixmap
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

from handlers.annotation_handler import AnnotationHandler
from handlers.click_handler import ClickHandler
from image_annotator.image_annotator.annotation_types import Annotation


class RendererWindow(QtWidgets.QMainWindow):
    _chosen_folder_path: str = None

    _annotated_image_paths: list[str] = []

    _shown_image_index: int = -1

    _chosen_annotation_index: int = -1

    _annotation_handler: AnnotationHandler = None

    _rendering_in_progress: bool = False

    _error_text: str = None

    _click_handler: ClickHandler = ClickHandler()

    _annotation_editor: AnnotationEditor = None

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 150, 1260, 600)
        self.render_ui()

    def navigate_images(self, direction: int):
        if self._shown_image_index + direction < 0 or self._shown_image_index + direction >= len(self._annotated_image_paths):
            return

        self._shown_image_index += direction

        self._chosen_annotation_index = -1

        self.render_ui()

    def render_ui(self):
        self.setWindowTitle("Annotation Renderer")

        choose_folder_button = QtWidgets.QPushButton("Choose a folder")
        choose_folder_button.clicked.connect(self.folder_dialog)

        choose_another_folder_button = QtWidgets.QPushButton("Choose another folder")
        choose_another_folder_button.clicked.connect(self.folder_dialog)

        panel_layout = QtWidgets.QVBoxLayout()

        panel_layout.addStretch()

        if self._chosen_folder_path is None:
            panel_layout.addWidget(choose_folder_button)

            if self._error_text is not None:
                error_text = QtWidgets.QLabel(self)
                error_text.setText(self._error_text)
                error_text.setStyleSheet("color: darkred;")

                panel_layout.addWidget(error_text)

        else:
            if self._error_text is not None:
                error_text = QtWidgets.QLabel(self)
                error_text.setText(self._error_text)
                error_text.setStyleSheet("color: darkred;")

                panel_layout.addWidget(error_text)
            elif self._rendering_in_progress:
                panel_layout.addWidget(QtWidgets.QLabel("Rendering in progress..."))
            else:
                if not self._annotated_image_paths:
                    panel_layout.addWidget(QtWidgets.QLabel("No images found in the chosen folder"))

                else:
                    if self._shown_image_index == -1:
                        panel_layout.addWidget(QtWidgets.QLabel("No images found in the chosen folder"))
                    else:
                        image = self._annotated_image_paths[self._shown_image_index]

                        unscaled_pixmap = QPixmap(image)

                        image_label = QtWidgets.QLabel(self)

                        image_label.setPixmap(create_scaled_pixmap(unscaled_pixmap))

                        image_label.mousePressEvent = self.infer_annotation_from_click

                        panel_layout.addWidget(image_label)
                        panel_layout.addWidget(QtWidgets.QLabel(f"Image {self._shown_image_index + 1} of {len(self._annotated_image_paths)}"))
                        panel_layout.addWidget(QtWidgets.QLabel(f"Image path: {image}"))

                        navigation_layout = QtWidgets.QHBoxLayout()

                        previous_image_button = QtWidgets.QPushButton("Previous image")
                        previous_image_button.clicked.connect(lambda: self.navigate_images(-1))
                        previous_image_button.setDisabled(self._shown_image_index == 0)

                        next_image_button = QtWidgets.QPushButton("Next image")
                        next_image_button.clicked.connect(lambda: self.navigate_images(1))
                        next_image_button.setDisabled(self._shown_image_index == len(self._annotated_image_paths) - 1)

                        navigation_layout.addWidget(previous_image_button)
                        navigation_layout.addWidget(next_image_button)

                        panel_layout.addLayout(navigation_layout)

                        def delete_annotation(annotation: Annotation):
                            self._annotation_handler.delete_annotation(annotation)
                            self._chosen_annotation_index = - 1

                        # if the editor is disabled, it is guaranteed that the chosen annotation index is -1
                        # and none of the methods passed to the editor will be called
                        self._annotation_editor = AnnotationEditor(
                            self._annotation_handler.modify_annotation,
                            delete_annotation,
                            self.render_ui,
                            self.get_chosen_annotation(),
                            disabled=self._chosen_annotation_index == -1
                        )

            chosen_folder_path_text = QtWidgets.QLabel(self)
            chosen_folder_path_text.setText(f"Chosen folder path: {self._chosen_folder_path}")

            panel_layout.addWidget(choose_another_folder_button)

        panel_layout.addStretch()

        final_layout = QtWidgets.QHBoxLayout()
        final_layout.addStretch()
        final_layout.addLayout(panel_layout)

        if self._annotation_editor is not None:
            editor_layout = QtWidgets.QVBoxLayout()
            editor_layout.addWidget(self._annotation_editor.get_annotation_editor())
            editor_layout.addStretch()

            final_layout.addLayout(editor_layout)

        final_layout.addStretch()

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        central.setLayout(final_layout)

        self.show()

    def folder_dialog(self):
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

        if dir_name:
            self._chosen_folder_path = dir_name

            self.render_annotations()

    def get_active_image_name(self):
        return os.path.basename(self._annotated_image_paths[self._shown_image_index])
    
    def get_annotations_of_active_image(self):
        return self._annotation_handler.get_annotations_by_filename(self.get_active_image_name())

    def get_chosen_annotation(self):
        if self._chosen_annotation_index == -1:
            return None

        return self.get_annotations_of_active_image()[self._chosen_annotation_index]

    def infer_annotation_from_click(self, click_event: QMouseEvent):
        active_image_annotations = self.get_annotations_of_active_image()
        
        inferred_annotation = self._click_handler.get_clicked_annotation(
            click_event,
            active_image_annotations,
            SCALE,
            SCALE / PROPORTION
        )

        # if the click was on a new annotation, add it to the list of annotations
        if inferred_annotation not in active_image_annotations:
            self._annotation_handler.save_new_annotation(inferred_annotation)

        self._chosen_annotation_index = active_image_annotations.index(inferred_annotation)

        self.render_ui()

    def render_annotations(self):
        self._rendering_in_progress = True
        self._error_text = None

        self.render_ui()

        try:
            self._annotation_handler = AnnotationHandler(self._chosen_folder_path)
        except FileNotFoundError as e:
            self._error_text = str(e)
            self.render_ui()
            return

        try:
            self._annotation_handler.parse_metadata()
            self._annotated_image_paths = self._annotation_handler.draw_on_all_images()

            self._error_text = None

            self._shown_image_index = 0

        except Exception as e:
            self._error_text = str(e)

        self._rendering_in_progress = False

        self.render_ui()

