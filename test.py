import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import bs4 as bs
import pickle
import requests
import os


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("data/sp500.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('data/sp500.pickle', 'rb') as f:
            tickers = pickle.load(f)

def compile_data():
    with open('data/sp500.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, tickers in enumerate(tickers):
        df = pd.read_csv('st ')


if __name__ == '__main__':

    style.use('ggplot')

    # Extracting data from web

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)
    
    df = web.DataReader('BBD-B.TO', 'yahoo', start, end)
    df.to_csv('data/bbd.csv')


    #df = pd.read_csv('data/tsla.csv', parse_dates=True, index_col=0)

    # Ploting value

    df['Close'].plot()
    plt.show()
    print(df)


    # Creating own indicator over pandas
    '''
    df = pd.read_csv('data/tsla.csv', parse_dates=True, index_col=0)
    df['100ma'] = df['Adj Close'].rolling(window=100).mean()
    print(df.tail())
    
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    
    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax2.plot(df.index, df['Volume'])
    
    plt.show()
    
    '''

    # Creating candlestick graph
    '''
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()
    
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()
    '''

    #ticker =save_sp500_tickers()
    #print(ticker)
