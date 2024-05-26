# This file contains the source code for the class that handles the click events on the QPixmaps (annotated imgs) in
# the RendererWindow.

from PyQt5.QtGui import QMouseEvent

from defs import Annotation, CellType

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080


class ClickHandler:
    def __init__(self):
        return

    @staticmethod
    def get_clicked_annotation(click_event: QMouseEvent, annotations: list[Annotation], img_width: int, img_height: int) -> Annotation:
        """
        Gets the annotation that was clicked on in the RendererWindow.
        :param click_event: The QMouseEvent that was triggered.
        :param annotations: The list of annotations to check. This is the list of annotations for the selected image.
        :param img_width: The width of the image.
        :param img_height: The height of the image.
        :return: The annotation that was clicked on, or a new annotation if none was clicked on.
        """

        clicked_x = click_event.x()
        clicked_y = click_event.y()

        real_clicked_x = (DEFAULT_WIDTH * clicked_x) / img_width
        real_clicked_y = (DEFAULT_HEIGHT * clicked_y) / img_height

        for annotation in annotations:
            center_x = annotation.center[0]
            center_y = annotation.center[1]

            if abs(center_x - real_clicked_x) < annotation.radius and abs(center_y - real_clicked_y) < annotation.radius:
                return annotation

        new_annotation = Annotation(
            CellType.NOT_CLASSIFIED,
            annotations[0].radius,
            [int(real_clicked_x), int(real_clicked_y)],
            annotations[0].source_name,
            [],
            None
        )

        return new_annotation
