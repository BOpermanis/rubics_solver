from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cube_model.naive_model import CubeState, apply_twist_action, TwistAction, random_cube_state, is_solved

seed = 42
cube = random_cube_state(seed)

rng = np.random.default_rng(seed)

iteration = 0
while not is_solved(cube):
    print(cube.hash_md5(), iteration)
    random_twist = TwistAction(rng.integers(3), rng.choice([-1, 0, 1]))
    apply_twist_action(cube, random_twist, inplace=True)
    iteration += 1