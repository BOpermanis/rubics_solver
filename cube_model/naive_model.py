from dataclasses import dataclass, field
import numpy as np
from collections import Counter
from copy import deepcopy
from hashlib import md5
import json

@dataclass
class TwistAction:
    axis: int # 0, 1, 2 axis
    twist: int # rotation around the axis -1, 0, 1


default_color_state = np.array((
    ("r", "g", "o"), #0 # never touch this
    ("r", "g", "w"), #1
    ("r", "b", "o"), #2
    ("r", "b", "w"), #3
    ("y", "g", "o"), #4
    ("y", "g", "w"), #5
    ("y", "b", "o"), #6
    ("y", "b", "w")  #7
    ), str)


@dataclass
class CubeState:
    # Requires type hints for dataclass args, and default_factory for mutable arrays
    loc: np.ndarray = field(default_factory=lambda: np.reshape(np.arange(0, 8, dtype=int), (2, 2, 2)))
    cols: np.ndarray = field(default_factory=lambda: deepcopy(default_color_state))

    def hash(self):
        return str(self.loc) + "\n" + str(self.cols)

    def hash_md5(self):
        stable_bytes = self.hash().encode('utf-8')
        return md5(stable_bytes).hexdigest()

# print(CubeState().hash())
# print(CubeState().hash_md5())
# exit()

colors_full = ["red", "yellow", "green", "blue", "orange", "white"]
colors = ['r', 'y', 'g', 'b', 'o', 'w']
assert all((a==b for a, b in zip(colors, [_[0] for _ in colors_full]))) and len(set(colors)) == 6


# location -> rot offset
face_coordinate =  {
        "front": (0, 0, 0, 0), # r (default)
        "back": (0, 0, 0, 0), # y (default)
        "up": (1, 1, 1, 1), # g (default)
        "down": (1, 1, 1, 1), # b (default)
        "right": (2, 2, 2, 2), # o (default)
        "left": (2, 2, 2, 2), # w (default)
    }


cntr = Counter(CubeState().cols.flatten())
assert len(cntr) == 6 and cntr.most_common()[0][1] == 4, cntr


def render_face(loc, cols, fname):
    colors = cols[loc.flatten(),face_coordinate[fname]].reshape((2,2))
    return colors, loc


def twist_on_colors(new_cstate, ids, i1, i2, twist):
    match twist:
        case 1 :
            new_cstate.cols[ids[:,None],[i1, i2]] = new_cstate.cols[ids[:,None],[i2, i1]]
        case -1 :
            new_cstate.cols[ids[:,None],(i2, i1)] = new_cstate.cols[ids[:,None],(i1, i2)]
        case _:
            return


def apply_twist_action(cstate: CubeState, action: TwistAction, inplace=False) -> CubeState:
    new_cstate = cstate if inplace else deepcopy(cstate)
    
    axis = [slice(None)] * 3
    axis[action.axis] = 1 
    axis = tuple(axis)
    new_cstate.loc[axis] = np.rot90(cstate.loc[axis], action.twist, axes=(0, 1)) # apply rotation along shifting axes

    axis_idx = list(range(3))
    axis_idx.pop(action.axis)
    twist_on_colors(new_cstate, new_cstate.loc[axis].flatten(), *axis_idx, action.twist)

    if not inplace:
        return new_cstate


def render_cube(cstate: CubeState):
    return {
        "front":render_face(cstate.loc[0,:, :], cstate.cols, "front"),
        "back":render_face(cstate.loc[1,:, :], cstate.cols, "back"),
        "up":render_face(cstate.loc[:,0, :], cstate.cols, "up"),
        "down":render_face(cstate.loc[:,1, :], cstate.cols, "down"),
        "right":render_face(cstate.loc[:,:, 1], cstate.cols, "right"),
        "left":render_face(cstate.loc[:,:, 0], cstate.cols, "left"),
    }


def fill_2x2(y, x, faces_flat, ids_flat, face):
    faces_flat[y:(y+2), x:(x+2)] = face[0]
    ids_flat[y:(y+2), x:(x+2)] = face[1]


def _apply_trans(fun, *arrs):
    return tuple(map(fun, arrs))


def render_cube_arr(cstate: CubeState):
    faces = render_cube(cstate)
    faces_flat = np.zeros((8, 6), str)
    ids_flat = np.zeros((8, 6), str)
    faces_flat[...] = " "
    ids_flat[...] = " "
    fill_2x2(0, 2, faces_flat, ids_flat, _apply_trans(np.flipud,*faces["up"]))
    fill_2x2(2, 2, faces_flat, ids_flat, faces["front"])
    fill_2x2(4, 2, faces_flat, ids_flat, faces["down"])
    fill_2x2(6, 2, faces_flat, ids_flat, _apply_trans(np.flipud,*faces["back"]))
    fill_2x2(2, 0, faces_flat, ids_flat, _apply_trans(lambda a: np.rot90(a, k=-1), *faces["left"]))
    fill_2x2(2, 4, faces_flat, ids_flat, _apply_trans(lambda a: np.flipud(np.rot90(a, k=1)), *faces["right"]))
    return faces_flat, ids_flat


def pretty_render(cstate):
    col_arr, ids_arr = render_cube_arr(cstate)
    s = ""
    for i in range(len(col_arr)):
        s += " ".join(col_arr[i,:]) + "   " + " ".join(ids_arr[i,:]) + "\n"
    return s

swap_rot_possible_perms = np.array([
    [0, 1, 2],
    [0, 2, 1],
    [2, 1, 0],
    [1, 0, 2]
])


def random_cube_state(seed=None):
    rng = np.random.default_rng(seed)

    loc = np.arange(8)
    rng.shuffle(loc)
    loc = np.reshape(loc, (2, 2, 2)) # first coordinate is always zero
    cols = deepcopy(default_color_state)
    for i in range(cols.shape[0]):
        inds = swap_rot_possible_perms[rng.integers(4)]
        cols[i,:] = cols[i,inds]
    return CubeState(loc=loc, cols=cols)


def is_solved(cube_state:CubeState):
    for colors, _ in render_cube(cube_state).values():
        if len(np.unique(colors)) !=1:
            return False
    return True


if __name__ == "__main__":
    zero_state = CubeState()
    print(pretty_render(zero_state))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(0, 0))))
    print(pretty_render(apply_twist_action(zero_state, TwistAction(0, 1))))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(0, -1))))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(1, 1))))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(1, -1))))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(2, 1))))
    # print(pretty_render(apply_twist_action(zero_state, TwistAction(2, -1))))