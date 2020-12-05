# import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import platform
import logging
logging.basicConfig(level=logging.INFO)
import sys

try:
    # finding the user's OS
    # then finding the correct version of chrome
    # then running the chromedriver by setting the correct path
    # literally trying every possible version, so you can't really mess this up
    if platform.system() == 'Linux':
        logging.info('OS Detcted: Linux')
        try:
            chromedriver_path = os.path.abspath('chromedriver/chromedriver_linux64/chromedriver88')
            driver = webdriver.Chrome(executable_path=chromedriver_path)
            logging.info('Successfuly launched driver version 88')
        except:
            try:
                chromedriver_path = os.path.abspath('chromedriver/chromedriver_linux64/chromedriver87')
                driver = webdriver.Chrome(executable_path=chromedriver_path)
                logging.info('Successfuly launched driver version 87')
            except:
                try:
                    chromedriver_path = os.path.abspath('chromedriver/chromedriver_linux64/chromedriver86')
                    driver = webdriver.Chrome(executable_path=chromedriver_path)
                    logging.info('Successfuly launched driver version 86')
                except:
                    logging.error('chromedriver path error')
                    sys.exit(0)
    elif platform.system() == 'Darwin':
        logging.info('OS Detcted: Mac (Darwin)')
        try:
            chromedriver_path = os.path.abspath('chromedriver/chromedriver_mac64/chromedriver88')
            driver = webdriver.Chrome(executable_path=chromedriver_path)
            logging.info('Successfuly launched driver version 88')
        except:
            try:
                chromedriver_path = os.path.abspath('chromedriver/chromedriver_mac64/chromedriver87')
                driver = webdriver.Chrome(executable_path=chromedriver_path)
                logging.info('Successfuly launched driver version 87')
            except:
                try:
                    chromedriver_path = os.path.abspath('chromedriver/chromedriver_mac64/chromedriver86')
                    driver = webdriver.Chrome(executable_path=chromedriver_path)
                    logging.info('Successfuly launched driver version 86')
                except:
                    logging.error('chromedriver path error')
                    sys.exit(0)
    elif platform.system() == 'Windows':
        logging.info('OS Detcted: Windows')
        try:
            chromedriver_path = os.path.abspath('chromedriver/chromedriver_win32/chromedriver88.exe')
            driver = webdriver.Chrome(executable_path=chromedriver_path)
            logging.info('Successfuly launched driver version 88')
        except:
            try:
                chromedriver_path = os.path.abspath('chromedriver/chromedriver_win32/chromedriver87.exe')
                driver = webdriver.Chrome(executable_path=chromedriver_path)
                logging.info('Successfuly launched driver version 87')
            except:
                try:
                    chromedriver_path = os.path.abspath('chromedriver/chromedriver_win32/chromedriver86.exe')
                    driver = webdriver.Chrome(executable_path=chromedriver_path)
                    logging.info('Successfuly launched driver version 86')
                except:
                    logging.error('chromedriver path error')
                    sys.exit(0)
except:
    logging.error('Unrecognized OS')
    sys.exit(0)

# attempt to get URL
try:
    url = 'https://www.walmart.com/m/deals/christmas-gifts'
    driver.get(url)
    logging.into('Successfully got URL')
except:
    logging.warning('Possible URL error')
    # sys.exit(0)

# attempt to get page
try:
    page = driver.execute_script('return document.body.innerHTML')
    logging.info('Successfuly got page')
except:
    logging.error('Failed to get page')
    sys.exit(0)

# attempt to soupify
try:
    soup = BeautifulSoup(''.join(page), 'html5lib')
    logging.info('Soup Achieved!')
except:
    logging.error('Failed to convert page to BeautifulSoup')
    sys.exit(0)



gridview_ul = soup.find('ul',{'class':'search-result-gridview-items'})

li_list = gridview_ul.find_all('li',limit=None)

x = li_list[0].prettify()
print(x)
