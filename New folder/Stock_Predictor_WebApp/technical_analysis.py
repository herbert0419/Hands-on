import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import yfinance as yf
import datetime
import warnings
warnings.filterwarnings('ignore')


# @st.cache(suppress_st_warning=True)
def calculated_df(df):
    df['Date'] = df.index
    df['Day_Perc_Change'] = df['Adj Close'].pct_change()*100
    df.dropna(inplace= True)
    df['Trend']= np.zeros(df['Day_Perc_Change'].count())
    df['Trend']= df['Day_Perc_Change'].apply(lambda x:trend(x))
    return df 

def last_2_years_price_plot(df):
    df['Adj Close'].plot()
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price')

# def daily_percent_change(df):
    
def daily_percent_change_plot(df):
    calculated_df(df)['Day_Perc_Change'].plot()
    plt.xlabel('Date')
    plt.ylabel('Percenatge returns')

def daily_percent_change_histogram(df):
    calculated_df(df)['Day_Perc_Change'].hist(bins = 50) 
    plt.xlabel('Daily returns')
    plt.ylabel('Frequency')
    plt.show()

def trend(x):
    if x > -0.5 and x <= 0.5:
        return 'Slight or No change'
    elif x > 0.5 and x <= 1:
        return 'Slight Positive'
    elif x > -1 and x <= -0.5:
        return 'Slight Negative'
    elif x > 1 and x <= 3:
        return 'Positive'
    elif x > -3 and x <= -1:
        return 'Negative'
    elif x > 3 and x <= 7:
        return 'Among top gainers'
    elif x > -7 and x <= -3:
        return 'Among top losers'
    elif x > 7:
        return 'Bull run'
    elif x <= -7:
        return 'Bear drop'
    
def trend_pie_chart(df):
    pie_label = sorted([i for i in calculated_df(df).loc[:, 'Trend'].unique()])
    plt.pie(calculated_df(df)['Trend'].value_counts(), labels = pie_label, autopct = '%1.1f%%', radius = 2)
    plt.show()

# def volume_plot(df):
#     plt.stem(calculated_df(df)['Date'], calculated_df(df)['Day_Perc_Change'])
#     (calculated_df(df)/1000000).plot(figsize = (15, 7.5), color = 'green', alpha = 0.5)
# Daily volume of trade has been reduced in scale to match with the daily return scale

def volume_plot(df):
    calculated = calculated_df(df)
    plt.stem(calculated['Date'], calculated['Day_Perc_Change'])
    (df['Volume']/1000000).plot(figsize=(15, 7.5), color='green', alpha=0.5)
    # Daily volume of trade has been reduced in scale to match with the daily return 
    
# def correlation_plot(df):
#     # calculated = calculated_df(df)
#     selected_stocks = st.multiselect('Select stocks', ['AAPL', 'MSFT', 'GOOG', 'AMZN'])
#     df = yf.download(selected_stocks, start='2010-01-01', end='2022-02-25')
#     corr_matrix = df.corr()
#     sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    
 
    
def volatility(df):
    calculated = calculated_df(df)

    calculated['Daily_Return'] = calculated['Adj Close'].pct_change()

    # Calculate the rolling standard deviation (volatility) over 30 days
    calculated['Volatility'] = calculated['Daily_Return'].rolling(window=30).std() * (252**0.5)
    
