from collections import defaultdict

import bs4
import matplotlib.pyplot as plt
import pandas as pd
import requests as rq


def get_dims(df: pd.DataFrame) -> pd.DataFrame:  # Только для легковушек, грузовики не работают
    for index, i in enumerate(df.car):
        print(index, end=' ')
        query = 'https://google.com/search?q=' + '+'.join(i.split(' ') + ['dimensions'])
        print(query)
        res = rq.get(query)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        length = soup.find('div', class_='BNeawe iBp4i AP7Wnd').text.lower().split(' x ')[0]
        length = ' '.join(length.split(' ')[0].split('\xa0')[:-1]).split('-')
        spreads = [int(''.join(i.split(' '))) for i in length]
        avg = sum(spreads) / len(spreads)

        df.at[index, 'dimensions'] = int(avg - avg % 50)

    df = df.sort_values(by=['dimensions', 'car'], ascending=True)

    return df


def get_plot(df: pd.DataFrame, index) -> plt.Figure:
    figure = plt.figure(index)

    dims = defaultdict(int)
    for index, row in df.iterrows():
        dims[str(row.dimensions)] += int(row.amount)

    plt.bar(list(dims.keys()), dims.values())
    plt.xticks(rotation=45)

    return figure
