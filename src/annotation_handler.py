from typing import List
import yaml

import numpy as np

from image_annotator.image_annotator.annotation_types import Annotation


class AnnotationHandler:
    _annotations: List[Annotation] = []
    
    _metadata_path: str = None

    def __init__(self, metadata_path: str):
        self._annotations = []
        
        self._metadata_path = metadata_path

    def parse_metadata(self):
        with open(self._metadata_path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                
                raw_annotations = data['annotation_data']['annotations']

                for raw_annotation in raw_annotations:
                    annotation = Annotation(
                        raw_annotation['annotation'], # the cell type
                        raw_annotation['radius'],
                        [raw_annotation['center_x'], raw_annotation['center_y']],
                        raw_annotation['orig_image'].replace('\\', '/'),
                        [],
                        raw_annotation['sec']
                    )
                    
                    self._annotations.append(annotation)

            except yaml.YAMLError as exc:
                print(exc)

    def get_all_annotations(self) -> List[Annotation]:
        return self._annotations
    
    def get_annotations_by_filename(self, chosen_file_path: str) -> List[Annotation]:
        def get_filename(path: str) -> str:
            return path.split('/')[-1]
        
        chosen_filename = get_filename(chosen_file_path)

        return [annotation for annotation in self._annotations if get_filename(annotation.source_name) == chosen_filename]
    
    def draw_on_image(self, img: np.ndarray):
        for annotation in self._annotations:
            annotation.draw(img)
            
        return img

    
if (__name__ == '__main__'):
    ah = AnnotationHandler('../sample_annotations.yaml')
    
    ah.parse_metadata()

    print(ah.get_all_annotations())

    print(ah.get_annotations_by_filename('image_42.jpg'))