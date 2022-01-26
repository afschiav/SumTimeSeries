'''
README
This python program popula

tes the nyt table in the NEWS database (AWS) by requesting each month of articles from
the NYT API.
'''

#import libraries
import nyt 
import pandas as pd
import pymysql #for performing sql operations in python
from sqlalchemy import create_engine #used for inserting  entire pandas dataframes into db
import os

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@timeline-project-db.cygoysgq94f1.us-east-2.rds.amazonaws.com/{db}"
                       .format(user=os.environ.get('DB_USER'),
                               pw=os.environ.get('DB_PASSWORD'),
                               db="NEWS"))

#populate nyt table
#Note: make sure pc is set to never sleep when populating large segments of data
for year in range(1900, 2022, 1):
    for month in range(1,13):
        df=pd.DataFrame(nyt.get_stories(str(year),str(month)))
        df.to_sql('nyt', con = engine, if_exists = 'append', chunksize = 1000, index=False)
        print(str(year)+"-"+str(month)+"successfully uploaded to nyt table")