import datetime
import time

import pandas as pd

date_now = time.strftime("%Y-%m-%d")

def get_t_n1_and_p1(negtive=False):
    k = [1,1,1,1,3,2,1]
    day_0 = datetime.datetime.strptime(Vday_0, "%Y-%m-%d")
    day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    day_2 = day_1 + datetime.timedelta(days=k[day_1.weekday()])
    return day_1.strftime("%Y-%m-%d"), day_2.strftime( "%Y-%m-%d")

df1 = pd.read_csv(f'DDD_{day_1}_t1_2_decision_buy.csv')
df2 = pd.read_csv(f'DDD_{day_2}_t1_2_decision_sell.csv')

    if (t2_2_high - t1_low) / t1_low >= 0.005:
        row1 = {'stock': ticker,
                'act_day': day_1,
                'act': 'buy',
                'target_price': t1_low,
                'act_low':0,
                'act_high':0,
                'buy':9999,
                'at_price':0}
        df1 = df1.append(row1, ignore_index=True)
        row2 = {'stock': ticker,
                'act_day': day_2,
                'act': 'sell',
                'target_price': t2_2_high,
                'gain_percent': round((t2_2_high - t1_low) / t1_low, 2)}
        df2 = df2.append(row2, ignore_index=True)

        df1.to_csv(f'DDD_{day_1}_t1_2_decision_buy.csv', index=False)
        df2.to_csv(f'DDD_{day_2}_t1_2_decision_sell.csv', index=False)
