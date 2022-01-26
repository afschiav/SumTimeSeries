'''
README
    This module develops methods for interacting with the Federal Reserve Economic Database (FRED) API.
    For API documentation see: 
'''

#import libraries
import requests
import pandas as pd
import time
import os 
from requests.api import request

#API Credentials
API_KEY =  os.environ.get('FRED_API_KEY')

#Functions
def get_series(SERIES_ID):
    
    #make API requests. See https://fred.stlouisfed.org/docs/api/fred/ for documentation
    observations_url="https://api.stlouisfed.org/fred/series/observations?series_id="+SERIES_ID+"&file_type=json&api_key="+API_KEY
    tag_url="https://api.stlouisfed.org/fred/series/tags?series_id="+SERIES_ID+"&api_key="+API_KEY+"&file_type=json"
    seriesinfo_url="https://api.stlouisfed.org/fred/series?series_id="+SERIES_ID+"&api_key="+API_KEY+"&file_type=json"

    #get APIs from FRED
    observations=requests.get(observations_url).json()
    tags=requests.get(tag_url).json()
    series_info=requests.get(seriesinfo_url).json()

    #create empty pandas dataframe
    df=pd.DataFrame(columns=["series","pub_date", "val", 'tags', 'freq'])

    #generate list of tags
    tag_list=[]
    for i in range(int(tags['count'])):
        tag_list.append(tags['tags'][i]['name'])

    #save observations into pandas dataframe
    for i in range(len(observations['observations'])): 
        pub_date=observations['observations'][i]['date']#save date
        value=observations['observations'][i]['value']#save observation
        df=df.append({'series':SERIES_ID,
        'pub_date':pub_date,
        'val':value, 
        'tags':str(tag_list),
         'freq':series_info['seriess'][0]['frequency_short']},
         ignore_index=True)
    
    return(df)