import os
import time

import pandas as pd

import defends

date_now = time.strftime("%Y-%m-%d")

stock_list = []
stock_list.extend(['sh600600'])

pre_fix = 'defend_'
daily_forecast_dir = ''
LOOKUP_STEP = 1
INIT_EPOCHS = 100
SECOND_EPOCHS = 30

daily_forecast_filename = os.path.join(daily_forecast_dir, f"{pre_fix}{date_now}_{LOOKUP_STEP}_forecast.csv")

if os.path.isfile(daily_forecast_filename):
    try:
        data = pd.read_csv(daily_forecast_filename)
    except:
        data = []
else:
    data = []

print(data)
dt = []
for stock in stock_list:
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
    future_price, reachability = \
        defends.go_defend(stock, lookup_step=LOOKUP_STEP, flush_result=False, epochs=epochs, only_forecast=False)
    epochs += saved_epochs
    dt.append({'stock': stock, 'fc_date': date_now, 'future_days': LOOKUP_STEP,
               'future_lowest': future_price, 'reachability': reachability,
               'uptonow_epochs' : epochs})
dt = pd.DataFrame.from_dict(dt)
if isinstance(data, list):
    data = dt.copy()
else:
    frames = [data, dt]
    data = pd.concat(frames)
print(data)
data.to_csv(daily_forecast_filename, index=False)
