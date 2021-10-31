from collections import defaultdict
from pprint import pprint

import pandas as pd

import core

datasheet = 'passengers.csv'
df = pd.read_csv(datasheet, index_col=False)

with_dims = core.get_dims(df)

# Probabilities
total = with_dims.amount.sum()

probabilities = defaultdict(float)
for amt, dim in zip(with_dims.amount, with_dims.dimensions):
    probabilities[dim] += amt / total

'''print('passengers:')
pprint(probabilities)
print(sum([value for key, value in probabilities.items()]))  # proove'''

# fig = core.get_plot(with_dims, 1)
