from pathlib import Path
import sys
from typing import List

from pprint import pprint
import numpy as np
from copy import deepcopy
from itertools import product
import math
from tqdm import tqdm
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cube_model.naive_model import CubeState, apply_twist_action, TwistAction, random_cube_state, is_solved, pretty_render, random_cube_state_shuffled, render_cube_arr

num_possible_combs = 3 ** 6 * math.factorial(7)

cube_solved = CubeState()

possible_actions = [TwistAction(axis, twist) for axis, twist in product(range(3), (-1, 1))]


def _apply_list_of_actions_inplace(cube:CubeState, actions: List[TwistAction]):
    for t in actions:
        apply_twist_action(cube, t, inplace=True)


def _get_inverse_solution(cube, action_inds, inplace=False):
    if not inplace:
        cube = deepcopy(cube)
    _apply_list_of_actions_inplace(cube, (possible_actions[i].inv() for i in reversed(action_inds)))
    return cube


def find(cube: CubeState):
    if is_solved(cube):
        return cube, []
    
    
    fwd_unvisited_solution_actions = {cube.hash():[]}
    fwd_visited = set()
    bwd_visited = {cube_solved.hash():[]}

    while len(fwd_unvisited_solution_actions) > 0:
        new_unvisited_solution_actions = {}
        for h, current_action_inds in fwd_unvisited_solution_actions.items():
            cube = CubeState.from_hash(h)
                
            for i in range(len(possible_actions)):

                next_cube = apply_twist_action(cube, possible_actions[i])

                next_action_inds = current_action_inds + [i]
                    
                h1 = next_cube.hash()
                if h1 in fwd_unvisited_solution_actions or h1 in fwd_visited:
                    continue

                if is_solved(next_cube):
                    return next_cube, [possible_actions[j] for j in next_action_inds]

                next_cube_inv = _get_inverse_solution(cube_solved, next_action_inds, inplace=False)
                h1_inv = next_cube_inv.hash()

                if h1_inv == h1:
                    _apply_list_of_actions_inplace(next_cube, (possible_actions[j] for j in next_action_inds))
                    return next_cube, [possible_actions[j] for j in next_action_inds] * 2
                    
                if h1 in bwd_visited:
                    _apply_list_of_actions_inplace(next_cube, (possible_actions[j] for j in bwd_visited[h1]))
                    return next_cube, [possible_actions[j] for j in next_action_inds] + [possible_actions[_] for _ in bwd_visited[h1]]
                    
                new_unvisited_solution_actions[h1] = bwd_visited[h1_inv] = next_action_inds
            
        fwd_visited.add(h)
        del fwd_unvisited_solution_actions[h]
        fwd_unvisited_solution_actions.update(new_unvisited_solution_actions)
            
    return None, []

if __name__ == "__main__":
    seed = 0
    cube, gt_solution_actions = random_cube_state_shuffled()

    # gt_solution_actions = [TwistAction(0, 1), TwistAction(0, 1)]
    # cube = CubeState()
    # for t in gt_solution_actions:
    #     apply_twist_action(cube, t, inplace=True)


    cube_solved, solution_actions = find(cube)
    print(pretty_render(cube))
    print(pretty_render(cube_solved))

    for a in solution_actions:
        print(a)
    print("-------------------")
    for a in gt_solution_actions:
        print(a)
