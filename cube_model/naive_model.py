from dataclasses import dataclass
import numpy as np

@dataclass
class TwistAction:
    twists: tuple[int] # 3 rotations of the free 4-piece planes


@dataclass
class CubeState:
    loc = np.reshape(np.arange(0, 8, dtype=int), (2, 2, 2)) # first coordinate is always zero
    rots = np.zeros((2, 2, 2), int) # first coordinate is always zero 


colors_full = ["red", "yellow", "green", "blue", "orange", "black"]
colors = ['r', 'y', 'g', 'b', 'o', 'b']
assert all((a==b for a, b in zip(colors, [_[0] for _ in colors_full])))


# location -> rot offset
location_rotation_offset = [
    [
        [0, 0],
        [0, 0]
    ],
    [
        [2, 2],
        [2, 2]
    ]
]
location_rotation_offset = np.asarray(location_rotation_offset).flatten()

# location -> colors in rot 0 (at first ordered by location for easier definition by human)
piece_colors = [
    [
        [("r", "g", "b"), ("r", "r", "r")],
        [("r", "r", "r"), ("r", "r", "r")]
    ],
    [
        [("y", "g", "b"), ("y", "r", "r")],
        [("y", "r", "r"), ("y", "r", "r")]
    ]
]
piece_colors = np.asarray(piece_colors).reshape((-1, 3)) # reshape from id -> colors



def render_face(loc, rots):
    loc = loc.flatten()
    rots = (location_rotation_offset[loc] + rots.flatten()) % 3
    colors = piece_colors[loc,:][np.arange(4),rots].reshape((2,2))
    # print(loc)
    # print(colors)
    # exit()
    return colors


def render_cube(cstate: CubeState):
    return {
        "front":render_face(cstate.loc[0,:, :], cstate.rots[0,:, :]),
        "back":render_face(cstate.loc[1,:, :], cstate.rots[1,:, :]),
        "up":render_face(cstate.loc[:,0, :], cstate.rots[:,0, :]),
        "down":render_face(cstate.loc[:,1, :], cstate.rots[:,1, :]),
        "right":render_face(cstate.loc[:,:, 0], cstate.rots[:,:, 0]),
        "left":render_face(cstate.loc[:,:, 1], cstate.rots[:,:, 1]),
    }
    


surfaces = render_cube(CubeState())

for k, f in surfaces.items():
    print("------------",k)
    print(f)

exit()

def apply_twist_action(cstate: CubeState, action: TwistAction) -> CubeState:
    pass




if __name__ == "__main__":
    # Example usage
    twist_action = TwistAction(twists=(1, 2, 0))
    cube_state = CubeState(loc=(0, 1, 2, 3), rots=(0, 1, 2, 0))

    print(twist_action)
    print(cube_state)