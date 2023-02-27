import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title='Stock Correlation Plot')

# Define function to fetch historical price data for a given ticker
@st.cache
def load_data(ticker):
    data = yf.download(ticker, start='2010-01-01', end='2022-02-25')
    return data

# Define function to generate correlation plot
def generate_correlation_plot(data):
    corr = data['Adj Close'].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm')
    plt.title('Correlation Plot')
    st.pyplot()

# Define Streamlit app
def main():
    # Set app title
    st.title('Stock Correlation Plot')
    
    # Get user input for stock tickers
    tickers = st.text_input('Enter stock tickers separated by commas (e.g. AAPL, MSFT)', value='AAPL, MSFT').upper().split(',')
    
    # Fetch and concatenate historical price data for the selected tickers
    data = pd.concat([load_data(ticker) for ticker in tickers], axis=1, keys=tickers)
    
    # Display data table
    st.write('Historical Price Data')
    st.write(data['Adj Close'])
    
    # Generate correlation plot
    generate_correlation_plot(data)

if __name__ == '__main__':
    main()
