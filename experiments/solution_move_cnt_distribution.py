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

from cube_model.naive_model import random_cube_state_shuffled
from cube_solver.bidirectional_brute_force import find as bidirectional_brute_force

import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def experiment(seed):
    cube, _ = random_cube_state_shuffled(seed=seed)
    _, solution_actions = bidirectional_brute_force(cube)
    return len(solution_actions)

with mp.Pool(processes=10) as pool:
    cnts = pool.map(experiment, range(3000))

print(np.average(cnts), np.std(cnts))
plt.hist(cnts)
plt.savefig('distribution.png')