# from cube_model.naive_model import *
from naive_model import *
from copy import deepcopy
import numpy as np
from itertools import permutations, chain
import math
from tqdm import tqdm
from pprint import pprint


def shift(i, rot):
    return rot[i:] + rot[:i]

def swap(i, rot):
    axis_idx = list(range(3))
    axis_idx.pop(i)
    rot = deepcopy(rot)
    x = rot[axis_idx[0]]
    rot[axis_idx[0]] = rot[axis_idx[1]]
    rot[axis_idx[1]] = x
    return rot

def generate_swap_rotation_grps():
    generated_rots = []
    for i in range(3):
        rot = [0, 1, 2]
        generated_rots1 = []
        for j in range(3):
            rot = swap(i, rot)
            generated_rots1.append("".join(map(str, rot)))
        print(Counter(generated_rots1), generated_rots1)
        generated_rots.extend(generated_rots1)


def test_cube_sane(cubestate: CubeState):
    faces = render_cube(cubestate)
    cntr = Counter()
    cntr_ids = Counter()
    for i, (cols, ids) in enumerate(faces.values()):
        cntr = cntr + Counter(cols.flatten())
        cntr_ids = cntr_ids + Counter(ids.flatten())
    col_cnts = set(cntr.values())
    id_cnts = set(cntr_ids.values())
    assert len(col_cnts) == 1 and len(cntr) == 6 and col_cnts == {4}, cntr
    assert len(id_cnts) == 1 and len(cntr_ids) == 8 and id_cnts == {3}, cntr


def test_if_randoms_are_valid():
    for seed in range(100):
        cube = random_cube_state(seed)  
        test_cube_sane(cube)
        for _ in range(20):
            twist = TwistAction(np.random.randint(3), np.random.choice([-1, 0, 1]))
            cube = apply_twist_action(cube, twist)
            test_cube_sane(cube)

test_if_randoms_are_valid()
print("tests are ok")
