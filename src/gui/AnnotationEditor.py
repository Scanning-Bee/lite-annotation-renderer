from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from image_annotator.image_annotator.annotation_types import Annotation, CellType


# not a window, just a widget in the main window (RendererWindow)
class AnnotationEditor(QtWidgets.QWidget):
    _modify_function: callable = None

    _save_function: callable = None

    _delete_function: callable = None

    _render_parent: callable = None

    _annotation: Annotation = None

    _disabled: bool = False

    def __init__(self, modify_function, delete_function, render_parent, annotation, disabled):
        super().__init__()

        def modify_and_render_parent(*args):
            modify_function(*args)
            render_parent()

        def delete_and_render_parent(*args):
            delete_function(*args)
            render_parent()

        self._modify_function = modify_and_render_parent
        self._delete_function = delete_and_render_parent
        self._render_parent = render_parent
        self._annotation = annotation
        self._disabled = disabled

        self.render_ui()

    def render_ui(self):
        this_layout = QtWidgets.QVBoxLayout()

        # Gamepad Buttons
        up = QtWidgets.QPushButton('Up')
        down = QtWidgets.QPushButton('Down')
        left = QtWidgets.QPushButton('Left')
        right = QtWidgets.QPushButton('Right')

        up.clicked.connect(lambda: self._modify_function(self._annotation, {
            "center": [self._annotation.center[0], self._annotation.center[1] - 5]
        }))
        down.clicked.connect(lambda: self._modify_function(self._annotation, {
            "center": [self._annotation.center[0], self._annotation.center[1] + 5]
        }))
        left.clicked.connect(lambda: self._modify_function(self._annotation, {
            "center": [self._annotation.center[0] - 5, self._annotation.center[1]]
        }))
        right.clicked.connect(lambda: self._modify_function(self._annotation, {
            "center": [self._annotation.center[0] + 5, self._annotation.center[1]]
        }))

        if (self._disabled):
            up.setDisabled(True)
            down.setDisabled(True)
            left.setDisabled(True)
            right.setDisabled(True)

        buttons_layout = QtWidgets.QHBoxLayout()
        # Adding buttons to layout
        buttons_layout.addWidget(up)
        buttons_layout.addWidget(down)
        buttons_layout.addWidget(left)
        buttons_layout.addWidget(right)

        this_layout.addLayout(buttons_layout)

        # Dropdown Menu
        dropdown_layout = QtWidgets.QHBoxLayout()
        dropdown_menu = QtWidgets.QComboBox()
        dropdown_menu.addItems([cell_type.name for cell_type in CellType])

        confirm_type_button = QtWidgets.QPushButton('Change Type')

        confirm_type_button.clicked.connect(lambda: self._modify_function(self._annotation, {
            "cell_type": CellType[dropdown_menu.currentText()]
        }))

        if (self._disabled):
            dropdown_menu.setDisabled(True)
            confirm_type_button.setDisabled(True)
        else:
            dropdown_menu.setCurrentIndex(self._annotation.cell_type.value - 1)

        dropdown_layout.addWidget(dropdown_menu)
        dropdown_layout.addWidget(confirm_type_button)

        this_layout.addLayout(dropdown_layout)

        # Slider
        slider_layout = QtWidgets.QHBoxLayout()

        slider = QtWidgets.QSlider(Qt.Horizontal)

        slider.setRange(1, 160)

        confirm_radius_button = QtWidgets.QPushButton('Change Radius')
        confirm_radius_button.clicked.connect(lambda: self._modify_function(self._annotation, {
            "radius": int(slider.value())
        }))

        if (self._disabled):
            slider.setDisabled(True)
            confirm_radius_button.setDisabled(True)
        else:
            slider.setValue(self._annotation.radius)

        slider_layout.addWidget(slider)
        slider_layout.addWidget(confirm_radius_button)

        this_layout.addLayout(slider_layout)

        # Delete button
        delete_button = QtWidgets.QPushButton('Delete')

        delete_button.clicked.connect(lambda: self._delete_function(self._annotation))

        if (self._disabled):
            delete_button.setDisabled(True)

        this_layout.addWidget(delete_button)

        labels_layout = QtWidgets.QVBoxLayout()

        # TODO: Dummy labels for now. Should be replaced with actual labels
        labels_layout.addWidget(QtWidgets.QLabel('Label 1'))
        labels_layout.addWidget(QtWidgets.QLabel('Label 2'))
        labels_layout.addWidget(QtWidgets.QLabel('Label 3'))

        this_layout.addLayout(labels_layout)

        # Set the layout
        self.setLayout(this_layout)

    def set_annotation(self, annotation: Annotation):
        self._annotation = annotation

        self.render_ui()

    def set_modify_function(self, modify_function: callable):
        self._modify_function = modify_function

        self.render_ui()

    def set_delete_function(self, delete_function: callable):
        self._delete_function = delete_function

        self.render_ui()

    def get_annotation_editor(self) -> QtWidgets.QWidget:
        editor_widget = QtWidgets.QWidget()

        editor_widget.setLayout(self.layout())

        return editor_widget
