import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

plt.rcParams['font.sans-serif']=['STSong']
today = datetime.strftime(datetime.today(), "%Y_%m_%d")


TOKEN = 'aeed5fcab3f3163d70faca84342abf2d283d5adeabcaabfaa0e08530'
ts.set_token(TOKEN)
pro = ts.pro_api()

'''     主板     2025
        中小板     988
        创业板     883
        科创板     206
        CDR       1
'''


def load_data(data_file_name, data_file_source, forced=False):
    if not forced:
        try:
            data = pd.read_csv(data_file_name)
            print('Get data from local!')
            return data
        except FileNotFoundError:
            data = pro.query(data_file_source[0], **data_file_source[1])
            data.to_csv(data_file_name, index=True)
            print('Fetching ' + data_file_source[0] + ' got done!')
            return data
    else:
        try:
            os.remove(data_file_name)
        except FileNotFoundError:
            pass
        data = pro.query(data_file_source[0], **data_file_source[1])
        data.to_csv(data_file_name, index=True)
        print('Updating ' + data_file_source[0] + ' got done!')
        return data


print(load_data('scrt_name_list.csv', ['stock_basic',
                                       {'exchange': '', 'list_status': 'L',
                                        'fields': 'ts_code,symbol,name,area,industry,market,list_date'}],
                forced=False))

# ## get industries' type statistics and save it to the industries.csv file
# nm_data = pd.read_csv('scrt_name_list.csv')
# in_df = nm_data['industry'].value_counts().rename_axis('industry').reset_index(name='num_of_listed')
# try:
#     os.remove('industries.csv')
# except FileNotFoundError:
#     pass
# in_df.to_csv('industries.csv', index=True)
# print(pd.read_csv('industries.csv'))


print(load_data('trade_dates.csv', ['trade_cal',
                                    {'exchange':'', 'start_date':'20000101', 'end_date': today.replace('_', '')}],
                forced=False))

print(load_data('index_basic.csv', ['index_basic', {}], forced=False))

# test on 000016.SH             上证50    SSE      中证公司     规模指数  20031231.0     1000.00  20040102.0

sample_index = '000016.SH'
sample_index_std = '20120102'
sample_index_edd = today.replace('_', '')
print(load_data('000016.SH.csv', ['index_daily',
                                  {'ts_code': sample_index, 'start_date':sample_index_std,
                                   'end_date': sample_index_edd}],
                forced=False))
