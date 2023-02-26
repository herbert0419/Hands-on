import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
import warnings
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
warnings.filterwarnings('ignore')

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

def volume_plot(df):
    # Daily volume of trade has been reduced in scale to match with the daily return scale
    calculated_data = calculated_df(df)
    plt.stem(calculated_data['Date'], calculated_data['Day_Perc_Change'])
    (calculated_data['Volume']/1000000).plot(figsize = (15, 7.5), color = 'green', alpha = 0.5)
    plt.show()


def correlation_plot(df):
    # Adj close price of all the stocks
    combined_df = yf.download(["ADANIENT.NS","TATASTEEL.NS","PAGEIND.NS","EICHERMOT.NS","INFY.NS"], start="2010-01-01", end="2023-02-12")['Adj Close']
    combined_df = combined_df.round(2)
    combined_df.head()
    
def volatility_plot(df):
    ADANI_vol = calculated_df(df)['Day_Perc_Change'].rolling(7).std()*np.sqrt(7)
    ADANI_vol.plot()


def generate_buy_sell_signals(condition_buy, condition_sell, dataframe, strategy):
    last_signal = None
    indicators = []
    buy = []
    sell = []
    for i in range(0, len(dataframe)):
        # if buy condition is true and last signal was not Buy
        if condition_buy(i, dataframe) and last_signal != 'Buy':
            last_signal = 'Buy'
            indicators.append(last_signal)
            buy.append(dataframe['Close'].iloc[i])
            sell.append(np.nan)
        # if sell condition is true and last signal was Buy
        elif condition_sell(i, dataframe)  and last_signal == 'Buy':
            last_signal = 'Sell'
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(dataframe['Close'].iloc[i])
        else:
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(np.nan)

    dataframe[f"{strategy}_Last_Signal"] = np.array(last_signal)
    dataframe[f"{strategy}_Indicator"] = np.array(indicators)
    dataframe[f"{strategy}_Buy"] = np.array(buy)
    dataframe[f"{strategy}_Sell"] = np.array(sell)


def get_macd(company):
    close_prices = company['Close']
    window_slow = 26
    signal = 9
    window_fast = 12
    macd = MACD(close_prices, window_slow, window_fast, signal)
    company['MACD'] = macd.macd()
    company['MACD_Histogram'] = macd.macd_diff()
    company['MACD_Signal'] = macd.macd_signal()

    generate_buy_sell_signals(
    lambda x, company: company['MACD'].values[x] < company['MACD_Signal'].iloc[x],
    lambda x, company: company['MACD'].values[x] > company['MACD_Signal'].iloc[x],
    company,
    'MACD')
    return company

def plot_price_and_signals(company, strategy):
    # data = get_macd(company)
    data = company
    last_signal_val = data[f"{strategy}_Last_Signal"].values[-1]
    last_signal = 'Unknown' if not last_signal_val else last_signal_val
    title = f'Close Price Buy/Sell Signals using {strategy}.  Last Signal: {last_signal}'
    # fig.suptitle(f'Top: ADANI Stock Price. Bottom: {strategy}')
    if not data[f'{strategy}_Buy'].isnull().all():
        plt.scatter(data.index, data[f'{strategy}_Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
    if not data[f'{strategy}_Sell'].isnull().all():
        plt.scatter(data.index, data[f'{strategy}_Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
    plt.plot(company['Close'], label='Close Price', color='blue', alpha=0.35)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Close Price', fontsize=18)
    plt.legend(loc='upper left')


def plot_macd(company):
    macd = get_macd(company)
    plt.plot(macd['MACD'], label=' MACD', color = 'green')
    plt.plot(macd['MACD_Signal'], label='Signal Line', color='orange')
    positive = macd['MACD_Histogram'][(macd['MACD_Histogram'] >= 0)]
    negative = macd['MACD_Histogram'][(macd['MACD_Histogram'] < 0)]
    plt.bar(positive.index, positive, color='green')
    plt.bar(negative.index, negative, color='red')    
    plt.legend(loc='upper left')
    plt.show()

def get_rsi(company):
    close_prices = company['Close']
    # dataframe = company.technical_indicators
    rsi_time_period = 20

    rsi_indicator = RSIIndicator(close_prices, rsi_time_period)
    company['RSI'] = rsi_indicator.rsi()

    low_rsi = 40
    high_rsi = 70

    generate_buy_sell_signals(
        lambda x, company: company['RSI'].values[x] < low_rsi,
        lambda x, company: company['RSI'].values[x] > high_rsi,
    company, 'RSI')

    return company

def plot_rsi(company):
    rsi = get_rsi(company)
    low_rsi = 40
    high_rsi = 70
    plt.fill_between(rsi.index, y1=low_rsi, y2=high_rsi, color='#adccff', alpha=0.3)
    plt.plot(rsi['RSI'], label='RSI', color='blue', alpha=0.35)
    plt.legend(loc='upper left')
    plt.show()

def get_bollinger_bands(company):
    close_prices = company['Close']
    window = 20
    indicator_bb = BollingerBands(close=close_prices, window=window, window_dev=2)

    # Add Bollinger Bands features
    company['Bollinger_Bands_Middle'] = indicator_bb.bollinger_mavg()
    company['Bollinger_Bands_Upper'] = indicator_bb.bollinger_hband()
    company['Bollinger_Bands_Lower'] = indicator_bb.bollinger_lband()

    generate_buy_sell_signals(
        lambda x, company: company['Close'].values[x] < company['Bollinger_Bands_Lower'].values[x],
        lambda x, company: company['Close'].values[x] > company['Bollinger_Bands_Upper'].values[x],
        company, 'Bollinger_Bands')

    return company

def plot_bollinger_bands(company):
        bollinger_bands = get_bollinger_bands(company)

        # fig, axs = plt.subplots(2, sharex=True, figsize=(20, 8))
        # plot_price_and_signals(fig, company, bollinger_bands, 'Bollinger_Bands', axs)
        plt.plot(bollinger_bands['Bollinger_Bands_Middle'], label='Middle', color='blue', alpha=0.35)
        plt.plot(bollinger_bands['Bollinger_Bands_Upper'], label='Upper', color='green', alpha=0.35)
        plt.plot(bollinger_bands['Bollinger_Bands_Lower'], label='Lower', color='red', alpha=0.35)
        plt.fill_between(bollinger_bands.index, bollinger_bands['Bollinger_Bands_Lower'], bollinger_bands['Bollinger_Bands_Upper'], alpha=0.1)
        plt.legend(loc='upper left')
        plt.show()


    
def sma_plot(user_input, window):
    # Download data using yfinance
    data = yf.download(user_input, period='max')
    # Calculate SMA using rolling window
    sma = data['Close'].rolling(window=window).mean()
    # Create a dataframe for buy and sell signals
    buy_sell_df = pd.DataFrame(index=data.index)
    buy_sell_df['SMA'] = sma
    buy_sell_df['Close'] = data['Close']
    buy_sell_df['Signal'] = 0.0
    buy_sell_df['Buy'] = np.zeros(len(data))
    buy_sell_df['Sell'] = np.zeros(len(data))
    # Determine the buy and sell signals
    for i in range(1, len(data)):
        if sma[i] > data['Close'][i] and sma[i-1] <= data['Close'][i-1]:
            buy_sell_df['Signal'][i] = 1.0
            buy_sell_df['Buy'][i] = data['Close'][i]
        elif sma[i] < data['Close'][i] and sma[i-1] >= data['Close'][i-1]:
            buy_sell_df['Signal'][i] = -1.0
            buy_sell_df['Sell'][i] = data['Close'][i]
    # Create a plot of the stock price with SMA and buy and sell signals
    fig, ax = plt.subplots(figsize=(20, 9))
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(sma.index, sma, label=f'{window} Day SMA')
    ax.scatter(buy_sell_df.index[buy_sell_df['Signal'] == 1.0], buy_sell_df['Buy'][buy_sell_df['Signal'] == 1.0], marker='^', color='green', label='Buy')
    ax.scatter(buy_sell_df.index[buy_sell_df['Signal'] == -1.0], buy_sell_df['Sell'][buy_sell_df['Signal'] == -1.0], marker='v', color='red', label='Sell')
    ax.legend()
    return fig



def ema_plot(user_input, date_from, date_to):
    # Download data from Yahoo Finance API
    df = yf.download(user_input, start=date_from, end=date_to)

    # Compute EMA with a window of 20 days
    ema = df['Adj Close'].ewm(span=20, adjust=False).mean()

    # Create a plot of the stock price with EMA
    fig, ax = plt.subplots(figsize=(20, 9))
    ax.plot(df.index, df['Adj Close'], label='Close')
    ax.plot(ema.index, ema, label='EMA')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'{user_input} EMA plot')
    ax.legend()
    return fig