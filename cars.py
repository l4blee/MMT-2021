from probs import base
import random

range_border = 10 ** 9

weights = [i * range_border for i in base.probability]

RANGES = dict()
rngs = list()
for index, i in base.iterrows():
    min_ = rngs[index - 1][1] if index > 0 else 0
    max_ = min_ + weights[index]

    RANGES[i.car] = (min_, max_)
    rngs.append((min_, max_))
else:
    del rngs

base = base.set_index('car')


class Car:
    def __init__(self, name: str, length: int, wheelbase: int, x: int):
        # exp_driver = random.choices([False, True], cum_weights=(82, 385))[0]
        exp_driver = False
        self.parking_gap = random.choice([wheelbase / 2, [1.5, 0.5][exp_driver]])

        self.name = name
        self.length = length
        self.wheelbase = wheelbase
        self.x_pos = x

    def __repr__(self):
        return f'Car(name={self.name}, len={self.length}, wb={self.wheelbase})'

    def __bool__(self):
        return False

    @classmethod
    def get_random(cls, x: int = None):
        seed = random.randrange(0, range_border)
        for name, value in RANGES.items():
            if value[0] < seed < value[1]:
                length = base.at[name, 'dimensions']
                wheelbase = base.at[name, 'wheelbase']
                return cls(name, length, wheelbase, x)
