from typing import List
import yaml

import os
import cv2

import numpy as np

from image_annotator.image_annotator.annotation_types import Annotation
from image_annotator.image_annotator.utils import to_annotation_dictionary


class AnnotationHandler:
    _annotations_dir_path: str = None

    _annotations_path: str = None

    _annotations_dict: dict = None

    def __init__(self, parent_directory: str):
        supposed_annotations_path = os.path.join(parent_directory, 'annotations', 'annotations.yaml')
        
        if os.path.exists(supposed_annotations_path):
            self._annotations_dir_path = os.path.join(parent_directory)
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
    
    def draw_on_all_images(self):
        output_dir = self.get_output_dir()

        try:
            # try: os.system(f'rm -rf {output_dir}')
            # except: print('me fail')

            os.makedirs(output_dir, exist_ok=True)

            output_paths = []

            for img_name in self._annotations_dict.keys():
                img = cv2.imread(os.path.join(self._annotations_dir_path, img_name))
                
                img = self.draw_on_image(img, self._annotations_dict[img_name])

                output_path = os.path.join(output_dir, img_name)

                cv2.imwrite(output_path, img)

                output_paths.append(output_path)

            return output_paths

        except Exception as exc:
            raise Exception(f'Error while drawing on images: {exc}')
    
    def get_all_annotations(self):
        return self._annotations_dict

    def get_annotations_by_filename(self, filename: str):
        return self._annotations_dict[filename]

    def save_new_annotation(self, annotation: Annotation):
        self._annotations_dict[annotation.source_name].append(annotation)

        new_img = self.draw_on_image(
            cv2.imread(os.path.join(self._annotations_dir_path, annotation.source_name)),
            self._annotations_dict[annotation.source_name]
        )

        output_path = os.path.join(self.get_output_dir(), annotation.source_name)

        # os.system(f'rm -f {output_path}')

        cv2.imwrite(output_path, new_img)

    def modify_annotation(self, annotation: Annotation, modifications: dict):
        annotation_index = self._annotations_dict[annotation.source_name].index(annotation)

        new_annotation = Annotation(
            source_name=annotation.source_name,
            center=annotation.center,
            radius=annotation.radius,
            cell_type=annotation.cell_type,
            timestamp=annotation.timestamp,
            poses=annotation.poses
        )

        for key in modifications.keys():
            setattr(new_annotation, key, modifications[key])

        self._annotations_dict[annotation.source_name][annotation_index] = new_annotation

        new_img = self.draw_on_image(
            cv2.imread(os.path.join(self._annotations_dir_path, annotation.source_name)),
            self._annotations_dict[annotation.source_name]
        )

        output_path = os.path.join(self.get_output_dir(), annotation.source_name)

        # os.system(f'rm -f {output_path}')

        cv2.imwrite(output_path, new_img)

    def delete_annotation(self, annotation: Annotation):
        self._annotations_dict[annotation.source_name].remove(annotation)

        new_img = self.draw_on_image(
            cv2.imread(os.path.join(self._annotations_dir_path, annotation.source_name)),
            self._annotations_dict[annotation.source_name]
        )

        output_path = os.path.join(self.get_output_dir(), annotation.source_name)

        # os.system(f'rm -f {output_path}')

        cv2.imwrite(output_path, new_img)

    def get_output_dir(self):
        return os.path.join(self._annotations_dir_path, '..', f'rendered_images_for_{os.path.basename(self._annotations_dir_path)}')


if (__name__ == '__main__'):
    ah = AnnotationHandler('../sample_annotations.yaml')
    
    ah.parse_metadata()

    print(ah.get_all_annotations())

    print(ah.get_annotations_by_filename('image_42.jpg'))
