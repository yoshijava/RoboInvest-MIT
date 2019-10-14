# -*- coding: utf-8 -*-

from twstock import *
import twstock
import sys
import traceback
import threading
import argparse
import datetime

is_debug_mode = False
is_multithread_mode = False
is_pdr_mode = False

def analyze(sid, endTimeObj):
    try:
        target = Stock(sid, endTimeObj, is_pdr_mode=is_pdr_mode)
        if target.fetcher != None:
            winner = WinnerRule(target)
            ret = winner.all_winner_rules()
            if ret != None:
                s = ", ".join(ret[1])
                print(s + ", M = " + str(ret[2]))
                sys.stdout.flush()
    except IndexError as e:
        if is_debug_mode:
            print(sid, e)
            print(traceback.format_exc())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dt", "--datetime", help="Give a specific end date")
    parser.add_argument("-u", "--update", help="Update stock codes", action="store_true")
    parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
    parser.add_argument("-pdr", "--pandas_datareader", help="pandas_datareader mode", action="store_true")
    parser.add_argument("-s", "--single", help="Get a single stock ID evaluation")
    
    args = parser.parse_args()

    if args.debug:
        is_debug_mode = True
    if args.update:
        twstock.__update_codes()
        print("Update stock codes succeeded.")
        exit(0)
    if args.datetime:
        endTimeObj = datetime.datetime.strptime(args.datetime, '%Y%m%d')
    else:
        endTimeObj = None
    if args.pandas_datareader:
        is_pdr_mode = True
    if args.single:
        codes = {args.single : codes[args.single]}

    for sid in sorted(codes):
        sid = str(sid)
        if len(sid) != 4:
            continue

        if is_debug_mode:
            print("Processing sid =", sid)

        try:
            analyze(sid, endTimeObj)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            # Issue #1. Caused by Yahoo Finance
            # If exception is list out of index, it may be caused by Yahoo Finance.
            # E.g., The starting day of 1404.TW is July 04, and it's apparently wrong
            if is_debug_mode:
                print(sid, e)
                print(traceback.format_exc())


