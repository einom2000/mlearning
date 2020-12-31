import os

import pandas as pd

import collects
import defends
import tool_day_off_filter
import tool_defend_patch


def predict(stock, module='defend', daily_forecast_dir=''):

    date_now = tool_day_off_filter.get_date_now()

    if module == 'defend':
        pre_fix = 'defend_'
        LOOKUP_STEP = 1
        INIT_EPOCHS = 2 * EPOCH_RATIO
        SECOND_EPOCHS = 2 * EPOCH_RATIO

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
        # data.to_csv(daily_forecast_filename, index=False)
        return float(future_price), reachability, reachability_2, epochs

    elif module == 'collect':
        pre_fix = 'collect'
        LOOKUP_STEP = 2
        INIT_EPOCHS = 3 * EPOCH_RATIO
        SECOND_EPOCHS = 3 * EPOCH_RATIO
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

        return float(future_price), reachability, reachability_2, epochs

    else:
        print('Unknown module...terminated!')


#==================main===============================conda

# patch the decision_file

tool_defend_patch.clear_old_catch()
tool_defend_patch.patch()

# 601211, 601319, 601328, 601390, 601727
stock_list = ['sh600685']
# stock_list.extend(['sh600030','sh600600', 'sh600648', 'sh600585', 'sh600529'])
# stock_list.extend(['sh600587', 'sh600058','sh600547'])


date_now = tool_day_off_filter.get_date_now()

EPOCH_RATIO = 100

for ticker in stock_list:
    t1_low, rch_1, rch_2, epo_d = predict(ticker)
    t2_high,rch2_1, rch2_2, epo_c = predict(ticker, module='collect')
    columes = ['stock', 'fc_date', 't+1_low', 'reachability', 't+1_low+0.5%', 'reachability2', 'df_epochs', 't+2_high',
               't+2_high', 'reality', 't+2_high*99.5%', 'reality_2', 'ht_epochs']
    if not os.path.isfile(f'TTT_{date_now}_t1_2_forecast.csv'):
        df = pd.DataFrame(columns=columes)
        df.to_csv(f'TTT_{date_now}_t1_2_forecast.csv', index=False)

    df = pd.read_csv(f'TTT_{date_now}_t1_2_forecast.csv')

    row = {'stock': ticker,
            'fc_date': date_now,
            't+1_low': round(round(t1_low, 2), 2),
            'reachability': rch_1,
            't+1_low+0.5%': round(t1_low * 1.005, 2),
            'reachability2': rch_2,
            'df_epochs': epo_d,
            't+2_high': round(t2_high, 2),
            'reality': rch2_1,
            't+2_high*99.5%' : round(t2_high * 0.995, 2),
            'reality_2': rch2_2,
            'ht_epochs': epo_c}

    df = df.append(row, ignore_index=True)

    df.to_csv(f'TTT_{date_now}_t1_2_forecast.csv', index=False)

# --------------------------------------------------------------

    t2_2_high = t2_high * .995
    day_1 = tool_day_off_filter.get_first_working_day(date_now, delta=1)
    day_2 = tool_day_off_filter.get_first_working_day(date_now, delta=2)
    columes_buy = ['stock', 'act_day', 'act', 'target_price', 'sell_day', 'T2-sell', 'gain_percent',
                   'act_low', 'act_high', 'buy', 'at_price', 'EPOCH_R']
    if not os.path.isfile(f'DDD_{day_1}_t1_2_decision_buy.csv'):
        df1 = pd.DataFrame(columns=columes_buy)
        df1.to_csv(f'DDD_{day_1}_t1_2_decision_buy.csv', index=False)

    df1 = pd.read_csv(f'DDD_{day_1}_t1_2_decision_buy.csv')

    if (t2_2_high - t1_low) / t1_low >= 0.005:
        row1 = {'stock': ticker,
                'act_day': day_1,
                'act': 'buy',
                'target_price': t1_low,
                'sell_day': day_2,
                'T2-sell': t2_2_high,
                'gain_percent': round((t2_2_high - t1_low) / t1_low, 2),
                'act_low': 0,
                'act_high': 0,
                'buy': 0,
                'at_price': 0,
                'sell':0,
                'selling_price':0,
                'EPOCH_R': EPOCH_RATIO}
        df1 = df1.append(row1, ignore_index=True)
        df1.to_csv(f'DDD_{day_1}_t1_2_decision_buy.csv', index=False)

# calculate the stock pool list
tool_defend_patch.pool_list()








