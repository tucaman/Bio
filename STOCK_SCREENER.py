# from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
# from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import requests
import datetime
import time
import os

yf.pdr_override()

stocklist_nasdaq = si.tickers_nasdaq()
stocklist_other = si.tickers_other()

'SLDB' in stocklist_nasdaq

si.get_stats('NERV')
si.get_holders('NERV')
si.get_stats_valuation('NERV')

help(si)

final = []
index = []
n = -1

# 1) Get list of all NASDAQ tickers (from NASDAQ FTP) -
# https://quant.stackexchange.com/questions/1640/where-to-download-list-of-all-common-stocks-traded-on-nyse-nasdaq-and-amex
# df_bio = NASDAQ_SECTOR_TICKERS(sector='Healthcare')
# save file
fd = 'C://Users//Lennart//PycharmProjects//Bio//'
df_bio = pd.read_csv(fd + 'NASDAQ_bio.csv').iloc[:, 1:]
print(df_bio.shape)
print(df_bio.tail().to_string())


df_bio[df_bio.company_name.str.startswith('Chemo')]

import clinical_trials

#ToDo: BUILD A SCRAPER: https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download
# Require Ticker & Company Name (for searching clinicaltrials.gov)
# Need to add CIK (for EDGAR requests) - 10K et alt.
# Need to figure out a relationship between Clinical Trial data and Release date...
# Need to figure out a relationship for importance of study read-out

#ToDo: Embed stocktwits # of followers, Twitter API - retrieve tweets from qualifying users

# 2) Loop over tickers & collect data (might take a while...)
# https://stackoverflow.com/questions/59080447/how-to-get-industry-data-from-yahoo-finance-using-python
yf.Ticker("NERV").info.get('sector')
print(yf.info['sector'])