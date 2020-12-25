import os
import time

import pandas as pd

import day_to_csv
import remove_file


def init():
    date_now = time.strftime("%Y-%m-%d")
    try:
        df = pd.read_csv(f'csv-original\\sh000300_{date_now}.csv')
    except FileNotFoundError:
        remove_file.remove('csv-original\\', startwith='sh000300')
        day_to_csv.day_to_csv('000300', market='sh')
        df = pd.read_csv(f'csv-original\\sh000300_{date_now}.csv')

    if not os.path.exists(f'csv-original\\sh000300_{date_now}_pct_300.csv'):
        adjclose = df['adjclose']
        vol = df['volume']
        # print(len(adjclose))
        pct_index = [0.0, ]
        pct_vol = [0.0, ]
        for i in range(1, len(adjclose)):
            k = ((adjclose[i] / adjclose[i - 1]) - 1) * 100
            j = ((vol[i] / vol[i - 1]) - 1) * 100
            pct_index.append(k)
            pct_vol.append(j)
        df['pct_index'] = pct_index
        df['pct_vol'] = pct_vol
        remove_file.remove('csv-original\\', endswith='_pct_300.csv')
        df.to_csv(f'csv-original\\sh000300_{date_now}_pct_300.csv', index=False)

def join_300(ticker):

# df = pd.read_csv('tutu.csv')
# dates = df['Unnamed: 0'].tolist()
# df_300 = pd.read_csv('sample_1.csv')
# dates_300 = df_300['Unnamed: 0'].tolist()
# pct_index_300 = []
# pct_vol_300 = []
#
# for date in dates:
#     if not date in dates_300:
#         pct_index_300.append(0.0)
#         pct_vol_300.append(0.0)
#     else:
#         pct_index_300.append(float(df_300[df_300['Unnamed: 0'] == date]['pct_index']))
#         pct_vol_300.append(float(df_300[df_300['Unnamed: 0'] == date]['pct_vol']))
#
# df['pct_index_300'] = pct_index_300
# df['pct_vol_300'] = pct_vol_300
#
# df.to_csv('tutu_1.csv')