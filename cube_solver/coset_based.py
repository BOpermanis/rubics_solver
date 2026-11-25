from pathlib import Path
import sys

from copy import deepcopy
import pickle
import os

REPO_ROOT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, REPO_ROOT)

from cube_model.naive_model import CubeState, apply_twist_action, TwistAction, pretty_render, random_cube_state_shuffled

DATA_DIR = Path(REPO_ROOT) / "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

PATH_COSET_LOOKUP = str(DATA_DIR / "coset_cache.pickle")

L = TwistAction(0, 1)
L2 = [L] * 2

U = TwistAction(1, 1)
U2 = [U] * 2

F = TwistAction(2, 1)
F2 = [F] * 2


def inverse_compound_action(action):
    if isinstance(action, TwistAction):
        return [action.inv()]
    return list(reversed([t.inv() for t in action]))


def gen_coset(starting_states, actions):
    
    result_group = {k:None for k in starting_states}
    states_to_expand = deepcopy(starting_states)

    while len(states_to_expand) > 0:
        states_to_expand1 = set()
        for h in states_to_expand:
            cube = CubeState.from_hash(h)
                
            for action in actions:
                h1 = apply_twist_action(cube, action).hash()
                if h1 in result_group:
                    continue
                states_to_expand1.add(h1)
                result_group[h1] = inverse_compound_action(action)
        states_to_expand = states_to_expand1
    return result_group


def make_lookup():
    G3 = gen_coset({CubeState().hash()}, [L2, U2, F2])
    print(len(G3))

    G2 = gen_coset(G3, [L2, U2, F2, L])
    print(len(G2))

    G1 = gen_coset(G2, [L2, U2, F2, L, U])
    print(len(G1))

    with open(PATH_COSET_LOOKUP, "wb") as conn:
        pickle.dump((G1, G2, G3), conn)
    return G1, G2, G3


if os.path.exists(PATH_COSET_LOOKUP):
    with open(PATH_COSET_LOOKUP, "rb") as conn:
        G1, G2, G3 = pickle.load(conn)
else:
    G1, G2, G3 = make_lookup()


def traverse_G(cstate, G, G_target):
    h = cstate.hash()
    assert h in G
    actions = []
    while h not in G_target:
        cstate = CubeState.from_hash(h)
        action = G[h]
        actions.extend(action)
        apply_twist_action(cstate, action, inplace=True)
        h = cstate.hash()
    return cstate, actions


def find(cube):
    cstate_from_G2, actions_G1_to_G2 = traverse_G(cube, G1, G2)
    cstate_from_G3, actions_G2_to_G3 = traverse_G(cstate_from_G2, G2, G3)
    _, actions_G3_to_solved = traverse_G(cstate_from_G3, G3, {CubeState().hash()})
    actions_to_solution = actions_G1_to_G2 + actions_G2_to_G3 + actions_G3_to_solved
    return actions_to_solution


if __name__ == "__main__":
    cube, _ = random_cube_state_shuffled()
    print(pretty_render(cube))
    actions_to_solution = find(cube)
    # print(actions_to_solution)

    cube_solved = apply_twist_action(cube, actions_to_solution)
    print(pretty_render(cube_solved))

