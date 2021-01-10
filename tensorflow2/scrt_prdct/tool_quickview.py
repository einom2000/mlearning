import datetime
import math
import time
import winsound

import keyboard
import pandas as pd
import pyautogui

import tool_day_off_filter


def beep(times=1):
    for _ in range(0, times):
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 100  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)


def wait_key_in(string):
    while True:
        if keyboard.is_pressed(string):
            beep(2)
            return


def move_click(x, y):
    time.sleep(0.3)
    pyautogui.moveTo(x, y)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(0.3)


def parse_csv():
    # when to start the key in, who knows!
    day_now = time.strftime("%Y-%m-%d")
    yesterday = tool_day_off_filter.get_first_working_day(day_now, delta=-1)
    tomorrow = tool_day_off_filter.get_first_working_day(day_now, delta=1)
    print(yesterday, tomorrow)
    if datetime.datetime.now().time() > datetime.time(12):
        sell_list_day = day_now   # should be day_now
        buy_list_day = tomorrow   # ----- for test set to day_now ,it should be tomorrow
        print('running in afternoon')
    else:
        sell_list_day = yesterday
        buy_list_day = tomorrow  # should be day_now
        print('running in morning')

    buy_list = []
    df = pd.read_csv(f'DDD_{buy_list_day}_t1_2_decision_buy.csv')
    stocks = list(dict.fromkeys(list(df['stock'])))
    for stock in stocks:
        buy_price = round(df[df['stock']==stock].min()['target_price'], 2)
        t2_price = round(df[df['stock']==stock].min()['T2-sell'], 2)
        target_gain = round(df[df['stock']==stock].min()['gain_percent'], 2)

        vol = math.trunc((20000 // buy_price) / 100) * 100
        if vol == 0:
            vol = 100
        buy_list.append([stock[2:], buy_price, vol, t2_price, target_gain])

    sell_list = []
    df = pd.read_csv(f'DDD_{sell_list_day}_t1_2_decision_buy.csv')
    df2 = df[(df['buy']!=0)  & (df['buy']!=9999)]
    if not df2.empty:
        for index, que in df2.iterrows():
            if que['gain_percent'] > 0.01:
                stock = que['stock']
                sell_price = que['T2-sell']
                vol = que['buy']
                sell_list.append([stock[2:], sell_price, vol])
    return buy_list, sell_list


buys, sells = parse_csv()
print('buys:')
print(buys)
print('sells:')
print(sells)
