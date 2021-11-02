from collections import defaultdict

import pandas as pd

with_dims = pd.read_csv('commercial.csv')
with_dims = with_dims.sort_values(by=['dimensions', 'car'], ascending=True)

# Probabilities
total = with_dims.amount.sum()

probabilities = defaultdict(float)
for amt, dim in zip(with_dims.amount, with_dims.dimensions):
    probabilities[dim] += amt / total
