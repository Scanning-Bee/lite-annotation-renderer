import os
import datetime

from image_annotator.image_annotator import Annotator
from PIL import Image, ImageDraw

OUTPUT_IMAGES_DIR = "generated_images"


def get_annotation(image_file_name: str):
    image_directory = os.path.dirname(image_file_name)
    image_base_name = os.path.basename(image_file_name)

    annotator = Annotator(
        image_directory,
        'metadata.yaml'
    )

    annotator.render_image_annotations(image_base_name)
