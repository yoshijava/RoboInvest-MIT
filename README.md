# RoboInvest
RoboInvest 是一個台灣股價評分系統框架，根據自定的技術指標，提供自定的評分標準下每日的回測報告。
RoboInvest 主要是以 twstock 改寫，增加了以下的功能

* Data source 由台灣證交所改為 Yahoo Finance, 以避免抓取資料時常被證交所 ban IP.
* 回測功能
  * 使用 StockCSVFetcher.py 抓取歷史股價, repository 中提供 2010 年至今的歷史(個)各股 .csv 檔
* 除了使用 csv 檔, 亦提供 pandas_reader mode, 可以抓取即時股價, 在盤中時做個股評分
* 技術分析目前實作 13 個, 範例都在 analytics.py 中, 所佔的分數比重目前全都設成一樣

# 評分輸出範例:
  * https://github.com/yoshijava/RoboInvest-MIT/blob/master/sample-20190930.cmd
  * 各列代表意義
    * 分數
    * 股票代號
    * 建議買入價格 (負數為作空)
    * 停損價格
    * Yahoo 連結方便看技術分析
    * Rx: 代表的是 match 的技術指標
    * M = [...] 代表的是 13 個技術指標的各項得分

目前的分數是平均分配, 並不反應市場真實的情況, 使用者必須根據自己對技術指標的理解來分配權重, 甚至自行實作更多的技術指標.

## How to Run
  RoboMain.py -h
  * -dt DATETIME, --datetime DATETIME          (Give a specific end date)
  * -u, --update                               (Update stock codes)
  * -d, --debug                                (Debug mode)
  * -s, --single                               (Get a single stock ID evaluation)
  * -pdr, --pandas_reader                      (Use pandas_datareader to get realtime data)
  
## Requirement
* pip3 install pandas-datareader
* python3

## License
RoboInvest is based on [twstock](https://github.com/mlouielu/twstock), and it follows the original license - MIT license.

## 歡迎有興趣的網友一同加入討論與實作
