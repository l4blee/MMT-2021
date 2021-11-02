from pprint import pprint
from collections import defaultdict
import pandas as pd

import matplotlib.pyplot as plt

from commercial import probabilities as com_prob, with_dims as com
from passengers import probabilities as pas_prob, with_dims as pas

total_cars = 847000 + 71000  # pas / com
com_auto_prob = 71000 / total_cars
pas_auto_prob = 847000 / total_cars

# Per car probs

pas_am = pas.amount.sum()
com_am = com.amount.sum()
total_am_probs = dict()

for _, i in pas.iterrows():
    total_am_probs[i.car] = (i.amount / pas_am) * pas_auto_prob

for _, i in com.iterrows():
    total_am_probs[i.car] = (i.amount / com_am) * com_auto_prob

total_am_probs = sorted(total_am_probs.items(), key=list[0])

base = pd.concat([pas, com], ignore_index=True)
# base = base.set_index('car')
# print(base)
# base = base.sort_values(by='car')

base['probability'] = [i[1] for i in total_am_probs]
base['wheelbase'] = [i - i % 50 for i in base.wheelbase]


avg_wheelbase = int(sum([i.wheelbase * i.probability for _, i in base.iterrows()]))
avg_dimensions = int(sum([i.dimensions * i.probability for _, i in base.iterrows()]))

# Total probabilities
total_probs = dict()
keys = list(com_prob.keys()) + list(pas_prob.keys())
for i in keys:
    total_probs[str(int(i))] = (com_prob.get(i, 0) * com_auto_prob + pas_prob.get(i, 0) * pas_auto_prob)


if __name__ == '__main__':
    print(base)

    print(f'{avg_wheelbase=}')
    print(f'{avg_dimensions=}')

    x = sorted(total_probs.keys())
    y = [total_probs[i] for i in x]

    '''plt.figure('cars_length_prob')
    plt.plot(x, y)
    plt.xlabel('car length')
    plt.ylabel('probability')
    plt.xticks(rotation=45)
    plt.tight_layout()
'''
    probs = defaultdict(float)
    for _, i in base.iterrows():
        probs[i.wheelbase] += i.probability

    x, y = zip(*sorted(probs.items()))
    x = [str(i) for i in x]

    print(x, y)

    plt.figure('wheelbases_prob')
    plt.plot(x, y)
    # plt.xlabel('car wheelbase')
    # plt.ylabel('probability')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
