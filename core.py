# import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import platform
import logging
# prints info to console, comment out if not needed
logging.basicConfig(level=logging.INFO)
import sys
import sqlite3
from sqlite3 import Error


# this straight up doesn't work
# headless doesn't exactly matter, but it would be nice
# FIXME:
chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True

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
# this is kinda buggy
# FIXME:
try:
    url = 'https://www.walmart.com/m/deals/christmas-gifts'
    driver.get(url)
    logging.into('Successfully got URL')
except:
    logging.warning('Possible URL error')

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

# begin actual parsing of html
gridview_ul = soup.find('ul',{'class':'search-result-gridview-items'})

li_list = gridview_ul.find_all('li',limit=None)

product_dict_list = []
for product in li_list:
    product_dict = {}
    try:
        # get price or continue if no price
        price_raw = product.find('span',{'class':"price display-inline-block arrange-fit price price-main"})
        price = price_raw.find('span', {'class':"visuallyhidden"})
        price_txt = price.get_text()
        try:
            # get image and title from alt and src
            title_img_raw = product.find('img',alt=True)
            title = title_img_raw['alt']
            img_src = title_img_raw['src']
            # just putting this loop here for seperation reasons
            try:
                product_dict['prod_title'] = title
                product_dict['prod_price'] = price_txt
                product_dict['prod_img'] = img_src
                product_dict_list.append(product_dict)
            except:
                continue
        except:
            continue
    except:
        continue
# we have all the data we need, so let's clode this
driver.quit()

# begin SQL work
# connect to local server (aka the db file)
try:
    conn = sqlite3.connect('products.db')
    logging.info('Successful SQLite3 server connection')
    version_info = 'SQLite3 version: %s'%sqlite3.version
    logging.info(version_info)
    cursor = conn.cursor()
except Error as e:
    logging.error(e)
    sys.exit(0)

# attempt table creation
try:
    # drop table on run
    try:
        sql_products_drop = """ DROP TABLE IF EXISTS products;"""
        cursor.execute(sql_products_drop)
        logging.info('Dropped table products')
    except:
        logging.error('Drop error')
        sys.exit(0)
    sql_create_products_table = """ CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        product text NOT NULL,
                                        price text NOT NULL,
                                        img_src text NOT NULL
                                    ); """
    cursor.execute(sql_create_products_table)
    conn.commit()
    logging.info('Table created successfully')
except Error as e:
    logging.error(e)
    sys.exit(0)

# attempt to add all products to table
unique_id = 0
for entry in product_dict_list:
    # there's no reason why this wouldn't work, but it's best to be safe
    try:
        sql_insert_cmd = """INSERT INTO products (id,product,price,img_src)
                            VALUES ('%d','%s','%s','%s'
                            );"""%(unique_id,entry['prod_title'],entry['prod_price'],entry['prod_img'])
        unique_id+=1
        cursor.execute(sql_insert_cmd)
        conn.commit()
    except:
        logging.error('Failed to add entry: %s'%entry['prod_title'])
        continue
cursor.execute("SELECT * FROM products")
print(cursor.fetchall())
conn.close()
