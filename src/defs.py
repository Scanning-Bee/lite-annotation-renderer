
from enum import Enum


class CellType(Enum):
    EMPTY = 1
    NECTAR = 2
    LARVAE = 3
    PUPPA = 4
    HONEY_CLOSED = 5
    BEE_OCCLUDED = 6
    EGG = 7
    POLLEN = 8
    NOT_CLASSIFIED = 9


class Annotation:
    radius: int = 0
    center: list[int] = [-1, -1]
    cell_type: CellType
    source_name: str
    active: bool = True
    timestamp = None
    poses: list[float] = []

    def __init__(
        self,
        cell_type: CellType,
        radius: int,
        center: list[int],
        source_name: str,
        poses: list[float],
        timestamp,
    ) -> None:
        self.cell_type = cell_type
        self.radius = radius
        self.center = center
        self.source_name = source_name
        self.timestamp = timestamp
        self.poses = poses
