from pathlib import Path
import sys

from pprint import pprint
import numpy as np
from copy import deepcopy
from itertools import product
import math
from tqdm import tqdm
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cube_model.naive_model import CubeState, apply_twist_action, TwistAction, random_cube_state, is_solved, pretty_render, random_cube_state_shuffled

seed = 0
cube, gt_solution_actions = random_cube_state_shuffled(seed, max_len=7)

rng = np.random.default_rng(seed)
num_possible_combs = 3 ** 6 * math.factorial(7)

def find(cube: CubeState):

    visited = set()
    h = cube.hash()
    possible_actions = [TwistAction(axis, twist) for axis, twist in product(range(3), (-1, 1))]
    unvisited_solution_actions = {h:[]}

    with tqdm(total=num_possible_combs) as pbar:
        while len(unvisited_solution_actions) > 0:

            new_unvisited_solution_actions = {}
            for h, current_actions in unvisited_solution_actions.items():
                cube = CubeState.from_hash(h)
                pbar.update(1)

                for i in range(len(possible_actions)):
                    next_cube = apply_twist_action(cube, possible_actions[i])
                    if is_solved(next_cube):
                        return next_cube, [possible_actions[j] for j in current_actions + [i]]
                    h1 = next_cube.hash()
                    
                    if h1 in unvisited_solution_actions or h1 in visited:
                        continue
                    new_unvisited_solution_actions[h1] = current_actions + [i]
            
            visited.add(h)
            del unvisited_solution_actions[h]
            unvisited_solution_actions.update(new_unvisited_solution_actions)
            
    return None, []

cube_solved, solution_actions = find(cube)
print(pretty_render(cube))
print(pretty_render(cube_solved))
for a in solution_actions:
    print(a)

for a in gt_solution_actions:
    print(a)
