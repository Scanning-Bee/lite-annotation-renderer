from defs import Annotation, CellType


def to_annotation_dictionary(annotations: list) -> dict[str, list[Annotation]]:
    annot_dict: dict[str, list[Annotation]] = dict(list)

    for annotation_data in annotations:
        img_name = annotation_data["orig_image"]
        annot_dict[img_name].append(Annotation(
            cell_type=CellType.__members__[annotation_data["annotation"]],
            radius=annotation_data["radius"],
            center=[annotation_data["center_x"], annotation_data["center_y"]],
            source_name=annotation_data["source_name"],
            poses=[annotation_data["x_pos"], annotation_data["y_pos"]],
            timestamp=annotation_data["sec"],
        ))

    return annot_dict