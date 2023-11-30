from typing import List
import yaml

import os
import cv2

import numpy as np

from image_annotator.image_annotator.annotation_types import Annotation, CellType
from image_annotator.image_annotator.utils import to_annotation_dictionary, print_annotation_dictionary


class AnnotationHandler:
    _annotations_path: str = None

    _annotations_dict: dict = None

    def __init__(self, parent_directory: str):
        supposed_annotations_path = os.path.join(parent_directory, 'annotations', 'annotations.yaml')
        
        if os.path.exists(supposed_annotations_path):
            self._annotations_path = supposed_annotations_path

        else:
            raise FileNotFoundError(f'No annotations.yaml file found in {parent_directory}')

    def parse_metadata(self):
        with open(self._annotations_path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                
                raw_annotations = data['annotation_data']['annotations']

                self._annotations_dict = to_annotation_dictionary(raw_annotations)

            except Exception as exc:
                raise Exception(f'Error while parsing annotations.yaml: {exc}')
    
    def draw_on_image(self, img: np.ndarray, annotations_to_draw: List[Annotation] = None):
        for annotation in annotations_to_draw:
            img = annotation.draw(img)
            
        return img
    
    def draw_on_all_images(self, parent_directory: str):
        try:
            output_paths = []

            for img_name in self._annotations_dict.keys():
                img = cv2.imread(os.path.join(parent_directory, img_name))
                
                img = self.draw_on_image(img, self._annotations_dict[img_name])

                parent_directory_basename = os.path.basename(parent_directory)

                output_path = os.path.join(parent_directory, '..', f'rendered_images_for_{parent_directory_basename}', img_name)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                cv2.imwrite(output_path, img)

                output_paths.append(output_path)

            return output_paths

        except Exception as exc:
            raise Exception(f'Error while drawing on images: {exc}')
    
    def get_all_annotations(self):
        return self._annotations_dict

    
if (__name__ == '__main__'):
    ah = AnnotationHandler('../sample_annotations.yaml')
    
    ah.parse_metadata()

    print(ah.get_all_annotations())

    print(ah.get_annotations_by_filename('image_42.jpg'))
