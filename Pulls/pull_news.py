
#import libraries
from pandas.core.algorithms import unique
import pandas as pd
from pandas.core.frame import DataFrame
import pymysql #for performing sql operations in python
import os

def pull(start_date, end_date, keyword):
    '''
    Parameters:
        start_date/end_date - start and end of publishing dates to query (datetime objects)
        series_tags - list of strings of tags associated with the series in question to be used in filter (array)
        keyword 
    '''


    #create connection
    connection = pymysql.connect(host=os.environ.get('HOST'),
                                user=os.environ.get('DB_USER'),
                                password=os.environ.get('DB_PASSWORD'),
                                db='NEWS')


    #Create cursor
    my_cursor = connection.cursor()

    #get list of cached tables
    table_list=pd.read_csv("sp500_cache/sp500_cache.csv")['Search Name'].str.upper()

    if (keyword in list(table_list)): #if table is cached
        filtered_news=pd.DataFrame(columns=['headline', 'pub_date'])
        query="SELECT headline, pub_date FROM {} WHERE pub_date BETWEEN {} and {}".format("`"+keyword+"`","'"+start_date+"'","'"+end_date+"'")
        temp=pd.read_sql(query, connection) 
        filtered_news=filtered_news.append(temp, ignore_index=True)
    
    else: #if not cached, search in wsj and nyt
        filtered_news=pd.DataFrame(columns=['headline', 'pub_date'])
        query="SELECT headline, pub_date FROM wsj WHERE headline LIKE {} AND pub_date BETWEEN {} and {}".format("'%"+keyword+"%'","'"+start_date+"'","'"+end_date+"'")
        temp=pd.read_sql(query, connection)
        filtered_news=filtered_news.append(temp, ignore_index=True)
        query="SELECT headline, pub_date FROM nyt WHERE headline LIKE {} AND pub_date BETWEEN {} and {}".format("'%"+keyword+"%'","'"+start_date+"'","'"+end_date+"'")
        temp=pd.read_sql(query, connection)
        filtered_news=filtered_news.append(temp, ignore_index=True)


    #Close the connection
    connection.close()

    return(filtered_news)

