'''
README

This program webscrapes articles from WSJ archives and populates wsj table in NEWS database
'''

import csv #import csv reader
import os
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException        
from selenium.common.exceptions import NoSuchWindowException        
import pandas as pd
import pymysql #for performing sql operations in python
from sqlalchemy import create_engine #used for inserting  entire pandas dataframes into db


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@timeline-project-db.cygoysgq94f1.us-east-2.rds.amazonaws.com/{db}"
                       .format(user=os.environ.get('DB_USER'),
                               pw=os.environ.get('DB_PASSWORD'),
                               db="NEWS"))

#optimize driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors') #ignore certification errors
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')#headless browsing
#options.add_extension('/path/to/extension.crx')#block ads

chrome_prefs = {} #disable images
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

#establish driver:
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

#function checks if element exists
def check_element_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#function scrapes article titles from WSJ for specified 'date'
def pull_date(date):
    ''''
    'date' is in YYYY-MM-DD HH:MM:SS format
    '''
    date=str(date)
    day=date[8:10]
    month=date[5:7]
    year=date[0:4]

    #initialize
    driver.get('https://www.wsj.com/news/archive/'+year+'/'+month+'/'+day+'?page='+str(1))
    num_pages=0
    if check_element_exists_by_xpath('//*[@id="main"]/div[2]/div/div/div/span'):
        num_pages=int(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/span').text.replace("of ",''))
    df=pd.DataFrame(columns=["headline","article_rank","page_rank", "pub_date"])
    
    for page_index in range(1,num_pages+1):
        driver.get('https://www.wsj.com/news/archive/'+year+'/'+month+'/'+day+'?page='+str(page_index))
        scraped_data=driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/ol').text.splitlines() #get all info

        headlines=scraped_data[1::3] #pick headlines from text
        article_ranks=range(1,len(headlines)+1) #establish article position on page
        page_ranks=np.repeat(page_index, len(headlines)) #record page number
        pub_dates=np.repeat(str(date)[0:10],len(headlines)) #record date

        df_temp=pd.DataFrame({"headline":headlines,"article_rank":article_ranks,"page_rank":page_ranks,"pub_date":pub_dates})
        df=df.append(df_temp, ignore_index=True)

    
    return(df)

#range: 1998-01-01 to 2021-212-28
#last 2021-12-28
for date in pd.date_range('2020-07-05', '2021-12-28', freq='D'): 
    df=pull_date(date)
    print("here")
    df.to_sql('wsj', con = engine, if_exists = 'append', chunksize = 1000, index=False)
    print(str(date)+"successfully uploaded to wsj table")
 



