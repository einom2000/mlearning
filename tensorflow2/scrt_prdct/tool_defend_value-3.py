import os

import matplotlib.pyplot as plt
import pandas as pd

import tool_day_off_filter

date_now = tool_day_off_filter.get_date_now()
start_date = '2020-12-28'

date_list = [start_date,]
next_day = start_date

while True:
    next_day = tool_day_off_filter.get_first_working_day(next_day, delta=1)
    if int(next_day.replace('-', '')) <= int(date_now.replace('-', '')):
        date_list.append(next_day)
    else:
        break

stock_list = []
stock_list.extend(['sh600030', 'sh600600', 'sh600648', 'sh600585', 'sh600529'])
stock_list.extend(['sh600587', 'sh600685', 'sh600058', 'sh600547'])

lookup_codes = stock_list.copy()

for lookup_code in lookup_codes:
    history_low = pd.DataFrame(columns=['date', 'forecast_low', 'act_low'])
    for day in date_list:
        df = pd.read_csv(f'DDD_{day}_t1_2_decision_buy.csv')
        query = df[df['stock']==lookup_code]
        if not query.empty:
            history_low = history_low.append({
                            'date': day,
                            'forecast_low': query['target_price'].min(),
                            'act_low': query['act_low'].min()
            }, ignore_index=True)

    history_high = pd.DataFrame(columns=['date', 'forecast_high', 'act_high'])
    for day in date_list[:-1]:
        df = pd.read_csv(f'DDD_{day}_t1_2_decision_buy.csv')
        query = df[df['stock']==lookup_code]
        day_1 = tool_day_off_filter.get_first_working_day(day, delta=1)
        df2 = pd.read_csv(f'DDD_{day_1}_t1_2_decision_buy.csv')
        query2 = df2[df2['stock']==lookup_code]
        if (not query.empty) and (not query2.empty):
            history_high = history_high.append({
                            'date': day_1,
                            'forecast_high': query['T2-sell'].min(),
                            'act_high': query2['act_high'].min()
            }, ignore_index=True)

    def plot_graph(history_low, history_high, plot_filename=''):
        plt.plot(history_low['forecast_low'], c='b')
        plt.plot(history_low['act_low'], c='y')
        plt.plot(history_high['forecast_high'], c='g')
        plt.plot(history_high['act_high'], c='r')
        plt.xticks(history_low.index, history_low["date"].values)
        plt.xlabel(f"{lookup_code}--Days")
        plt.ylabel("Price")
        plt.legend(["Predicted Low", "Actual Low", "Predicted High", "Actual High"])
        # plt.show()
        date_now = tool_day_off_filter.get_date_now()
        if os.path.isfile(f'DDD_{lookup_code}_updated_{date_now}.png'):
            print(f'deleting DDD_{lookup_code}_updated_{date_now}.png')
            os.remove(f'DDD_{lookup_code}_updated_{date_now}.png')
        plt.savefig(f'DDD_{lookup_code}_updated_{date_now}.png')
        plt.clf()
    # print(history_low, history_high)
    plot_graph(history_low, history_high)
