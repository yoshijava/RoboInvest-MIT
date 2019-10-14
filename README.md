# RoboInvest
RoboInvest 是一個台灣股價評分系統框架，根據自定的技術指標，提供自定的評分標準下每日的回測報告。
RoboInvest 主要是以 twstock 改寫，增加了以下的功能

* Data source 由台灣證交所改為 Yahoo Finance, 以避免抓取資料時常被證交所 ban IP.
* 回測功能
  * 使用 StockCSVFetcher.py 抓取歷史股價, repository 中提供 2010 年至今的歷史各股 .csv 檔
* 除了使用 csv 檔, 亦提供 pandas_reader mode, 可以抓取即時股價, 在盤中時做個股評分
* 技術分析目前實作 13 個, 範例都在 analytics.py 中, 所佔的分數比重目前全都設成一樣



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

