# from cube_model.naive_model import *
from naive_model import *
from copy import deepcopy
import numpy as np
from itertools import permutations, chain
from sympy.utilities.iterables import multiset_permutations
from tqdm import tqdm

def is_same_vals(arr):
    return np.unique(arr).shape[0] == 1

def test_simple_rotations(rot):
    s1 = apply_twist_action(CubeState(), TwistAction(rot))
    s1_faces = render_cube(s1)

    lines_of_interest = [
        s1_faces["up"][1,:],
        s1_faces["left"][:,1],
        s1_faces["right"][:,1],
        s1_faces["down"][1,:],
        
        s1_faces["up"][0,:],
        s1_faces["left"][:,0],
        s1_faces["right"][:,0],
        s1_faces["down"][0,:],
    ]
    lines_not_broken = all(is_same_vals(line) for line in lines_of_interest)
    arrs = list(s1_faces.values())
    cntr = Counter(np.concatenate(arrs).flatten())
    equal_numbers = len(cntr) == 6 and cntr.most_common()[0][1] == 4
    # print(pretty_render(s1))
    return lines_not_broken and equal_numbers

def test_simple_multiple_rotations():
    return test_simple_rotations((1, 0, 0)) and test_simple_rotations((-1, 0, 0))

# test_simple_rotations()

original_piece_colors = deepcopy(piece_colors)
original_face_coordinate = deepcopy(face_coordinate)


keys = ["front", "back", "up", "down", "right", "left"]
def permutation_traverse():    
    base_ints = [0]*8 + [1]*8 + [2]*8 

    # Iterates all ~9.46 billion combinations without nuking your machine
    for p in tqdm(multiset_permutations(base_ints), total=9_465_511_770):
        face_coordinate1 = {k: tuple(p[i*4 : i*4+4]) for i, k in enumerate(keys)}
        for k in face_coordinate:
            face_coordinate[k] = face_coordinate1[k]
        if test_simple_multiple_rotations():
            print()
            print(face_coordinate)
            # print(pretty_render(apply_twist_action(CubeState(), TwistAction((1, 0, 0)))))
            print("success")
            break




def recursive_traverse():
    
    def rec(perm, cnt0, cnt1, cnt2):
        if len(perm) == 24:
            face_coordinate = {k: tuple(perm[i*4 : i*4+4]) for i, k in enumerate(keys)}
            
            if test_simple_multiple_rotations():
                print()
                print(face_coordinate)
                # print(pretty_render(apply_twist_action(CubeState(), TwistAction((1, 0, 0)))))
                print("success")
                return True
        else:
            if cnt0 < 8:
                perm1 = (*perm, 0)
                if rec(perm1, cnt0 + 1, cnt1, cnt2):
                    return True
            if cnt1 < 8:
                perm1 = (*perm, 1)
                if rec(perm1, cnt0, cnt1+1, cnt2):
                    return True
            if cnt2 < 8:
                perm1 = (*perm, 2)
                if rec(perm1, cnt0, cnt1, cnt2+1):
                    return True

    rec((), 0, 0, 0)

if __name__ == "__main__":
    # permutation_traverse()
    recursive_traverse()