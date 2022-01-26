'''
README
This python program populates the nyt table in the ECON database (AWS) by requesting each month of articles from
the FRED API.

THIS WILL NEED TO BE UPDATED WHEN INCLUDING DATA FROM OTHER SOURCES!
'''

#import libraries
import sqlalchemy
import fred 
import pandas as pd
import pymysql #for performing sql operations in python
from sqlalchemy import create_engine #used for inserting  entire pandas dataframes into db
import os

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@timeline-project-db.cygoysgq94f1.us-east-2.rds.amazonaws.com/{db}"
                       .format(user=os.environ.get('DB_USER'),
                               pw=os.environ.get('DB_PASSWORD'),
                               db="ECON"))

#populate fred table
#Note: make sure pc is set to never sleep when populating large segments of data
series_list=["T10Y2Y", "CPIAUCSL", "GDPC1", "SP500", "NASDAQCOM", "UNRATE"]
for series in series_list:
    df=pd.DataFrame(fred.get_series(series))
    df.to_sql('fred', con = engine, if_exists = 'append', chunksize = 1000, index=False)
    print(series+" successfully uploaded")