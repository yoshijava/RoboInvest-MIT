from pandas_datareader import data as web
import datetime as dt
from twstock import *

for sid in sorted(codes):
    if len(sid) != 4:
        continue
    if sid.isdigit() and codes[sid].market == '上市':
        print("Saving %s history..." % sid)
        start = dt.datetime(2010, 1, 1)
        end = dt.datetime.today()
        df = web.get_data_yahoo([sid + '.TW'], start, end)
        df.to_csv(r'StockHistory/%s.TW.csv' % sid)


