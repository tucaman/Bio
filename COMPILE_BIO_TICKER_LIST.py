from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import time


# ----------------------------------------------------------------------------------------------------------------------
# Request ticker lists from NASDAQ

def NASDAQ_SECTOR_TICKERS(sector='Healthcare'):

    dict_sector = {'Financial': '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[3]/div[2]/ul/li[1]/button',
                   'Healthcare': '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[3]/div[2]/ul/li[2]/button',
                   'Conglomerates': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[3]/button',
                   'Consumer Goods': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[4]/button',
                   'Services': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[5]/button',
                   'Utilities': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[6]/button',
                   'Basic Materials': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[7]/button',
                   'Technology': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[8]/button',
                   'Industrial Goods': '/html/body/div[2]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[9]/button'}

    # initiate Chrome instance
    driver = webdriver.Chrome()

    # open webpage
    driver.get("https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download")
    time.sleep(5)
    print('Webpage loaded.')

    # accept cookies
    elem = driver.find_element_by_xpath('/html/body/div[8]/button[1]')
    elem.click()
    time.sleep(5)
    print('Cookie policy accepted.')

    # select only stocks for sector
    elem = driver.find_element_by_xpath(dict_sector.get(sector))
    elem.click()
    time.sleep(5)
    print('Sector selected.')

    # confirm selection
    # /html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[4]/button
    elem = driver.find_element_by_xpath('/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[3]/div[4]/button')
    elem.click()
    time.sleep(15)
    print('Selection confirmed.')

    def parse_table(table):
        l_ticker = []
        l_company_name = []
        for r in table:
            # use regular expressions to extract stock symbols
            p = re.compile(r'<.*?>')  # strip all html components

            # TICKER
            c = r.contents[0]
            l_ticker += [p.sub('', str(c))]
            # COMPANY NAME
            c = r.contents[1]
            l_company_name += [p.sub('', str(c))]

        df = pd.DataFrame(zip(l_ticker, l_company_name),
                          columns=['ticker', 'company_name'])

        return df

    # loop over the subtable
    l_df = []

    # evaluate the number of pages to parse
    # last_page = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[10]/a'
    last_page = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/ul/li[10]/a'
    #
    elem = driver.find_element_by_xpath(last_page)
    last_page = elem.get_attribute('innerHTML')
    print('last_page:', last_page)
    # We apply the following strategy for extracting all subtables:
    # 1) We call the first six subpages 2-7 directly.
    # 2) We then call only subpage 8 until we reach page last_page - 1
    # 3) We then call the final page
    time.sleep(3)
    # Step 1
    for i in range(2,8):
        print('Run step 1 - page:', i-1)
        # x_path = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[' + str(i) + ']/a'
        x_path = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/ul/li[' + str(i) + ']/a'
        # x_path == '/html/body/div[4]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[2]/a'
        # x_path = '/html/body/div[4]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[2]/a'
        elem = driver.find_element_by_xpath(x_path)

        try:
            elem.click()
        except ElementClickInterceptedException:
            print('Click intercepted for ', elem.get_attribute('innerHTML'))
            time.sleep(3)
            elem = driver.find_element_by_xpath(x_path)
            elem.click()

        time.sleep(3) #wait until the table has been fully loaded

        # get the the results table
        x_path_table = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/div/table'
        elem = driver.find_element_by_xpath(x_path_table)
        html_string = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        table = soup.find_all('tbody')[0]  # Grab the first table

        l_df += [parse_table(table)]

    # Step 2
    num_page = 0
    while int(num_page) < int(last_page) - 1:

        # x_path = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[8]/a'
        x_path = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/ul/li[8]/a'
        elem = driver.find_element_by_xpath(x_path)
        try:
            elem.click()
        except ElementClickInterceptedException:
            print('num_page', str(num_page))
            print('Click intercepted for ', elem.get_attribute('innerHTML'))
            time.sleep(3)
            elem = driver.find_element_by_xpath(x_path)
            elem.click()

        num_page = elem.get_attribute('innerHTML')
        print('num_page', num_page)
        time.sleep(3) #wait until the table has been fully loaded

        # get the the results table
        # x_path_table = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/div/table'
        x_path_table = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/div/table'
        elem = driver.find_element_by_xpath(x_path_table)
        html_string = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        table = soup.find_all('tbody')[0]  # Grab the first table

        l_df += [parse_table(table)]

    # Step 3
    i = 1
    while num_page < last_page:
        print(i)
        x_path = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/ul/li[' + str(8 + i) + ']/a'

        elem = driver.find_element_by_xpath(x_path)
        try:
            elem.click()
        except ElementClickInterceptedException:
            print('Click intercepted for ', elem.get_attribute('innerHTML'))
            time.sleep(3)
            elem = driver.find_element_by_xpath(x_path)
            elem.click()
        time.sleep(3) #wait until the table has been fully loaded
        num_page = elem.get_attribute('innerHTML')
        print('num_page', num_page)

        # get the the results table
        # x_path_table = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/div/table'
        x_path_table = '/html/body/div[2]/div/main/div[2]/div[3]/div/section/div[1]/div[4]/div/table'
        elem = driver.find_element_by_xpath(x_path_table)
        html_string = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        table = soup.find_all('tbody')[0]  # Grab the first table

        l_df += [parse_table(table)]

    # append all result tables
    df_final = pd.DataFrame()
    for df in l_df:
        df_final = df_final.append(df)
    # add NASDAQ sector
    df_final['NASDAQ_sector'] = sector
    print(df_final.head())
    print(df_final.tail())

    # close the driver
    driver.close()

    return df_final

df_bio = NASDAQ_SECTOR_TICKERS(sector='Healthcare')
# save file
fd = 'C://Users//lenna//PycharmProjects//Bio//'
df_bio.to_csv(fd + 'NASDAQ_bio.csv')
print(df_bio.shape)
print(df_bio.tail().to_string())
    # assert "Python" in driver.title

df_finance = NASDAQ_SECTOR_TICKERS(sector='Financial')
fd = 'C://Users//Lennart//PycharmProjects//Bio//'
df_finance.to_csv(fd + 'NASDAQ_finance.csv')
print(df_finance.shape)
print(df_finance.tail().to_string())

# ----------------------------------------------------------------------------------------------------------------------
# Enrich ticker lists with CUSIPS (using list of 13F securities)
# ----------------------------------------------------------------------------------------------------------------------
# import the list of 13F securities
import requests
import re
import pdfplumber

def download_list_of_section_13_f_securities(year=2020, quarter=1):
    '''
    :param year: year of list of 13F securities
    :param quarter: quarter of list of 13F securities
    :return: download path
    '''

    # compile download link
    url = 'https://www.sec.gov/divisions/investment/13f/13flist' + str(year) +'q' + str(quarter) + '.pdf'
    r = requests.get(url)

    # define save path
    _fd = os.getcwd() + "//List_of_13f_securities//"
    if not os.path.exists(_fd):
        os.makedirs(_fd, exist_ok=True)
    _f = str(year) + 'q' + str(quarter) + '.pdf'

    with open(_fd+_f, 'wb') as f:
        f.write(r.content)

    return _fd + _f

_file = download_list_of_section_13_f_securities(year=2020, quarter=1)

def extract_list_of_13f_securities(_file):
    df = pd.DataFrame()
    with pdfplumber.open(_file) as pdf:
        for i in range(2, len(pdf.pages)):

            p = pdf.pages[i]

            # extract column for cusip
            cropped_cusip_no = p.within_bbox((0, 115, 160, p.height))
            l_cusip = cropped_cusip_no.extract_text().split('\n')

            # extract column for issuer
            cropped_issuer = p.within_bbox((160, 115, 350, p.height))
            l_issuer = cropped_issuer.extract_text().split('\n')

            # extract column for description and status
            cropped_desc_status = p.within_bbox((350, 115, p.width, p.height))
            l_desc_status = cropped_desc_status.extract_text().split('\n')
            # split desc and status
            l_status = []
            l_desc = []
            for t in l_desc_status:
                # print(t)
                if (t.endswith('DELETED')) | (t.endswith('ADDED')):
                    status = t.split()[-1]
                    desc = ''.join(t.split()[::-1][1:])
                else:
                    status = ''
                    desc = t

                if not desc.startswith('Total Count:'):
                    l_status += [status]
                    l_desc += [desc]

            # join into dataframe
            tmp = pd.DataFrame([l_cusip, l_issuer, l_desc, l_status],
                               index=['cusip', 'issuer', 'class', 'status']).T

            df = df.append(tmp)

            #add variants for cusip
            df['cusip6'] = df['cusip'].map(lambda x: x.replace(' ', '')[:6])
            df['cusip8'] = df['cusip'].map(lambda x: x.replace(' ', '')[:8])
            df['cusip9'] = df['cusip'].map(lambda x: x.replace(' ', '')[:9])

    # savev file as .csv
    df.to_csv(_file.replace('.pdf', '.csv'), index=False)
    print(df.tail().to_string())
    print(df.shape)

# this takes a couple of seconds
extract_list_of_13f_securities(_file)

# ----------------------------------------------------------------------------------------------------------------------
# match CUSIPS (from list of 13F securities) to NASDAQ tickers()
def match_CUSIPS_13F_tickers(f_tickers='NASDAQ_bio.csv',
                             f_13f='2020q2.csv'):

    # -----------------------------------------------------------------------------------
    # get list of 13F securities
    _file= os.getcwd() + '//List_of_13f_securities//' + f_13f
    cusips = pd.read_csv(_file)

    # only keep COM, ORD, COM PAR, SHS and SPONSORED ADR
    instrument_types = ['COM', 'ORD', 'COM PAR', 'SHS', 'SPONSORED ADR', 'ADR']
    cusips = cusips[~cusips['class'].isin(['PUT', 'CALL'])]
    cusips = cusips[~cusips['class'].str.startswith('*W')]
    cusips = cusips[~cusips['class'].str.contains('NOTE')]
    cusips = cusips[~cusips['class'].str.contains('DEBT')]
    cusips = cusips[~cusips['class'].str.contains('DBCV')]
    cusips = cusips[~cusips['class'].str.startswith('PFD')]
    cusips = cusips[~cusips['class'].str.startswith('CONV')]
    cusips = cusips[~cusips['class'].str.startswith('UNIT')]
    cusips = cusips[~cusips['class'].str.startswith('RIGHT')]
    cusips = cusips[~cusips['class'].str.contains('PFD')]
    # drop deleted CUSIPs
    cusips = cusips[cusips['status'] != 'DELETED']

    # -----------------------------------------------------------------------------------
    # get list of NASDAQ tickers
    tickers = pd.read_csv(f_tickers)
    # some clean_up in tickers
    print(tickers[tickers.company_name.str.contains('amp;')].to_string())
    tickers['company_name'] = tickers['company_name'].str.replace('&amp;', '&').str.replace(',', '')
    print(tickers[tickers.company_name.str.contains('&')].to_string())

    # -----------------------------------------------------------------------------------
    # Map cusips to tickers
    # loop over tickers.
    # For each token in ticker:
    # 1) Cast token to uppercase
    # 2) filter on ISSUER NAME in dataframe 'cusips'
    # 3)    a) If one unique record has been found --> add CUSIP to dictionary dict_map
    #       b) If no record matches --> add NONE to dictionary dict_map
    #       c) If multiple records match --> filter results by next token
    dict_map_cusip = {}
    dict_map_13F_name = {}
    for row in tickers.iterrows():
        ticker = row[1].get('ticker')
        tokens = row[1].get('company_name').upper().split()
        tmp = cusips.copy(deep=True)
        # if ticker == 'NOVAN':
        #     break
        cnt = 0
        for t in tokens:
            # print(t)
            t = t.replace('(', '').replace(')', '').replace('.', '').replace("'", '')
            if cnt == 0:
                if tmp[tmp['issuer'].str.startswith(t[:len(t)-1])].shape[0] == 0:
                    tmp = tmp[tmp['issuer'].str.startswith(t[:len(t)-1])]
                else:
                    tmp = tmp[tmp['issuer'].str.startswith(t)]
                    # if there are multiple matching issuer names we revert to EXACT match
                    if tmp.issuer.unique().shape[0] > 1:
                        tmp = tmp[tmp['issuer'].str.split(' ').map(lambda x: x[0]) == t]

            else:
                if t.startswith('PHARM'):
                    t = 'PHARM'
                dict_keys = {'LIMITED': 'LTD',
                             'CORPORATION': 'CORP',
                             'LABORATORIES': 'LABS'}
                tmp = tmp[(tmp['issuer'].str.contains(t)) | (tmp['issuer'].str.contains(str(dict_keys.get(t))))]

            if tmp.shape[0] == 1:
                dict_map_cusip = {**dict_map_cusip, **{ticker: tmp['cusip9'].values[0]}}
                dict_map_13F_name = {**dict_map_13F_name, **{ticker: tmp['issuer'].values[0]}}
                break
            # increase token counter
            cnt += 1

    # update ticker list
    tickers['cusip'] = tickers['ticker'].map(dict_map_cusip)
    tickers['13F_name'] = tickers['ticker'].map(dict_map_13F_name)

    # save ticker list
    _file = os.getcwd() + '//NASDAQ_bio_enriched_' + f_13f
    tickers.iloc[:, 1:].to_csv(_file, index=False)

    print(tickers.tail(15).to_string())
    print(tickers[tickers.cusip.isnull()].to_string())
    tickers[tickers.cusip.isnull()].shape
    tickers[tickers.cusip.notnull()].shape

def match_CUSIPS_with_CIKS(f_tickers='NASDAQ_bio_enriched.csv'):

    # we use a precompiled map between CUSIPs and CIKs
    # ToDo: This CIK-CUSIP File is stale. We need to find a way how to update this. Possibly a manual process
    _f = os.getcwd() + '//cik-cusip-mapping-master//cik-cusip-maps.csv'
    map_cusips_cik = pd.read_csv(_f).drop_duplicates(subset=['cusip8'], keep='last')
    # map_cusips_cik.dropna(subset=['cik'], axis=0)
    print(map_cusips_cik.head())
    dict_cusip8_cik = dict(zip(map_cusips_cik['cusip8'], map_cusips_cik['cik'].astype(int)))

    # read the ticker list
    df = pd.read_csv(os.getcwd() + '//' + f_tickers)

    # enrich ticker list with CIK
    df['cusip8'] = df['cusip'].map(lambda x: str(x)[0:8])
    df['cik'] = df['cusip8'].map(lambda x: dict_cusip8_cik.get(str(x)))

    # save final list
    df.to_csv(_f, index=False)

    # print(df.head().to_string())
    # print(df[df.cik.notnull()].head().to_string())
    # print(df[(df.cusip8 != 'nan') & (df.cik.isnull())].to_string())

    #ToDo: using the unmapped records we can access EDGAR using the Ticker symbol to extract the CIK. We need to build a SELENIUM process for doing so
    # HTML: https://www.sec.gov/edgar/searchedgar/companysearch.html
    # Xpath for search box: //*[@id="company"]
    # Enter the ticker symbol
    # Confirm SEARCH button: //*[@id="search_button"]
    # Extract link text in Xpath: //*[@id="contentDiv"]/div[1]/div[3]/span/a
    unmapped_cusips = df[(df.cusip8 != 'nan') & (df.cik.isnull())]
    print('There are #', unmapped_cusips.shape[0], 'unmapped securities.')
    print(unmapped_cusips.head().to_string())

    def update_map_cusips_cik(ticker):

        # initiate Chrome instance
        driver = webdriver.Chrome()

        # open webpage
        html = 'https://www.sec.gov/edgar/searchedgar/companysearch.html'
        driver.get(html)
        time.sleep(3)
        print('Webpage loaded.')

        # Xpath for search box
        xpath = '//*[@id="company"]'
        elem = driver.find_element_by_xpath(xpath)
        elem.send_keys(ticker)
        elem.send_keys(Keys.ENTER)
        time.sleep(3)

        # extract CIK
        try:
            xpath = '//*[@id="contentDiv"]/div[1]/div[3]/span/a'
            elem = driver.find_element_by_xpath(xpath)
            cik = int(elem.text.split(' ')[0])
        except:
            cik = np.nan
        # close driver
        driver.close()

        return cik

    if unmapped_cusips.shape[0] > 0:
        l_r = []
        for row in unmapped_cusips.iterrows():
            ticker = row[1].get('ticker')
            cusip8 = row[1].get('cusip8')

            cik = update_map_cusips_cik(ticker)
            r = (cik, cusip8[:6], cusip8)
            l_r += [r]
        tmp = pd.DataFrame(l_r, columns=['cik', 'cusip6', 'cusip8'])

        # append to original records
        map_cusips_cik = map_cusips_cik.append(tmp).drop_duplicates(keep='last').dropna(subset=['cik'], axis=0)
        # save file
        print('Updated file cik-cusip-maps.csv from EDGAR')
        map_cusips_cik.to_csv(_f)

# ----------------------------------------------------------------------------------------------------------------------
# match CUSIPS for Q1 2020
match_CUSIPS_13F_tickers(f_tickers='NASDAQ_bio.csv',
                         f_13f='2020q1.csv')
match_CUSIPS_with_CIKS(f_tickers='NASDAQ_bio_enriched_2020q1.csv')

# match CUSIPS for Q2 2020
match_CUSIPS_13F_tickers(f_tickers='NASDAQ_bio.csv',
                         f_13f='2020q2.csv')
match_CUSIPS_with_CIKS(f_tickers='NASDAQ_bio_enriched_2020q2.csv')

# match CUSIPS for Q3 2020
match_CUSIPS_13F_tickers(f_tickers='NASDAQ_bio.csv',
                         f_13f='2020q3.csv')
match_CUSIPS_with_CIKS(f_tickers='NASDAQ_bio_enriched_2020q3.csv')
# ----------------------------------------------------------------------------------------------------------------------