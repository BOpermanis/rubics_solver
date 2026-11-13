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

from cube_model.naive_model import random_cube_state
from cube_solver.bidirectional_brute_force import find as bidirectional_brute_force

import multiprocessing as mp
from collections import Counter

def experiment(seed):
    cube = random_cube_state(seed=seed)
    solution, _ = bidirectional_brute_force(cube, max_depth=6)
    return solution is not None

with mp.Pool(processes=10) as pool:
    solvables = pool.map(experiment, range(30))

print("solvability:", Counter(solvables).most_common())

