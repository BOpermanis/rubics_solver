# from cube_model.naive_model import *
from naive_model import *
from copy import deepcopy
import numpy as np
from itertools import permutations

def is_same_vals(arr):
    return np.unique(arr).shape[0] == 1

def test_simple_rotations():
    s1 = apply_twist_action(CubeState(), TwistAction((1, 0, 0)))
    s1_faces = render_cube(s1)

    lines_of_interest = [
        s1_faces["up"][1,:],
        s1_faces["left"][:,1],
        s1_faces["right"][:,1],
        s1_faces["down"][1,:],
    ]

    return all(is_same_vals(line) for line in lines_of_interest)

    line = s1_faces["right"][:,0]
    print(is_same_vals(line), line)
    # exit()
    print(pretty_render(s1))

# test_simple_rotations()

original_piece_colors = deepcopy(piece_colors)
original_face_coordinate = deepcopy(face_coordinate)


vs = [0]*8 + [1]*8 + [2]*8
for vs1 in permutations()