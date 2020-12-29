import datetime
import time

import pandas as pd

date_now = time.strftime("%Y-%m-%d")

def get_t_posi_1(today):
    k = [1,1,1,1,3,2,1]
    day_0 = datetime.datetime.strptime(today, "%Y-%m-%d")
    day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    return day_1.strftime("%Y-%m-%d")

def get_t_neg_1(today):
    k = [-3,-1,-1,-1,-1,-1,-2]
    day_0 = datetime.datetime.strptime(today, "%Y-%m-%d")
    day_n1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    return day_n1.strftime("%Y-%m-%d")

day_n1 = get_t_neg_1(date_now)

df1 = pd.read_csv(f'DDD_{date_now}_t1_2_decision_buy.csv')

stocks = list(dict.fromkeys(list(df1['stock'])))

for ticker in stocks:
    act_day = df1[df1['stock'] == ticker].min()['act_day']
    try:
        df2 = pd.read_csv(f'csv-original\\{ticker}_{date_now}.csv')
    except FileNotFoundError:
        df2 = pd.read_csv(f'csv-original\\{ticker}_{act_day}.csv')

    df = df2[df2['Unnamed: 0.1'] == act_day]
    df_t2 = df2[df2['Unnamed: 0.1'] == date_now]
    if not df.empty:
        df1.at[df1['stock']==ticker, 'act_low'] = df['low'].item()
        df1.loc[df1['stock'] == ticker, 'act_high'] = df2[df2['Unnamed: 0.1'] == act_day]['high'].item()

    if not df_t2.empty:
        df1.at[df1['stock'] == ticker, 'T2_high'] = df2[df2['Unnamed: 0.1'] == date_now]['high'].item()

df1['act_low_dif'] = round((df1['target_price'] - df1['act_low']), 2)
df1.loc[df1['target_price'] >= df1['act_low'], 'at_price'] = df1['target_price']
df1.loc[df1['target_price'] >= df1['act_low'], 'buy'] = 9999
print(df1.to_string())

df1.to_csv(f'DDD_{day_n1}_t1_2_decision_buy.csv', index=False)




