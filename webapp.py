from pickle import TRUE
import streamlit as st 
import pandas as pd
import numpy as np 
import yfinance as yf
import pandas_market_calendars as mcal

import time
#import pull_series
#import pull_breakpoints
import pull_news

from datetime import date
from dateutil.relativedelta import relativedelta


import plotly.express as px
import plotly.graph_objects as go
from lexrank import STOPWORDS, LexRank
from path import Path
from sklearn.mixture import GaussianMixture

#######FUNCTIONS############

def int_to_date(x): #converts number of units since first date (int) to datetime object
    if series.freq[0] == "B":
        date=date_crosswalk.loc[x,'dates']
        return date
    else:
        date=(pd.date_range(start=series.pub_date[0], periods=x, freq=series.freq[0]+"S")[-1])
        return date

def pick_components(data, max_group): #finds number of components that minimizes the bic
            bic_list=[]
            for i in range(1,max_group+1):
                bic_list.append(GaussianMixture(n_components=i, random_state=0).fit(data).bic(data))
            return(bic_list.index(min(bic_list))+1)


#######WEBPAGE#######

###side bar###
st.sidebar.title('Welcome to SumTimeSeries!')

st.sidebar.write("""
 Enter a stock and select a period you are interested in learning more about. An interactive plot will be generated to tell its story using news headlines from the New York Times and Wall Street Journal.
""")

series_name=st.sidebar.text_input(
    label="TICKER",
    value="AAPL",
    max_chars=7,
    help="A 3-6 character value associated with a stock, bond, or other security.  \n Note: right now only in the S&P500 are supported!"
)

firm = yf.Ticker(series_name)

if firm.history(period="min").empty: #this takes a long time
    st.warning('Please input a valid ticker.')
    st.stop()

data=firm.history(period="max")
max_val=date(year=int(str(max(data.index))[0:4]), month=int(str(max(data.index))[5:7]), day=int(str(max(data.index))[8:10]))
min_val=date(year=int(str(min(data.index))[0:4]), month=int(str(min(data.index))[5:7]), day=int(str(min(data.index))[8:10]))

time_range = st.sidebar.slider(
    "Select date range",
    min_value=min_val,
    max_value=max_val,
    value=(date(2010,1,1),date(2020,1,1)),
    format="YYYY-MM-DD")


range_scalar=(time_range[1]-time_range[0]).total_seconds()/2592000

#################CODE BELOW EXECUTES AFTER USER PRESSES 'BUILD TIMELINE' BUTTON###########################


col1, col2, col3 , col4, col5 = st.sidebar.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    build_button = st.button('Go')


st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")
st.sidebar.text(" \n")

st.sidebar.write("For documentation, source code, and project details, visit my [GitHub page](https://github.com/afschiav)!")
#st.sidebar.write("[link](https://github.com/afschiav)")

if build_button==False:
    ###center page###
    series_name="AAPL"
    full_name="Apple Inc."

    series=pd.read_csv(r"home_screen/series.csv")
    breakpoints=pd.read_csv(r"home_screen/breakpoints.csv")

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=series.pub_date,
                            y=series.val,
                            mode='lines',
                            hovertemplate='%{y:$.2f}<br><b> Date: %{x}<extra></extra>',
    ))
    for i in range(len(breakpoints.index)):
        fig.add_vrect(
            x0=breakpoints['breaks'][i],
            x1=breakpoints['leads'][i],
            fillcolor="blue",
            opacity=0.2,
            line_width=0    
        )
        fig.add_trace(
            go.Scatter(
                x=[breakpoints['breaks'][i],breakpoints['breaks'][i],breakpoints['leads'][i],breakpoints['leads'][i],breakpoints['breaks'][i]], 
                y=[min(series.val)*.95,max(series.val)*1.05,max(series.val)*1.05,min(series.val)*.95,min(series.val)*.95], 
                fill="toself",
                mode='lines',
                name='',
                text=str(breakpoints['summary'][i])[1:len(str(breakpoints['summary'][i]))-1].replace(", '", '<br>'),
                hovertemplate='This: %{text}',
                opacity=0
            )
        )
    fig.update_layout(showlegend=False,
                    yaxis_title=series_name,
                    title=full_name,
                    title_font_size=25,
                    width=1000,
                    height=600,
                    margin=go.layout.Margin(
                        l=3, #left margin
                        r=3, #right margin
                        #b=0, #bottom margin
                        #t=0, #top margin
    )
    )


    #plot!
    st.plotly_chart(fig, use_container_width=True)
    st.info("How it works:  \n  \n Blue rectangles highlight detected events in the time-series. These are detected using an unsupervised method called [Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html). Articles corresponding to each event are queried and summarized using a text summarization method called [LexRank](https://pypi.org/project/lexrank/). Hover your cursor over an event to see its summary!")

else:
    st.empty()
    with st.spinner("Building! This will take a minute..."):

        #get firm data from yfinance
        firm = yf.Ticker(series_name)
        data=firm.history(start=str(time_range[0]), end=str(time_range[1]))
        data.reset_index(inplace=True)
        series=pd.DataFrame({'pub_date':data['Date'], 'val':data['Open']})
        

        #get firm info from S&P500 cache
        sp500_cache=pd.read_csv("sp500_cache/sp500_cache.csv")
    
        if sp500_cache.Symbol.str.contains(series_name).any():
            full_name=sp500_cache.loc[sp500_cache.index[sp500_cache['Symbol'] == series_name][0], 'Name']
            name=sp500_cache.loc[sp500_cache.index[sp500_cache['Symbol'] == series_name][0], 'Search Name']

        else:
            full_name=firm.info['shortName']#this is quite slow
            name=full_name.split()[0].upper()


        #establish date crosswalk
        nyse = mcal.get_calendar('NYSE')
        date_crosswalk=pd.DataFrame({'dates':nyse.valid_days(start_date=str(time_range[0]), end_date=str(time_range[1]))})

        #create time variable that corresponds to dates
        series['time']=range(len(series.index))

        #create frequency variable
        series['freq']="B" #B is for 'Business Day Frequency'

        #remove negative values
        series=series[series.val>0]
        series.reset_index(inplace=True)

        #compute first-diff moving average
        series['val_SMA_4']=series['val'].rolling(window=10).mean()
        series['D_val_SMA_4']=series['val_SMA_4']-series['val_SMA_4'].shift(1)
        series['D_val_SMA_4']=series['D_val_SMA_4'].abs()

        #remove na values 
        series=series[~series['D_val_SMA_4'].isna()]
        series.reset_index(inplace=True, drop=True)

        ####### mixture model ######

        #determine optimal number of mixtures (max of 20)s
        n=pick_components(series[['time','D_val_SMA_4']], 20)

        #estimate mixture model
        MM=GaussianMixture(n_components=n, covariance_type='full').fit(series[['time','D_val_SMA_4']])
        MM_centers=pd.DataFrame(MM.means_) #get mean parameters of distribution

        MM_centers.rename({0:'time', 1:'D_val_SMA_4'}, axis=1, inplace=True)
        MM_centers['abs_D_val_SMA_4']=MM_centers['D_val_SMA_4'].abs() #create abs. val

        MM_centers.sort_values(by='abs_D_val_SMA_4', ascending=False, inplace=True) #sort in decending order
        MM_centers.reset_index(inplace=True)
        MM_centers=MM_centers.loc[0:10,] #select mixtures with largest abs. vals (max 10)

        ####gather breakpoints####

        #obtain breakpoints (mean time values for each cluster)
        breaks=np.round(MM_centers['time']).astype(int).apply(int_to_date)

        #create leads
        leads=np.round(MM_centers['time']).astype(int) 
        leads=leads.apply(int_to_date)+pd.DateOffset(months=round(range_scalar/360)+2) #determine here the approapriate lead time to get relevant news articles

        #create breakpoint dataframe
        breakpoints=pd.DataFrame({"breaks":breaks, "leads":leads})


        #####text summarization model#####

        #initialize LexRank
        documents = []

        #note: the corpus should be adapted for type of series being analyzed. options are: business, entertainment, politics, sports, and tech
        documents_dir = Path('corpus/')

        for file_path in documents_dir.files('*.txt'):
            with file_path.open(mode='rt', encoding='utf-8') as fp:
                documents.append(fp.readlines())

        lxr = LexRank(documents, stopwords=STOPWORDS['en'])

        event_summaries=[]
        for i in range(len(breaks.index)):
            news=pull_news.pull(str(breakpoints['breaks'][i])[0:10], str(breakpoints['leads'][i])[0:10], name.upper()) 
            text=news['headline'].array
            summary=lxr.get_summary(text, summary_size=2, threshold=.1)
            event_summaries.append(summary)

        breakpoints['summary']=event_summaries

        series=series[series.val>0]

        fig=go.Figure()
        fig.add_trace(go.Scatter(x=series.pub_date,
                                y=series.val,
                                mode='lines',
                                hovertemplate='%{y:$.2f}<br><b> Date: %{x}<extra></extra>',
        ))
        for i in range(len(breaks.index)):
            fig.add_vrect(
                x0=breakpoints['breaks'][i],
                x1=breakpoints['leads'][i],
                fillcolor="blue",
                opacity=0.2,
                line_width=0    
            )
            fig.add_trace(
                go.Scatter(
                    x=[breakpoints['breaks'][i],breakpoints['breaks'][i],breakpoints['leads'][i],breakpoints['leads'][i],breakpoints['breaks'][i]], 
                    y=[min(series.val)*.95,max(series.val)*1.05,max(series.val)*1.05,min(series.val)*.95,min(series.val)*.95], 
                    fill="toself",
                    mode='lines',
                    name='',
                    text=str(breakpoints['summary'][i])[1:len(str(breakpoints['summary'][i]))-1].replace(", '", '<br>'),
                    hovertemplate='This: %{text}',
                    opacity=0
                )
            )
        fig.update_layout(showlegend=False,
                        yaxis_title=series_name,
                        title=full_name,
                        title_font_size=25,
                        width=1000,
                        height=600,
                        margin=go.layout.Margin(
                            l=3, #left margin
                            r=3, #right margin
                            #b=0, #bottom margin
                            #t=0, #top margin
    )
    )


    #plot!
    st.plotly_chart(fig, use_container_width=True)
    st.info("How it works:  \n  \n Blue rectangles highlight detected events in the time-series. These are detected using an unsupervised method called [Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html). Articles corresponding to each event are queried and summarized using a text summarization method called [LexRank](https://pypi.org/project/lexrank/). Hover your cursor over an event to see its summary!")

