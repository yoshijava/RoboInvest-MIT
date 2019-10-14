# -*- coding: utf-8 -*-
import pandas_datareader as pdr
import pandas
import json
import calendar
import sys
import datetime
import os
import urllib.parse
from twstock import analytics
from collections import namedtuple
from twstock import codes
from json.decoder import JSONDecodeError
import requests

DATATUPLE = namedtuple('Data', ['date', 'open', 'high', 'low',
                                'close', 'volume'])

class BaseFetcher(object):
    def fetch(self, year, month, sid):
        pass

    def _make_datatuple(self, data):
        pass

    def purify(self, original_data):
        pass


class TWSEFetcher(BaseFetcher):
    is_pdr_mode = False

    def __init__(self):
        pass

    def fetch(self, year: int, month: int, sid: str, today):
        sid = sid + ".TW"
        data = None

        while today.weekday() >= 5:
            today = today - datetime.timedelta(days=1)

        cwd = os.getcwd()
        dateparse = lambda dates: [pandas.datetime.strptime(d, '%Y-%m-%d') for d in dates]
        if self.is_pdr_mode:
            endTimeObj = today - datetime.timedelta(days=120)
            df = pdr.get_data_yahoo(sid, endTimeObj, today)
        else:
            df = pandas.read_csv(cwd + "/StockHistory/%s.csv" % sid, parse_dates=['Date'], date_parser=dateparse, index_col=0,
                                    skiprows=3, names=["Date", "High", "Low", "Open", "Close", "Volume", "Adj Close"])
            endTimeObj = today - datetime.timedelta(days=120)
            df = df[endTimeObj:today]
        # print(df)

        jsonfile = df.transpose().to_json()
        result = json.loads(jsonfile)
        # print(result)

        final_ret = []
        for originalTS in result:
            ts = int(originalTS) / 1000
            entry = result[str(originalTS)]
            stock_result = []
            stock_result.append(ts)
            stock_result.append(float(entry["Open"]))
            stock_result.append(float(entry["High"]))
            stock_result.append(float(entry["Low"]))
            stock_result.append(float(entry["Close"]))
            stock_result.append(int(entry["Volume"]))
            final_ret.append(stock_result)

        data = sorted(final_ret, key=lambda y: y[0])
        # print(data)
        
        if data == None:
            data = {}
        else:
            ret = self.purify(data)
            data = ret

        return data

    def _make_datatuple(self, data):
        '''
        DATATUPLE = namedtuple('Data', ['date', 'open', 'high', 'low',
                                'close', 'vol'])
        '''

        data[0] = datetime.datetime.fromtimestamp(data[0])
        data[1] = int(data[1]) # open
        data[2] = float(data[2]) # high
        data[3] = float(data[3]) # low
        data[4] = float(data[4]) # close
        data[5] = int(data[5]) # vol
        return DATATUPLE(*data)

    def purify(self, original_data):
        # print(original_data)
        return [self._make_datatuple(d) for d in original_data if d[5] != 0]


class Stock(analytics.Analytics):
    today = None
    fetcher = None

    def __init__(self, sid: str, endTimeObj = None, initial_fetch: bool=True, is_pdr_mode = False):
        self.sid = sid
        self.fetcher = TWSEFetcher() if codes.codes[sid].market == '上市' else None
        if self.fetcher != None:
            self.data = []
            self.fetcher.is_pdr_mode = is_pdr_mode

            if endTimeObj != None:
                self.today = endTimeObj
            else:
                self.today = datetime.datetime.today()

            # Init data
            if initial_fetch:
                self.fetch_90()

    def fetch_from(self, year: int, month: int):
        """Fetch data from year, month to current year month data"""
        self.data = self.fetcher.fetch(year, month, self.sid, self.today)
        return self.data

    def fetch_90(self):
        """Fetch 90 days data"""
        before = self.today - datetime.timedelta(days=120)
        self.fetch_from(before.year, before.month)
        self.data = self.data[-90:]
        return self.data

    @property
    def date(self):
        return [d.date for d in self.data]

    @property
    def volume(self):
        return [d.volume for d in self.data]

    @property
    def high(self):
        return [d.high for d in self.data]

    @property
    def low(self):
        return [d.low for d in self.data]

    @property
    def open(self):
        return [d.open for d in self.data]

    @property
    def close(self):
        return [d.close for d in self.data]

