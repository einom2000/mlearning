import datetime
import os
import time

import pandas as pd

import collects
import collects_2dlow
import day_to_csv
import defends
import remove_file
import tool_get_per_of_300


def predict(stock, module='defend', daily_forecast_dir=''):

    date_now = time.strftime("%Y-%m-%d")

    if module == 'defend':
        pre_fix = 'defend_'
        LOOKUP_STEP = 1
        INIT_EPOCHS = 2 * EPOCHS_RATIO
        SECOND_EPOCHS = 2 * EPOCHS_RATIO

        daily_forecast_filename = os.path.join(daily_forecast_dir, f"{pre_fix}{date_now}_{LOOKUP_STEP}_forecast.csv")

        if os.path.isfile(daily_forecast_filename):
            try:
                data = pd.read_csv(daily_forecast_filename)
            except:
                data = []
        else:
            data = []

        # print(data)
        dt = []
        print(stock)
        saved_epochs = 0
        if not isinstance(data, list):
            saved_epochs = data[data['stock'] == stock]['uptonow_epochs'].max()
            if type(saved_epochs) == float:
                saved_epochs = 0
        if isinstance(data, list) or saved_epochs < 800:
            epochs = INIT_EPOCHS
        else:
            epochs = SECOND_EPOCHS
        future_price, reachability, reachability_2 = \
            defends.go_defend(stock, lookup_step=LOOKUP_STEP, flush_result=False, epochs=epochs, only_forecast=False)
        epochs += saved_epochs
        dt.append({'stock': stock, 'fc_date': date_now,
                   'T+1_lowest': round(future_price, 2), 'reachability': reachability,
                   'T+1_lowest_+0.5%': round(future_price * 1.005, 2), 'reachability_2': reachability_2,
                   'uptonow_epochs' : epochs})
        dt = pd.DataFrame.from_dict(dt)
        if isinstance(data, list):
            data = dt.copy()
        else:
            frames = [data, dt]
            data = pd.concat(frames)
        # print(data)
        data.to_csv(daily_forecast_filename, index=False)
        return round(float(future_price), 2), round(reachability, 2), round(reachability_2, 2), epochs

    elif module == 'collect':
        pre_fix = 'collect'
        LOOKUP_STEP = 2
        INIT_EPOCHS = 3 * EPOCHS_RATIO
        SECOND_EPOCHS = 3 * EPOCHS_RATIO
        daily_forecast_filename = os.path.join(daily_forecast_dir, f"{pre_fix}{date_now}_{LOOKUP_STEP}_forecast.csv")

        if os.path.isfile(daily_forecast_filename):
            try:
                data = pd.read_csv(daily_forecast_filename)
            except:
                data = []
        else:
            data = []

        # print(data)
        dt = []
        print(stock)
        saved_epochs = 0
        if not isinstance(data, list):
            saved_epochs = data[data['stock'] == stock]['uptonow_epochs'].max()
            if type(saved_epochs) == float:
                saved_epochs = 0
        if isinstance(data, list) or saved_epochs < 800:
            epochs = INIT_EPOCHS
        else:
            epochs = SECOND_EPOCHS
        future_price, reachability, reachability_2= \
            collects.go_collect(stock, lookup_step=LOOKUP_STEP, flush_result=False, epochs=epochs, only_forecast=False)
        epochs += saved_epochs
        dt.append({'stock': stock, 'fc_date': date_now, 'future_days': LOOKUP_STEP,
                   'future_high': future_price, 'reachability': reachability, "0.5%_off": reachability_2,
                   'uptonow_epochs': epochs})
        dt = pd.DataFrame.from_dict(dt)
        if isinstance(data, list):
            data = dt.copy()
        else:
            frames = [data, dt]
            data = pd.concat(frames)
        # print(data)
        data.to_csv(daily_forecast_filename, index=False)

        return round(float(future_price), 2), round(reachability, 2), round(reachability_2, 2), epochs

    elif module == 'collect_low':
        pre_fix = 'collect_low'
        LOOKUP_STEP = 2
        INIT_EPOCHS = 3 * EPOCHS_RATIO
        SECOND_EPOCHS = 3 * EPOCHS_RATIO
        daily_forecast_filename = os.path.join(daily_forecast_dir, f"{pre_fix}{date_now}_{LOOKUP_STEP}_forecast.csv")

        if os.path.isfile(daily_forecast_filename):
            try:
                data = pd.read_csv(daily_forecast_filename)
            except:
                data = []
        else:
            data = []

        # print(data)
        dt = []
        print(stock)
        saved_epochs = 0
        if not isinstance(data, list):
            saved_epochs = data[data['stock'] == stock]['uptonow_epochs'].max()
            if type(saved_epochs) == float:
                saved_epochs = 0
        if isinstance(data, list) or saved_epochs < 800:
            epochs = INIT_EPOCHS
        else:
            epochs = SECOND_EPOCHS
        future_price, reachability, reachability_2= \
            collects_2dlow.go_collect(stock, lookup_step=LOOKUP_STEP, flush_result=False, epochs=epochs, only_forecast=False)
        epochs += saved_epochs
        dt.append({'stock': stock, 'fc_date': date_now, 'future_days': LOOKUP_STEP,
                   'future_low': future_price, 'reachability': reachability, "0.5%_up": reachability_2,
                   'uptonow_epochs': epochs})
        dt = pd.DataFrame.from_dict(dt)
        if isinstance(data, list):
            data = dt.copy()
        else:
            frames = [data, dt]
            data = pd.concat(frames)
        # print(data)
        data.to_csv(daily_forecast_filename, index=False)

        return round(float(future_price), 2), round(reachability, 2), round(reachability_2, 2), epochs

    else:
        print('Unknown module...terminated!')


def get_t_1_and_2(Vday_0):
    k = [1,1,1,1,3,2,1]
    day_0 = datetime.datetime.strptime(Vday_0, "%Y-%m-%d")
    day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    day_2 = day_1 + datetime.timedelta(days=k[day_1.weekday()])
    return day_1.strftime("%Y-%m-%d"), day_2.strftime( "%Y-%m-%d")


def value(df1, df2, ticker, pool, max_pool=20):

    global PROFIT_COLLECTED, LL, LH, spirit_2l, spirit_2h

    # attr_1 ( if the 2 adj is >>>, give a - 0.05% ...
    Vday_0_adjc = round(df1[-1:]['adjclose'].item(), 2)
    Vday_n1_adj = float(df1[-2:-1]['adjclose'].item())
    Vday_n2_adj = float(df1[-3:-2]['adjclose'].item())


    def get_total_from_pool(pool):
        total = 0.0
        for i in pool:
            total += i[0] * i[1]
        return total

    Vday_0 = str(df1[-1:]['Unnamed: 0.1'].item())
    print(Vday_0)
    Vday_0_actlow = float(df1[-1:]['low'].item())
    Vday_0_acthigh = float(df1[-1:]['high'].item())
    Vday_1, Vday_2 = get_t_1_and_2(Vday_0)
    Vday_1_actlow = float(df2[0:1]['low'].item())
    Vday_1_acthigh = float(df2[0:1]['high'].item())
    Vday_2_actlow = float(df2[1:2]['low'].item())
    Vday_2_acthigh = float(df2[1:2]['high'].item())
    Vday_2_actc = float(df2[1:2]['adjclose'].item())

    t1_low, rch_1, rch_2, epo_d = predict('sh999999')
    t2_high,rch2_1, rch2_2, epo_c = predict('sh999999', module='collect')
    t2_2_high = round(t2_high * 0.995, 2)
    t2_low, rch2_1, rch2_2, epo_c = predict('sh999999', module='collect_low')
    t2_2_low = round(t2_low * 1.005, 2)


    spirit = 1  # spirit of trend
    if Vday_n2_adj > Vday_n1_adj > Vday_0_adjc:
        spirit = 0.995
    elif Vday_n2_adj < Vday_n1_adj < Vday_0_adjc:
        spirit = 1.005
    else:
        spirit = 1

    # arg2 for adjust misforecast   paused
    if Vday_0_actlow > LL:
        spirit_2l = (Vday_0_actlow - LL) / LL + 1
        spirit_2h = (Vday_0_actlow - LL) / LL + 1

    if Vday_0_actlow < LL < 900:
        spirit_2l = 1 - (Vday_0_actlow - LL) / LL
        spirit_2h = 1 - (Vday_0_actlow - LL) / LL

    if Vday_0_acthigh < LH:
        try:
            spirit_2h = 1 - (LH - Vday_0_acthigh) / LH
        except ZeroDivisionError:
            spirit_2h = 1

    if Vday_0_acthigh > LH > 1:
        spirit_2h = (Vday_0_acthigh - LH) / LH + 1

    spirit_2l = spirit_2h =1

    t1_low = round(t1_low * spirit * spirit_2l, 2)
    LL = t1_low

    t2_2_high = round(t2_2_high * spirit * spirit_2h * spirit_2l, 2)
    LH = t2_2_high

    with open(f'memo_{ticker}_v2.txt', 'a') as f:
        f.write(str(pool) + '\n')
        f.write(f"Vday_0 = {Vday_0} \n")
        f.write(f"Vday_0's adjclose = {Vday_0_adjc} \n")
        f.write(f"T+1 {Vday_1} actual low at {Vday_1_actlow} \n")
        f.write(f"T+1 {Vday_1} forecast low at {t1_low} with {rch_1} possibility \n")
        f.write(f"T+2 {Vday_2} forecast high at {t2_2_high} with {rch2_2} \n")
        f.write(f"T+2 {Vday_2} actual high at {Vday_2_acthigh} \n")
        f.write(f"above with spirits of {spirit} & {spirit_2l}  & {spirit_2h}\n")
        f.write(f"T+2 {Vday_2} actual close at {Vday_2_actc} \n")

        # buying strategy
        if len(pool) < max_pool + 1:
            # stock buying strategy
            if t1_low >= Vday_1_actlow and (t2_2_high - t1_low) / t1_low >= 0.005:  # 0.5% margin
                f.write(f'on {Vday_1} buy ' + str(pool[0][0]) + f' at {t1_low} \n')  # pool[0][0] is the min_buy_vol
                pool.append([pool[0][0], t1_low, 1])
                total_value = get_total_from_pool(pool)
                f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                f.write(f"----stock on hand's value is {total_value} \n")
                f.write(f"stock as following:" + str(pool) + '\n')
            elif t1_low >= Vday_1_actlow and (t2_2_high - t1_low) / t1_low < 0.005: # margin too low
                f.write('Good Forecast on T1low but low margin. try any sell? \n')
            elif t1_low < Vday_1_actlow and (t2_2_high - t1_low) / t1_low >= 0.005:
                dif = round(Vday_1_actlow - t1_low, 2)
                f.write(f"Good Margin but T1low is not reachable by {dif}. \n")
            else:
                dif = round(Vday_1_actlow - t1_low, 2)
                f.write(f"No good margin and t1low is not reachable by {dif}.. \n")

        if len(pool) > 1:
            for trade in pool[1:]:
                f.write('working on ' + str(trade) + f"on day{Vday_2}" + "\n")

                if trade[1] <= t2_2_high <=Vday_2_acthigh and trade[2] <= 2: # best forecast
                    f.write(f'BEST TRADE on {Vday_2} sell ' + str(trade[0]) + f' of {ticker} at {t2_2_high} \n')
                    PROFIT_COLLECTED += (t2_2_high - trade[1]) * trade[0]
                    f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                    total_value = get_total_from_pool(pool)
                    f.write('pop trade... \n')
                    pool.pop(pool.index(trade))
                    f.write(f"----stock on hand's value is {total_value} \n")
                    f.write(f"stock as following:" + str(pool) + '\n')

                elif trade[1] > Vday_2_acthigh and trade[2] <= 2: # bad forecast
                    dif = round(t2_2_high - Vday_2_acthigh, 2)
                    f.write(f'BAD FORECAST on {Vday_2} with supposed selling at {t2_2_high} but failed by {dif} \n')
                    f.write(f"list the stock in pool...")
                    f.write(f"stock as following:" + str(pool) + '\n')
                    spirit_2l = spirit_2h= 0.995

                elif trade[1] * 1.003 <= Vday_2_acthigh and trade[2] >= 2:
                    f.write('clearing on ' + str(trade) + f"on day{Vday_1}" + "\n")
                    clearing_price = round(trade[1] * 1.003, 2)
                    f.write(f'cuttting price {clearing_price} \n')
                    f.write(f'on {Vday_2} cutting stock ' + str(trade[0]) + f' of {ticker} at ' + str(clearing_price)
                            + '\n')
                    PROFIT_COLLECTED += round((clearing_price * trade[0] - trade[1] * trade[0]), 2)
                    f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                    total_value = get_total_from_pool(pool)
                    f.write(f"----stock on hand's value is {total_value} \n")
                    f.write('pop trade... \n')
                    pool.pop(pool.index(trade))
                    f.write(f"stock as following:" + str(pool) + '\n')
                elif trade[1] * 1.003 > Vday_2_acthigh and trade[2] >= 2:
                    f.write('clearing on ' + str(trade) + f"on day{Vday_1}" + "\n")
                    trade[2] += 1
                    f.write(f"cant cut on {Vday_2} at with the actual high at {Vday_2_acthigh}, try any selling?\n")
                    f.write(f"list the stock in pool...")
                    f.write(f"stock as following:" + str(pool) + '\n')
                else:
                    f.write('what it the else I forget? \n')
                trade[2] += 1

        total_value = get_total_from_pool(pool)

        f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
        f.write(f"----stock on hand's value is {total_value} \n")

        f.write('========================================================= \n')

# ==================main===============================


EPOCHS_RATIO = 5

ticker = 'sh600587'
pool = [[1000, 0.0, 1], ] # last elemnt is the day from T0

PROFIT_COLLECTED = 0
LL = 9999.0  # last low
LH = 0.0  # last high
spirit_2l = 1
spirit_2h = 1
stock_list = []   # tested dataframe
date_now = time.strftime("%Y-%m-%d")

# test slice
last = 30
last *= -1


if os.path.isfile(f'csv-original\\sh999999_{date_now}.csv'):
    os.remove(f'csv-original\\sh999999_{date_now}.csv')
if os.path.isfile('csv-original\\valuation.csv'):
    os.remove('csv-original\\valuation.csv')

if os.path.isfile('csv-original\\' + ticker + '_' + time.strftime("%Y-%m-%d") + '.csv'):
    df = pd.read_csv('csv-original\\' + ticker + '_' + time.strftime("%Y-%m-%d") + '.csv')
else:
    remove_file.remove('csv-original\\', startwith=ticker)
    day_to_csv.day_to_csv(single_code=ticker[2:], market=ticker[:2])
    # put 300 index growing percent to the csv
    tool_get_per_of_300.join_300(ticker)
    df = pd.read_csv('csv-original\\' + ticker + '_' + time.strftime("%Y-%m-%d") + '.csv')

df2 = df[last:]
df1 = df[:last]
df1.to_csv(f'csv-original\\sh999999_{date_now}.csv', index=False)
df2.to_csv('csv-original\\valuation.csv', index=False)

while True:
    df1 = pd.read_csv(f'csv-original\\sh999999_{date_now}.csv')
    df2 = pd.read_csv('csv-original\\valuation.csv')

    value(df1, df2, ticker, pool)

    # move one row to history from evaluation data

    if len(df2) == 2:
        break
    df1 = df1.append(df2[0:1])
    df2 = df2[1:]
    df1.to_csv(f'csv-original\\sh999999_{date_now}.csv', index=False)
    df2.to_csv('csv-original\\valuation.csv', index=False)






