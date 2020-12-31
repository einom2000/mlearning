import datetime
import math
import time
import winsound

import keyboard
import pandas as pd
import pyautogui


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

def get_previous_day(day0, pri=1):
    k = [-3, -1, -1, -1, -1, -1, -2]
    pri_day = datetime.datetime.strptime(day0, "%Y-%m-%d")
    for _ in range(pri):
        pri_day = pri_day+ datetime.timedelta(days=k[pri_day.weekday()])  # 0,1,2,3,4,5,6(sun)
    return pri_day.strftime("%Y-%m-%d")


def get_t_posi_1(today):
    k = [1, 1, 1, 1, 3, 2, 1]
    day_0 = datetime.datetime.strptime(today, "%Y-%m-%d")
    day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
    return day_1.strftime("%Y-%m-%d")

# collect coordinations
# while True:
#     positions = ['qtwt', 'ymdan', 'add', 'code', 'buy', 'sell', 'price', 'vol', 'confirm', 'cancel']
#     coordi = {}
#     for posi in positions:
#         print(f'key in {posi}...')
#         wait_key_in('space')
#         coordi[posi] = pyautogui.position()
#
#     print(coordi)


def move_click(x, y):
    time.sleep(0.3)
    pyautogui.moveTo(x, y)
    time.sleep(0.3)
    pyautogui.click()
    time.sleep(0.3)


def parse_csv():
    # when to start the key in, who knows!
    day_now = time.strftime("%Y-%m-%d")
    yesterday = get_previous_day(day_now, 1)
    tomorrow = get_t_posi_1(day_now)
    if datetime.datetime.now().time() > datetime.time(12):
        sell_list_day = day_now
        buy_list_day = tomorrow   #----- for test set to day_now ,it should be tomorrow
        print('running in afternoon')
    else:
        sell_list_day = yesterday
        buy_list_day = day_now
        print('running in morning')

    buy_list = []
    df = pd.read_csv(f'DDD_{buy_list_day}_t1_2_decision_buy.csv')
    stocks = list(dict.fromkeys(list(df['stock'])))
    for stock in stocks:
        buy_price = round(df[df['stock']==stock].min()['target_price'], 2)
        vol = math.trunc((20000 // buy_price) / 100) * 100
        if vol == 0:
            vol = 100
        buy_list.append([stock[2:], buy_price, vol])

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
print(buys, sells)

coordination = {'init': [[55, 539], [71, 561],],
                'add': [291, 73],
                'code': [1284, 659],
                'buy': [1291, 691],
                'sell': [1404, 685],
                'price': [1314, 792],
                'vol': [1309, 820],
                'confirm': [1292, 846],
                'cancel': [1396, 843]
                }

print('open the page..and press space then we go!')
wait_key_in('space')


for posi in coordination['init']:
    pyautogui.moveTo(posi[0], posi[1])
    pyautogui.click()
    time.sleep(1)

add_btn = coordination['add']
code_box = coordination['code']
buy_btn = coordination['buy']
sell_btn = coordination['sell']
price_box = coordination['price']
vol_box = coordination['vol']
confirm_btn = coordination['confirm']
cancel_btn = coordination['cancel']




for buy in buys:

    code, price, vol = buy
    move_click(add_btn[0], add_btn[1])
    move_click(code_box[0], code_box[1])
    pyautogui.write(code)
    pyautogui.press('enter')
    move_click(buy_btn[0], buy_btn[1])
    move_click(price_box[0], price_box[1])
    pyautogui.write(str(price))
    pyautogui.press('enter')
    move_click(vol_box[0], vol_box[1])
    pyautogui.write(str(vol))
    pyautogui.press('enter')
    move_click(confirm_btn[0], confirm_btn[1])

for sell in sells:
    code, price, vol = sell
    move_click(add_btn[0], add_btn[1])
    move_click(code_box[0], code_box[1])
    pyautogui.write(code)
    pyautogui.press('enter')
    move_click(sell_btn[0], sell_btn[1])
    move_click(price_box[0], price_box[1])
    pyautogui.write(str(price))
    pyautogui.press('enter')
    move_click(vol_box[0], vol_box[1])
    pyautogui.write(str(vol))
    pyautogui.press('enter')
    move_click(confirm_btn[0], confirm_btn[1])


beep(8)


