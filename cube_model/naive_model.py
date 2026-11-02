from dataclasses import dataclass
import numpy as np
from collections import Counter

@dataclass
class TwistAction:
    twists: tuple[int] # for each of the rotation axis: -1, 0, 1


@dataclass
class CubeState:
    loc = np.reshape(np.arange(0, 8, dtype=int), (2, 2, 2)) # first coordinate is always zero
    rots = np.zeros((2, 2, 2), int) # first coordinate is always zero 


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


# location -> colors in rot 0 (at first ordered by location for easier definition by human)
piece_colors = [
    ("r", "g", "o"), #0
    ("r", "g", "w"), #1
    ("r", "b", "o"), #2
    ("r", "b", "w"), #3
    ("y", "g", "o"), #4
    ("y", "g", "w"), #5
    ("y", "b", "o"), #6
    ("y", "b", "w")  #7
]
piece_colors = np.asarray(piece_colors).reshape((-1, 3)) # reshape from id -> colors

cntr = Counter(piece_colors.flatten())
assert len(cntr) == 6 and cntr.most_common()[0][1] == 4, cntr


def render_face(loc, rots, fname):
    loc = loc.flatten()
    rots = rots.flatten()

    # print(fname, loc)

    colors = piece_colors[loc,:]
    colors = colors[np.arange(4), face_coordinate[fname]].reshape((2,2))

    return colors


def apply_twist_action(cstate: CubeState, action: TwistAction) -> CubeState:
    new_cstate = CubeState()
    new_cstate.loc[1,:,:] = np.rot90(cstate.loc[1,:,:], action.twists[0], axes=(0, 1))
    new_cstate.loc[:,1,:] = np.rot90(cstate.loc[:,1,:], action.twists[1], axes=(0, 1))
    new_cstate.loc[:,:,1] = np.rot90(cstate.loc[:,:,1], action.twists[2], axes=(0, 1))

    new_cstate.rots[1,:,:] = (cstate.rots[1,:,:] + action.twists[0]) % 3
    new_cstate.rots[:,1,:] = (cstate.rots[:,1,:] + action.twists[1]) % 3
    new_cstate.rots[:,:,1] = (cstate.rots[:,:,1] + action.twists[2]) % 3
    
    return new_cstate


def render_cube(cstate: CubeState):
    return {
        "front":render_face(cstate.loc[0,:, :], cstate.rots[0,:, :], "front"),
        "back":render_face(cstate.loc[1,:, :], cstate.rots[1,:, :], "back"),
        "up":render_face(cstate.loc[:,0, :], cstate.rots[:,0, :], "up"),
        "down":render_face(cstate.loc[:,1, :], cstate.rots[:,1, :], "down"),
        "right":render_face(cstate.loc[:,:, 0], cstate.rots[:,:, 0], "right"),
        "left":render_face(cstate.loc[:,:, 1], cstate.rots[:,:, 1], "left"),
    }


def fill_2x2(y, x, faces_flat, face):
    faces_flat[y:(y+2), x:(x+2)] = face


def render_cube_arr(cstate: CubeState):
    faces = render_cube(cstate)
    faces_flat = np.zeros((8, 6), str)
    faces_flat[...] = " "
    fill_2x2(0, 2, faces_flat, faces["up"])
    fill_2x2(2, 2, faces_flat, faces["front"])
    fill_2x2(4, 2, faces_flat, faces["down"])
    fill_2x2(6, 2, faces_flat, faces["back"])
    fill_2x2(2, 0, faces_flat, faces["left"])
    fill_2x2(2, 4, faces_flat, faces["right"])
    return faces_flat


def pretty_render(cstate):
    arr = render_cube_arr(cstate)
    s = ""
    for i in range(len(arr)):
        s += " ".join(arr[i,:]) + "\n"
    return s


if __name__ == "__main__":
    zero_state = CubeState()
    print(pretty_render(zero_state))
    print(pretty_render(apply_twist_action(zero_state, TwistAction((1, 0, 0)))))