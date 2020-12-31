import os

import pandas as pd

import hunts
import tool_day_off_filter

date_now = tool_day_off_filter.get_date_now()

stock_list = []
stock_list.extend(['sh600600', 'sh600846', 'sh600585', 'sh601229'])
stock_list.extend(['sh600529', 'sh600547', 'sh600587', 'sh600058', 'sh600448'])

pre_fix = ''
daily_forecast_dir = ''
LOOKUP_STEP = 8
INIT_EPOCHS = 500
SECOND_EPOCHS = 500

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
    future_price, buying_accuracy_rate = \
        hunts.go_hunt(stock, lookup_step=LOOKUP_STEP, flush_result=False, epochs=epochs, only_forecast=False)
    epochs += saved_epochs
    dt.append({'stock': stock, 'fc_date': date_now, 'future_days': LOOKUP_STEP,
               'future_price': future_price, 'buy_acc_rate': buying_accuracy_rate,
               'uptonow_epochs' : epochs})
dt = pd.DataFrame.from_dict(dt)
if isinstance(data, list):
    data = dt.copy()
else:
    frames = [data, dt]
    data = pd.concat(frames)
print(data)
data.to_csv(daily_forecast_filename, index=False)
