# you NEED to download selenium, yagmail, and bs4 through pip
# and i am too tired to make a proper requirements.txt
# you also need to install html5lib
from selenium import webdriver
from bs4 import BeautifulSoup
import yagmail
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
            chromedriver_path = os.path.abspath('chromedriver\chromedriver_win32\chromedriver88.exe')
            driver = webdriver.Chrome(executable_path=chromedriver_path)
            logging.info('Successfuly launched driver version 88')
        except:
            try:
                chromedriver_path = os.path.abspath('chromedriver\chromedriver_win32\chromedriver87.exe')
                driver = webdriver.Chrome(executable_path=chromedriver_path)
                logging.info('Successfuly launched driver version 87')
            except:
                try:
                    chromedriver_path = os.path.abspath('chromedriver\chromedriver_win32\chromedriver86.exe')
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
# try:
soup = BeautifulSoup(''.join(page), 'html5lib')
logging.info('Soup Achieved!')
# except:
#     logging.error('Failed to convert page to BeautifulSoup')

# begin actual parsing of html
gridview_ul = soup.find('ul',{'class':'search-result-gridview-items'})

li_list = gridview_ul.find_all('li',limit=None)
# print(li_list[0].prettify())
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
            link_raw = product.find('a',{'class':"search-result-productimage gridview display-block"})['href']
            link = 'walmart.com'+link_raw
            # just putting this loop here for seperation reasons
            try:
                product_dict['prod_title'] = title
                product_dict['prod_price'] = price_txt
                product_dict['prod_img'] = img_src
                product_dict['prod_link'] = link
                product_dict_list.append(product_dict)
            except:
                continue
        except:
            continue
    except:
        continue
# we have all the data we need, so let's close this
driver.quit()

# begin SQL work
# connect to local server (aka the db file)
try:
    conn = sqlite3.connect('products.db')
    logging.info('Successful SQLite3 server connection')
    version_info = 'SQLite3 version: %s'%sqlite3.version
    logging.info(version_info)
    # create cursor
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
    # table creation
    sql_create_products_table = """ CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        product text NOT NULL,
                                        price text NOT NULL,
                                        img_src text NOT NULL,
                                        link text NOT NULL
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
        sql_insert_cmd = """INSERT INTO products (id,product,price,img_src,link)
                            VALUES ('%d','%s','%s','%s','%s'
                            );"""%(unique_id,entry['prod_title'],entry['prod_price'],entry['prod_img'],entry['prod_link'])
        unique_id+=1
        cursor.execute(sql_insert_cmd)
        conn.commit()
    except:
        # apparently there are some issues here, but it mostly works so whatever
        logging.error('Failed to add entry: %s'%entry['prod_title'])
        continue
conn.close()

# begin script to send emails
# the new email is fake.walmart.bot@gmail.com
# password is sweezer123
# first let's create an email with all the products, images, and prices
email_html_w = open('email_html.html','w')
email_html_w.write('')
logging.info('Clear email_html.html')
email_html_a = open('email_html.html','a+')
html_text = """
<html>
    <body>
        <h1>Here's some great deals from Walmart!</h1>
    """
email_html_a.write(html_text)
for entry in product_dict_list:
    entry_txt = """
    \t\t\t<img src="%s">
    \t\t\t<h4>%s</h4>
    \t\t\t<h4>%s</h4>
    \t\t\t<h4>%s</h4>
    """%(entry['prod_img'],entry['prod_title'],entry['prod_price'],entry['prod_link'])
    email_html_a.write(entry_txt)
html_close = """
    </body>
</html>"""
email_html_a.write(html_close)
logging.info('Successfully Compiled HTML')

# now let's actually send the thing
try:
    yag = yagmail.SMTP(user='fake.walmart.bot@gmail.com', password='sweezer123')
    logging.info("Yag connection successful")
except:
    logging.error("Yag failed to connect")

# iterate through list of emails and send
read_email_html = open('email_html.html','r').read()
reciepient_list = open('emails.txt','r').read().splitlines()
for reciepient in reciepient_list:
    yag.send(to=reciepient, subject='Holiday Deals From Walmart!', contents=read_email_html)
    logging.info('Sent email to %s'%reciepient)
