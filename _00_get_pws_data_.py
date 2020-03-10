# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
Name:    ADD SCRIPT MAIN NAME
Purpose: ADD SCRIPT PURPSOSE

Created on: 2020-01-31

Parameters
----------
file_loc : str
    The file location of the spreadsheet
print_cols : bool, optional
    A flag used to print the columns to the console (default is False)

Returns
-------
list
    a list of strings representing the header columns
    
https://www.pythonforbeginners.com/scraping/scraping-wunderground
https://docs.google.com/document/d/1w8jbqfAk0tfZS5P7hYnar1JiitM0gQZB-clxDfG3aD0/edit

https://www.wunderground.com/dashboard/pws/ISTUTTGA863/graph/2020-01-7/2020-01-7/monthly

http://api.weather.com/v2/pws/observations/current?apiKey=6532d6454b8aa370768e63d6ba5a832e&stationId=StationID&format=json&units=m

http://api.weather.com/v2/pws/observations/current?apiKey=6532d6454b8aa370768e63d6ba5a832e&stationId=ISTUTTGA863&format=json&units=m

https://www.wunderground.com/dashboard/pws/ISTUTTGA863

https://darksky.net/dev/account
https://darksky.net/dev/docs#time-machine-request
https://github.com/Detrous/darksky
"""


__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# =============================================================

from pathlib import Path

from pprint import pprint
import arrow
import urllib.request

import pandas as pd
import json


import os
import timeit
import time


main_dir = Path(os.getcwd())
os.chdir(main_dir)

# my_headers = {'accept-encoding': 'gzip'}

# api_stn = (r'http://api.weather.com/v2/pws/observations/'
#            'current?apiKey=6532d6454b8aa370768e63d6ba5a832e&'
#            'stationId=IFREUD4&format=json&units=m')  # 6532d6454b8aa370768e63d6ba5a832e

# 0c4b2b3b0875f8fecfdc155a69536a78
# #filderstadt = r'https://www.wunderground.com/history/daily/de/filderstadt/EDDS/date/2015-1-1'
# test_url = (r'https://api.darksky.net/forecast/'
#             '0c4b2b3b0875f8fecfdc155a69536a78/48.738551,9.100067')
#
# test_url = (r'https://api.darksky.net/forecast/'
#             '0c4b2b3b0875f8fecfdc155a69536a78/48.738551,9.100067'
#             '255657600?exclude=currently,flagsunits=')
#
# #[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
# # 'http://api.wunderground.com/api/0c4b2b3b0875f8fecfdc155a69536a78/forecast/q/France/Paris.json'
#
# # dark sky
# response = urllib.request.urlopen(test_url, headers=my_headers)  # api_stn
# data = json.loads(response.read())
# print(data)

# weather underground
# response = urllib.request.urlopen(api_stn)  # api_stn
# data = json.loads(response.read())
# pprint(data)
# # setup


station_ID = 'ISTUTTGA863'
api_key = '6532d6454b8aa370768e63d6ba5a832e'
# 6cd1ae3a7922473091ae3a7922e7303e
start_date = '20190101'
end_date = '20191230'

time_range = pd.date_range(start=start_date, end=end_date, freq='1440min')

for x in time_range:

    WU_date = str(x).split()[0].replace('-', '')

    url = ('http://api.weather.com/v2/pws/history/all?stationId=' + station_ID +
           '&format=json&units=m&date=' + WU_date + '&apiKey=' + api_key)
    try:
        df = pd.read_json(url)
        tf = pd.read_json((df['observations']).to_json(), orient='index')
        tf2 = pd.read_json((tf['metric']).to_json(),  orient='index')
        tf3 = tf.join(tf2)

        tf_out = tf3[['obsTimeLocal', 'tempHigh', 'dewptHigh',
                      'winddirAvg', 'windspeedAvg', 'windgustHigh', 'pressureMax',
                      'humidityAvg', 'precipRate', 'precipTotal',
                      'uvHigh', 'solarRadiationHigh']]

        tf_sum = {'Record': ['obsTimeLocal', 'tempHigh', 'tempLow',
                             'dewptHigh', 'dewptLow', 'winddirAvg', 'windspeedAvg', 'windgustHigh',
                             'pressureMax', 'pressureMin', 'humidityAvg',
                             'precipRate', 'precipTotal', 'uvHigh', 'solarRadiationHigh'],
                  'Observation': [tf3['obsTimeLocal'].values,
                                  tf3['tempHigh'].values, tf3['tempLow'].values,
                                  tf3['dewptHigh'].values,
                                  tf3['dewptLow'].values, tf3['winddirAvg'].values,
                                  tf3['windspeedAvg'].mean(
                  ), tf3['windgustHigh'].max(),
            tf3['pressureMax'].values, tf3['pressureMin'].values,
            tf3['humidityAvg'].values, tf3['precipRate'].values,
            tf3['precipTotal'].values, tf3['uvHigh'].values,
            tf3['solarRadiationHigh'].values]
        }

        tf_sum_base = pd.DataFrame(tf_sum, columns=['Record', 'Observation'])

        tf_sum_out = tf_sum_base.transpose()

        print(WU_date)

        out_path = r'X:\exchange\ElHachem\wunderground\data\%s_%s.xlsx' % (
            station_ID, WU_date)
        with pd.ExcelWriter(out_path) as writer:
            tf_out.to_excel(writer, sheet_name=WU_date)
            tf_sum_out.to_excel(writer, sheet_name='Summary')

    except Exception:
        print('ERE')
        tf_out = pd.DataFrame()
        tf_sum_out = pd.DataFrame()
        with pd.ExcelWriter(out_path) as writer:
            tf_out.to_excel(writer, sheet_name=WU_date)
            tf_sum_out.to_excel(writer, sheet_name='Summary')


if __name__ == '__main__':

    print('**** Started on %s ****\n' % time.asctime())
    START = timeit.default_timer()  # to get the runtime of the program

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
