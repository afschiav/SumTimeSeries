
#import libraries
from pandas.core.algorithms import unique
import pandas as pd
import pymysql #for performing sql operations in python
import os

def pull(series, source):
    '''
    series - unique identifier of user-selected series (str)
    source - source of data (fred, bea, bls, etc.) (str)
    '''

    #create connection
    connection = pymysql.connect(host=os.environ.get('HOST'),
                                user=os.environ.get('DB_USER'),
                                password=os.environ.get('DB_PASSWORD'),
                                db='ECON')

    #Make query, save as df
    query="SELECT * FROM {} WHERE series = {}".format(source, "'"+series+"'")
    df=pd.read_sql(query, connection)

    #Close the connection
    connection.close()
    
    
    return(df)

