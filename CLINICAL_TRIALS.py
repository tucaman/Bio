from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

import pandas as pd
from bs4 import BeautifulSoup
import re
import time


# init browser
driver = webdriver.Chrome()
# Clinical trials - Advanced search
webpage = 'https://clinicaltrials.gov/ct2/search/advanced'
# open webpage
driver.get(webpage)
time.sleep(3)
print('Webpage loaded.')

# Search for Sponsor (Lead):
x_path = '/html/body/div[6]/div[3]/div/form/fieldset/div[17]/div[2]/input'
elem = driver.find_element_by_xpath(x_path)
elem.send_keys('Chemocentryx')
# execute the search

from selenium.webdriver.common.keys import Keys
elem.send_keys(Keys.RETURN)
# modify the columns displayed on result page
dict_x_path={'study_start': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[16]/span',
             'primary_completion': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[17]/span',
             'study_completion': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[18]/span',
             'last_update': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[20]/span',
             'location': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[22]/span',
             'phase': '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/button[5]/span'}
for x_path_res in dict_x_path.values():
    x_path = '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[3]/button/span'
    elem = driver.find_element_by_xpath(x_path)
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_xpath(x_path_res)
    elem.click()
    time.sleep(1)

# set # of results per page
x_path = '/html/body/div[6]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/label/select'
dropdown = driver.find_element_by_xpath(x_path)
# click the dropdown button
dropdown.click()
# find all list elements in the dropdown.
# target the list of options
li = dropdown.find_elements_by_tag_name('option')
# click the second element in list
li[3].click()

# download the results table
html = driver.page_source
soup = BeautifulSoup(html)
tables = soup.find_all('table')
table = tables[1]
# convert to table
df = pd.read_html(str(table))[0]
print(df.head().to_string())
print(df.shape)