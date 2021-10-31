from collections import defaultdict
from pprint import pprint

import pandas as pd

import core

with_dims = pd.read_csv('commercial.csv')
with_dims = with_dims.sort_values(by=['dimensions', 'car'], ascending=True)

# Probabilities
total = with_dims.amount.sum()

probabilities = defaultdict(float)
for amt, dim in zip(with_dims.amount, with_dims.dimensions):
    probabilities[dim] += amt / total

'''print('commercial:')
pprint(probabilities)
print(sum([value for key, value in probabilities.items()]))  # proove'''

# fig = core.get_plot(with_dims, 2)
