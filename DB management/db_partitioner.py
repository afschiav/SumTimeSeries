#import libraries
import pandas as pd
import pymysql #for performing sql operations in python
from sqlalchemy import create_engine #used for inserting  entire pandas dataframes into db
import os

''''
Program takes aggregate nyt and wsj tabls and creates keyword-based tables to speed up querying on front-end.
'''

def partition_data_by_word(keywords):

    #create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@timeline-project-db.cygoysgq94f1.us-east-2.rds.amazonaws.com/{db}"
                        .format(user=os.environ.get('DB_USER'),
                                pw=os.environ.get('DB_PASSWORD'),
                                db="NEWS"))

    #create connection
    connection = pymysql.connect(host='timeline-project-db.cygoysgq94f1.us-east-2.rds.amazonaws.com',
                                user='admin',
                                password='Ghdje43#!da',
                                db='NEWS')

    #create cursor 
    cursor=connection.cursor() 

    #query nyt data
    query="SELECT headline, pub_date FROM nyt"
    temp=pd.read_sql(query, connection) #get data...
    
    #query wsj data
    query="SELECT headline, pub_date FROM wsj"
    temp1=pd.read_sql(query, connection) #get data...
    
    #create aggregate df
    temp=temp.append(temp1, ignore_index=True)
    temp['headline']=temp['headline'].str.upper()

    del temp1
    

    #filter articles by keyword
    for word in keywords:
        df=temp[temp['headline'].str.contains(word.upper())]
        df.reset_index(inplace=True, drop=True)
        #write table to database
        df.to_sql(word.upper(), con = engine, if_exists = 'replace', chunksize = 1000, index=False)
        print("Table "+word.upper()+" successfully written to database!")
        del df

    #close db connection
    cursor.close()
    connection.close()



#MAIN
def main():
    meta_cache=pd.read_csv("nasdaq_cache.csv")
    partition_data_by_word(meta_cache['Search Name'])

if __name__ == "__main__":
    main()