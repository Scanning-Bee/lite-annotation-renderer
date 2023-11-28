import os

from image_annotator.image_annotator import Annotator


class AnnotatorInterface:
    _annotator: Annotator = None

    _annotated_image = None

    def __init__(
        self,
    ):
        return

    def initialise_annotator(self, metadata_path: str):
        metadata_directory = os.path.dirname(metadata_path)
        metadata_base_name = os.path.basename(metadata_path)

        self._annotator = Annotator(
            metadata_directory,
            metadata_base_name,
        )

    def annotate_image_from_metadata(self, image_path: str):
        self._annotated_image = self._annotator.render_image_annotations(image_path)

    def get_annotated_image_path(self):
        return self._annotated_image
