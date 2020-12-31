import datetime
import os
import time

import pandas as pd


def get_first_working_day(datestr, delta=0, add_holiday_list=[]):

    def get_t_posi_1(today):
        k = [1, 1, 1, 1, 3, 2, 1]
        day_0 = datetime.datetime.strptime(today, "%Y-%m-%d")
        day_1 = day_0 + datetime.timedelta(days=k[day_0.weekday()])  # 0,1,2,3,4,5,6(sun)
        return day_1.strftime("%Y-%m-%d")

    def get_previous_day(day0):
        k = [-3, -1, -1, -1, -1, -1, -2]
        pri_day = datetime.datetime.strptime(day0, "%Y-%m-%d")
        pri_day = pri_day + datetime.timedelta(days=k[pri_day.weekday()])  # 0,1,2,3,4,5,6(sun)
        return pri_day.strftime("%Y-%m-%d")

    if not os.path.isfile('DDD_2021-holidays.csv'):
        holiday_2021 =[['2021-01-01'], ['2021-10-01']]
        df = pd.DataFrame(holiday_2021, columns=['date'])
        print(df)
        df.to_csv('DDD_2021-holidays.csv', index=False)

    df = pd.read_csv('DDD_2021-holidays.csv')
    holiday_2021 = list(df['date'])

    if len(add_holiday_list) > 0:
        for holiday in add_holiday_list:
            holiday_2021.append(holiday)
    holiday_2021 = list(dict.fromkeys(holiday_2021))
    df = pd.DataFrame(holiday_2021, columns=['date'])
    df.to_csv('DDD_2021-holidays.csv', index=False)

    if delta >= 1:
        first_working_date = datestr
        for i in range(0, delta):
            first_working_date = get_t_posi_1(first_working_date)
            while first_working_date in holiday_2021:
                first_working_date = get_t_posi_1(first_working_date)
        return first_working_date

    if delta == 0:
        while datestr in holiday_2021:
            datestr = get_previous_day(datestr)
        return datestr

    if delta < 0:
        last_working_date = datestr
        for i in range (0, abs(delta)):
            last_working_date = get_previous_day(last_working_date)
            while True:
                if last_working_date not in holiday_2021:
                    break
                last_working_date = get_previous_day(last_working_date)
        return last_working_date


def get_date_now():
    if datetime.datetime.now().time() <= datetime.time(15):
        return get_first_working_day(time.strftime("%Y-%m-%d"), delta=-1)
    else:
        return get_first_working_day(time.strftime("%Y-%m-%d"), delta=0)


# today = '2021-1-4'
#
# print(get_first_working_day(today, delta=-1))
#
# today = '2021-01-04'
#
# print(get_first_working_day(today, delta=-2))

# today ='2021-02-13'
# print(get_first_working_day(today, delta=0))