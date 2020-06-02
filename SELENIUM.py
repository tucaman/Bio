from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

import pandas as pd
from bs4 import BeautifulSoup
import re
import time

def example():
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

def NASDAQ_SECTOR_TICKERS(sector='Healthcare'):

    dict_sector = {'Financial': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[1]/button',
                   'Healthcare': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[2]/button',
                   'Conglomerates': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[3]/button',
                   'Consumer Goods': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[4]/button',
                   'Services': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[5]/button',
                   'Utilities': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[6]/button',
                   'Basic Materials': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[7]/button',
                   'Technology': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[8]/button',
                   'Industrial Goods': '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[2]/ul/li[9]/button'}

    # initiate Chrome instance
    driver = webdriver.Chrome()

    # open webpage
    driver.get("https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download")
    time.sleep(10)
    print('Webpage loaded.')

    # accept cookies
    elem = driver.find_element_by_xpath('/html/body/div[8]/button[1]')
    elem.click()
    time.sleep(5)
    print('Cookie policy accepted.')

    # select only stocks for sector
    elem = driver.find_element_by_xpath(dict_sector.get(sector))
    elem.click()
    time.sleep(15)
    print('Sector selected.')

    # confirm selection
    # /html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[4]/button
    elem = driver.find_element_by_xpath('/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[3]/div[4]/button')
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
    last_page = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[10]/a'

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
        x_path = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[' + str(i) + ']/a'
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
        elem = driver.find_element_by_xpath('/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/div/table')
        html_string = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        table = soup.find_all('tbody')[0]  # Grab the first table

        l_df += [parse_table(table)]

    # Step 2
    num_page = 0
    while int(num_page) < int(last_page) - 1:

        x_path = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[8]/a'
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
        elem = driver.find_element_by_xpath('/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/div/table')
        html_string = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        table = soup.find_all('tbody')[0]  # Grab the first table

        l_df += [parse_table(table)]

    # Step 3
    i = 1
    while num_page < last_page:
        print(i)
        x_path = '/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/ul/li[' + str(8 + i) + ']/a'

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
        elem = driver.find_element_by_xpath('/html/body/div[3]/div/main/div/div[4]/div/section/div[1]/div[4]/div/table')
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
fd = 'C://Users//Lennart//PycharmProjects//Bio//'
df_bio.to_csv(fd + 'NASDAQ_bio.csv')
print(df_bio.shape)
print(df_bio.tail().to_string())
    # assert "Python" in driver.title

df_finance = NASDAQ_SECTOR_TICKERS(sector='Financial')
fd = 'C://Users//Lennart//PycharmProjects//Bio//'
df_finance.to_csv(fd + 'NASDAQ_finance.csv')
print(df_finance.shape)
print(df_finance.tail().to_string())
