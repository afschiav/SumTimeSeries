
#import libraries
from pandas.core.algorithms import unique
import pandas as pd
import pymysql #for performing sql operations in python
import os

def pull(series):
    '''
    series - unique identifier of user-selected series (str)
    '''

    #create connection
    connection = pymysql.connect(host=os.environ.get('HOST'),
                                user=os.environ.get('DB_USER'),
                                password=os.environ.get('DB_PASSWORD'),
                                db='ECON')

    #Create cursor
    #my_cursor = connection.cursor()

    #Make query, save as df
    query="SELECT * FROM {}".format(series+"_breaks")
    df=pd.read_sql(query, connection)

    #Close the connection
    connection.close()
    
    
    return(df)
