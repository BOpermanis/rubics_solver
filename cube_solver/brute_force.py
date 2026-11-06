from pathlib import Path
import sys

sys.setrecursionlimit(10000000)
from pprint import pprint
import numpy as np
from copy import deepcopy

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cube_model.naive_model import CubeState, apply_twist_action, TwistAction, random_cube_state, is_solved, pretty_render

seed = 0
cube = random_cube_state(seed)

rng = np.random.default_rng(seed)

num_seen = 0
def rec(cube: CubeState, history: set, trajectory:list[TwistAction]) -> list[TwistAction]:
    global num_seen
    if is_solved(cube):
        return trajectory
    history.add(cube.hash())
    print(len(history), num_seen)
    for axis in range(3):
        for twist in (-1, 1):
            action = TwistAction(axis, twist)
            next_cube = apply_twist_action(cube, action)
            if next_cube.hash() in history:
                num_seen += 1
                continue
            outputs = rec(next_cube, history, trajectory + [action])
            if len(outputs) > 0:
                return outputs
            
    return []

trajectory = rec(deepcopy(cube), set(), [])

pprint(trajectory)

cube_to_solve = deepcopy(cube)
for action in trajectory:
    apply_twist_action(cube_to_solve, action, inplace=True)

pretty_render(cube_to_solve)