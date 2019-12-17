from pandas_datareader import data as web
import datetime as dt
from twstock import *
import sys
import pandas as pd
import os
import argparse
import time

def do_fetch_rest(sid):
    print("Saving %s history..." % sid, end='')
    if os.path.isfile(r'StockHistory/%s.TW.csv' % sid):
        with open(r'StockHistory/%s.TW.csv' % sid,"r") as f:
            lines = list(f)
            csv_format = lines[0].replace("\n","")
            csv_date = lines[-1].split(',')[0]
    else:
        start = dt.datetime(2008, 1, 1) # max history data in Yahoo Finance
        end = dt.datetime.today()
        do_fetch(sid, start, end)
        return

    start = dt.datetime.strptime(csv_date, "%Y-%m-%d")
    start = start + dt.timedelta(days=1)
    end =  dt.datetime.today()

    print("start:",dt.datetime.strftime(start, "%Y-%m-%d"),"end",dt.datetime.strftime(end, "%Y-%m-%d"))
    if start.date() > end.date():
        #print("start > end")
        return

    success = False
    timeout = 0
    while success == False:
        try:
            if codes[sid].market == '上市':
                df = web.get_data_yahoo([str(sid) + '.TW'], start, end)
            if codes[sid].market == '上櫃':
                df = web.get_data_yahoo([str(sid) + '.TWO'], start, end)
            success = True
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            timeout = timeout + 1
            if timeout < 3:
                print("{} fetch error".format(sid))
                time.sleep(1)
                pass
            else:
                return

    df.reset_index(inplace=True)
    fetch_end = df.iat[-1,0]
    print(fetch_end.date(), start.date())
    if fetch_end.date() < start.date():
        return

    print(df)
    f = open(r'StockHistory/%s.TW.csv' % sid,"a+")
    for index, row in df.iterrows():
        s=""
        for name in csv_format.split(','):
            if name == "Attributes":
                s = s + dt.datetime.strftime(row["Date"].tolist()[0], "%Y-%m-%d") + ','
            else:
                s = s + str(row[name].tolist()[0]) + ','
        s = s[0:-2] + "\n"
        f.write(s)
    f.close()


def fetch_rest():
    for sid in sorted(codes):
        if len(sid) != 4:
            continue
        if sid.isdigit() and (codes[sid].market == '上市' or codes[sid].market == '上櫃'):
            do_fetch_rest(sid)


def fetch_all():
    start = dt.datetime(2008, 1, 1) # max history data in Yahoo Finance
    end = dt.datetime.today()
    for sid in sorted(codes):
        if len(sid) != 4:
            continue
        if sid.isdigit() and codes[sid].market == '上市':
            do_fetch(sid, start, end, "TW")

    for sid in sorted(codes):
        if len(sid) != 4:
            continue
        if sid.isdigit() and codes[sid].market == '上櫃':
            do_fetch(sid, start, end, "TWO")


def do_fetch(sid, start, end):
    print("Saving %s history..." % sid)
    success = False
    while success == False:
        try:
            if codes[sid].market == '上市':
                df = web.get_data_yahoo([str(sid) + '.TW'], start, end)
            if codes[sid].market == '上櫃':
                df = web.get_data_yahoo([str(sid) + '.TWO'], start, end)
            success = True
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass

    #print(df)
    df.to_csv(r'StockHistory/%s.TW.csv' % sid)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--single", help="Given a specific sid")
    parser.add_argument("-p", "--partial", help="Fetch partial log")
    parser.add_argument("-a", "--all", help="Fetch all log")
    args = parser.parse_args()

    if args.single:
        do_fetch_rest(args.single)
        sys.exit(0)


    fetch_rest()
