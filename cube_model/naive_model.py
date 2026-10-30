from dataclasses import dataclass


@dataclass
class TwistAction:
    twists: tuple[int] # 3 rotations of the free 4-piece planes


@dataclass
class CubeState:
    loc: tuple[int] # perimutation of free piece locations
    rots: tuple[int] # a list corresponding to orientation of each piece (3 orientations per pieace, 0-2 ints)



