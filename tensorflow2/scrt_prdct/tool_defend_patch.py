import datetime
import glob
import os
import shutil

import pandas as pd

import day_to_csv
import tool_day_off_filter
import tool_get_per_of_300


#!!!! must run on the T+1 day  actualy + 1


def patch():

    # def get_t_posi_1(today):
    #     k = [1, 1, 1, 1, 3, 2, 1]
    #     day_0 = datetime.datetime.strptime(today, "%Y-%m-%d")
    #     day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    #     return day_1.strftime("%Y-%m-%d")

    if not os.path.isdir('decision_back\\'):
        os.mkdir('decision_back\\')

    date_now = tool_day_off_filter.get_date_now()
    day_p1 = tool_day_off_filter.get_first_working_day(date_now, delta=1)

    df1 = pd.read_csv(f'DDD_{date_now}_t1_2_decision_buy.csv')

    stocks = list(dict.fromkeys(list(df1['stock'])))

    for ticker in stocks:

        act_day = df1[df1['stock'] == ticker].min()['act_day']

        if not os.path.isfile(f'csv-original\\{ticker}_{date_now}.csv'):
            day_to_csv.day_to_csv(single_code=ticker[2:], market=ticker[:2])
            # put 300 index growing percent to the csv
            tool_get_per_of_300.join_300(ticker)

        df2 = pd.read_csv(f'csv-original\\{ticker}_{date_now}.csv')

        df = df2[df2['Unnamed: 0.1'] == act_day]
        df_t2 = df2[df2['Unnamed: 0.1'] == day_p1]
        if not df.empty:
            df1.at[df1['stock']==ticker, 'act_low'] = df['low'].item()
            df1.loc[df1['stock'] == ticker, 'act_high'] = df2[df2['Unnamed: 0.1'] == act_day]['high'].item()

        if not df_t2.empty:
            df1.at[df1['stock'] == ticker, 'T2_high'] = df2[df2['Unnamed: 0.1'] == date_now]['high'].item()

    df1['act_low_dif'] = round((df1['target_price'] - df1['act_low']), 2)
    df1.loc[df1['target_price'] >= df1['act_low'], 'at_price'] = df1['target_price']
    df1.loc[df1['target_price'] >= df1['act_low'], 'buy'] = 0
    print(df1.to_string())
    now = str(datetime.datetime.now())[:19]
    now = now.replace(":", "_")
    shutil.copy(f'DDD_{act_day}_t1_2_decision_buy.csv', f'decision_back\\DDD_{act_day}_t1_2_decision_buy_backon_{now}.csv')
    df1.to_csv(f'DDD_{act_day}_t1_2_decision_buy.csv', index=False)


# def get_previous_day(day0, pri=1):
#     k = [-3, -1, -1, -1, -1, -1, -2]
#     pri_day = datetime.datetime.strptime(day0, "%Y-%m-%d")
#     for _ in range(pri):
#         pri_day = pri_day+ datetime.timedelta(days=k[pri_day.weekday()])  # 0,1,2,3,4,5,6(sun)
#     return pri_day.strftime("%Y-%m-%d")


def clear_old_catch():
    date_now = tool_day_off_filter.get_date_now()
    catch_dirs =['results\\', 'data\\', 'csv-results\\', 'csv-original\\']
    for i in range(3, 5):
        old_day = tool_day_off_filter.get_first_working_day(date_now, delta=i*(-1))
        print(f"clearing following catched files of day {old_day}....")
        for catch_dir in catch_dirs:
            lists = glob.glob(f"{catch_dir}*{old_day}*.*")
            if lists:
                print(lists)
                for file in lists:
                    os.remove(file)


def pool_list():
    now = str(datetime.datetime.now())[:19]
    now = now.replace(":", "_")
    shutil.copy(f'DDD_stock_list.csv',
                f'decision_back\\DDD_stock_list.csv_backon_{now}.csv')
    date_now = tool_day_off_filter.get_date_now()
    if not os.path.isfile('DDD_stock_list.csv'):
        df = pd.DataFrame(columns=['stock', 'inpool_date', 'volume', 'inpool_price',
                                   'toll_fees', 'outpool_date', 'outpool_price', 'margin'])
        df.to_csv('DDD_stock_list.csv', index=False)

    df = pd.read_csv('DDD_stock_list.csv')

    for i in range(5, -1, -1):
        history_day = tool_day_off_filter.get_first_working_day(date_now, delta=i * (-1))
        if os.path.isfile(f'DDD_{history_day}_t1_2_decision_buy.csv'):
            df_decision = pd.read_csv(f'DDD_{history_day}_t1_2_decision_buy.csv')
            rows = df_decision[(df_decision['buy'] != 0)]
            if not rows.empty:
                for index, row in rows.iterrows():

                    if df[(df['stock']==row['stock']) & (df['inpool_date']==row['act_day']) &
                          (df['volume']==row['buy']) & (df['inpool_price']==row['at_price'])].empty:
                        query = {'stock': row['stock'],
                                'inpool_date': row['act_day'],
                                'volume': row['buy'],
                                'inpool_price': row['at_price'],
                                'toll_fees': 0,
                                'outpool_date': 0,
                                'outpool_price': 0,
                                'margin': 0
                                }
                        df = df.append(query, ignore_index=True)
            rows = df_decision[(df_decision['sell'] != 0)]
            if not rows.empty:
                for index, row in rows.iterrows():
                    his_df = df[(df['stock']==row['stock']) & (df['volume']==row['sell']) &
                          (df['outpool_price']==0)]
                    outpool_date = datetime.datetime.strptime(row['act_day'], "%Y-%m-%d")
                    if not his_df.empty:
                        for ind, que in his_df.iterrows():
                            inpool_date = datetime.datetime.strptime(que['inpool_date'], "%Y-%m-%d")
                            if outpool_date>=inpool_date:
                                df.loc[ind, 'outpool_date'] = row['act_day']
                                df.loc[ind, 'outpool_price'] = row['selling_price']

                                df.loc[ind, 'margin'] = round((df.loc[ind, 'outpool_price'] - df.loc[ind, 'inpool_price']) \
                                                        * df.loc[ind, 'volume'], 2)

            df.to_csv('DDD_stock_list.csv', index=False)


pool_list()