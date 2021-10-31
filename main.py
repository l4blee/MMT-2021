import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint

import core
from commercial import with_dims as com, probabilities as com_prob
from passengers import with_dims as pas, probabilities as pas_prob

# pprint(com_prob)
# pprint(pas_prob)

total_cars = 847000 + 71000
com_auto_prob = 71000 / total_cars
pas_auto_prob = 847000 / total_cars

total_probs = dict()
keys = list(com_prob.keys()) + list(pas_prob.keys())
for i in keys:
    total_probs[str(i)] = (com_prob.get(i, 0) * com_auto_prob
                           + pas_prob.get(i, 0) * pas_auto_prob) / 2

# print(total_probs)
print(sum(total_probs.values()))
'''df = pd.concat([pas, com])
fig = core.get_plot(df, 3)

plt.show()'''

x = sorted(total_probs.keys())
y = [total_probs[i] for i in x]

# print(x, y)

plt.bar(x, y)
plt.xticks(rotation=45)
plt.show()
