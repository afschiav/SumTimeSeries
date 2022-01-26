#####README#####
#This module defines methods for requesting historical articles
#from the New York Times (NYT). details found here: https://developer.nytimes.com/docs/archive-product/1/overview
#The Archive API returns an array of NYT articles for a given month, going back to 1851.

#import libraries
import requests
import pandas as pd
import time
import os 

#API Credentials
API_KEY =  os.environ.get('NYT_API')

#Functions
def get_stories(year, month):
    #make API call
    url="https://api.nytimes.com/svc/archive/v1/"+year+"/"+month+".json?api-key="+API_KEY

    #get response from FRED
    response=requests.get(url).json()
    
            
    #create empty pandas dataframe
    df=pd.DataFrame(columns=["headline", "abstract", "section_name", "keywords", "pub_date"])
    
    for i in range(len(response['response']['docs'])):
        headline=response['response']['docs'][i]['headline']['main'] #get article headline
        abstract=response['response']['docs'][i]['abstract'] #get article abstract
        section_name=response['response']['docs'][i]['section_name'] #get article section name
        keywords=str(response['response']['docs'][i]['keywords']) #get article keywords (convert to string)
        pub_date=response['response']['docs'][i]['pub_date'][0:10]#get date of article
        
        
        df=df.append({'headline':headline, 'abstract':abstract, 'section_name':section_name, 'keywords':keywords, 'pub_date':pub_date}, ignore_index=True)
    
    return(df)