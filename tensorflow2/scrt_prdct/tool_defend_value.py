import os

import pandas as pd

import collects
import day_to_csv
import defends
import remove_file
import tool_day_off_filter
import tool_get_per_of_300


def predict(stock, module='defend', daily_forecast_dir=''):

    date_now = tool_day_off_filter.get_date_now()

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

    else:
        print('Unknown module...terminated!')


def value(df1, df2, ticker, pool, max_pool=2):

    global PROFIT_COLLECTED, LL, LH, spirit_2l, spirit_2h

    # attr_1 ( if the 2 adj is >>>, give a - 0.05% ...
    Vday_0_adjc = round(df1[-1:]['adjclose'].item(), 2)
    Vday_0_actlow = float(df1[-1:]['low'].item())
    Vday_n1_adj = float(df1[-2:-1]['adjclose'].item())
    Vday_n2_adj = float(df1[-3:-2]['adjclose'].item())



    spirit = 1  # spirit of trend

    if Vday_n2_adj > Vday_n1_adj > Vday_0_adjc:
        spirit = 0.997
    if Vday_n2_adj < Vday_n1_adj < Vday_0_adjc:
        spirit = 1.003

    print(Vday_n1_adj, Vday_n2_adj)

    def get_total_from_pool(pool):
        total = 0.0
        for i in pool:
            total += i[0] * i[1]
        return total

    Vday_0 = str(df1[-1:]['Unnamed: 0.1'].item())
    print(Vday_0)
    Vday_1 = tool_day_off_filter.get_first_working_day(Vday_0, delta=1)
    Vday_2 = tool_day_off_filter.get_first_working_day(Vday_0, delta=2)
    Vday_1_actlow = float(df2[0:1]['low'].item())
    Vday_1_acthigh = float(df2[0:1]['high'].item())
    Vday_2_acthigh = float(df2[1:2]['high'].item())
    Vday_2_actc = float(df2[1:2]['adjclose'].item())

    t1_low, rch_1, rch_2, epo_d = predict('sh999999')
    t2_high,rch2_1, rch2_2, epo_c = predict('sh999999', module='collect')
    t1_1_low = round(t1_low * 1.005, 2)
    t2_2_high = round(t2_high * 0.995, 2)


    if Vday_0_actlow > LL:
        spirit_2l *= 1
        if spirit_2l >= 1.005:
            spirit_2l = 1.005
    else:
        spirit_2l = 1
    if Vday_1_acthigh < LH:
        spirit_2h *= 1
    else:
        spirit_2h = 1

    t1_low = round(t1_low * spirit * spirit_2l, 2)
    LL = t1_low

    t2_2_high = round(t2_2_high * spirit_2h, 2)
    LH = t2_2_high

    with open(f'memo_{ticker}.txt', 'a') as f:
        f.write(str(pool) + '\n')
        f.write(f"Vday_0 = {Vday_0} \n")
        f.write(f"Vday_0's adjclose = {Vday_0_adjc} \n")
        f.write(f"T+1 {Vday_1} actual low at {Vday_1_actlow} \n")
        f.write(f"T+1 {Vday_1} forecast low at {t1_low} with {rch_1} possibility \n")
        f.write(f"T+2 {Vday_2} forecast high at {t2_2_high} with {rch2_2} \n")
        f.write(f"T+2 {Vday_2} actual high at {Vday_2_acthigh} \n")
        f.write(f"above with spirits of {spirit} & {spirit_2l}  & {spirit_2h}\n")
        f.write(f"T+2 {Vday_2} actual close at {Vday_2_actc} \n")

        if len(pool) < max_pool + 1:
            # stock buying strategy
            if t1_low >= Vday_1_actlow and (t2_2_high - t1_low) / t1_low >= 0.005:  # 0.5% margin
                f.write(f'on {Vday_1} buy ' + str(pool[0][0]) + f' at {t1_low} \n')  # pool[0][0] is the min_buy_vol
                pool.append([pool[0][0], t1_low, 1])
                f.write(str(pool) + '\n')
                total_value = get_total_from_pool(pool)
                f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                f.write(f"----stock on hand's value is {total_value} \n")
            else:
                f.write('BUYING NOTHING.... \n')

        if len(pool) > 1:
            for trade in pool[1:]:
                f.write('working on ' + str(trade) + "\n")
                if trade[1] < t2_2_high <= Vday_2_acthigh and trade[2] <= 2: # best forecast
                    f.write(f'on {Vday_2} sell ' + str(trade[0]) + f' of {ticker} at {t2_2_high} \n')
                    PROFIT_COLLECTED += (t2_2_high - trade[1]) * trade[0]
                    f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                    pool.pop(pool.index(trade))
                    f.write('pop trade... \n')
                    f.write(str(pool) + '\n')

                elif trade[1] * 1.003 <= Vday_1_acthigh and trade[2] > 2:
                    clearing_price = round(trade[1] * 1.003, 2)
                    f.write(f'cuttting price {clearing_price} \n')
                    f.write(f'on {Vday_0} cutting stock ' + str(trade[0]) + f' of {ticker} at ' + str(clearing_price)
                            + '\n')
                    PROFIT_COLLECTED += round((clearing_price * trade[0] - trade[1] * trade[0]), 2)
                    f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
                    pool.pop(pool.index(trade))
                    f.write('pop trade... \n')
                    f.write(str(pool) + '\n')
                else:
                    trade[2] += 1
                    f.write("cant sell on Vday2 bad forcast \n")
                    f.write(str(pool) + '\n')



        total_value = get_total_from_pool(pool)

        f.write(f"----profit in total is {PROFIT_COLLECTED} \n")
        f.write(f"----stock on hand's value is {total_value} \n")

        f.write('========================================================= \n')

# ==================main===============================


EPOCHS_RATIO = 10

ticker = 'sh600030'
pool = [[1000, 0.0, 1], ] # last elemnt is the day from T0

PROFIT_COLLECTED = 0
LL = 9999.0  # last low
LH = 0.0  # last high
spirit_2l = 1
spirit_2h = 1
stock_list = []   # tested dataframe

last = 30
last *= -1
date_now = tool_day_off_filter.get_date_now()
if os.path.isfile(f'csv-original\\sh999999_{date_now}.csv'):
    os.remove(f'csv-original\\sh999999_{date_now}.csv')
if os.path.isfile('csv-original\\valuation.csv'):
    os.remove('csv-original\\valuation.csv')

if os.path.isfile('csv-original\\' + ticker + '_' + date_now + '.csv'):
    df = pd.read_csv('csv-original\\' + ticker + '_' + date_now + '.csv')
else:
    remove_file.remove('csv-original\\', startwith=ticker)
    day_to_csv.day_to_csv(single_code=ticker[2:], market=ticker[:2])
    # put 300 index growing percent to the csv
    tool_get_per_of_300.join_300(ticker)
    df = pd.read_csv('csv-original\\' + ticker + '_' + date_now + '.csv')


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






