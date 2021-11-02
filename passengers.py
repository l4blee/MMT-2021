from collections import defaultdict

import pandas as pd

import search

'''datasheet = 'passengers.csv'
df = pd.read_csv(datasheet, index_col=False)

with_dims = core.get_dims(df)
with_dims.to_csv('passengers_d.csv', index=False)'''

datasheet = 'passengers_d.csv'
with_dims = pd.read_csv(datasheet)

# Probabilities
total = with_dims.amount.sum()

probabilities = defaultdict(float)
for amt, dim in zip(with_dims.amount, with_dims.dimensions):
    probabilities[dim] += amt / total

