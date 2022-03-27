#!/usr/bin/python3

"""
Creating a crypto traiding bot, base on the SMA200 and SMA600 market trend.
Trade on the 1h time.
The futur objectif of this traiding bot will be to create a AI, will predict the market stock price
but waiting to grab knowledge on AI in my next school year :)
"""

import pandas as pd
from binance.client import Client
from API_KEY import api_key, api_secret
from time import sleep

client = Client(api_key, api_secret)


def getHistoricalData():
    """
    Get the 600 close price
    Args: Nothing
    Return: Data
    """
    KlineT = client.get_historical_klines(
        'BTCEUR', Client.KLINE_INTERVAL_1HOUR, "26 day ago UTC")
    data = pd.DataFrame(KlineT, columns=['timestamp', 'open', 'high', 'low', 'close',
                        'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    return (data)


def clearData(data):
    """
    Clear all the useless columns
    Args:
        data (pd DataFrames): All the usefull data to work
    Returns: No return 
    """
    del data['close_time']
    del data['quote_av']
    del data['trades']
    del data['tb_base_av']
    del data['tb_quote_av']
    del data['ignore']

    data['close'] = pd.to_numeric(data['close'])
    data['high'] = pd.to_numeric(data['high'])
    data['low'] = pd.to_numeric(data['low'])
    data['open'] = pd.to_numeric(data['open'])

    data = data.set_index(data['timestamp'])
    data.index = pd.to_datetime(data.index, unit='ms')

    del data['timestamp']
    return data


def createIndicator(data):
    """
    Create the SMA200 and the SMA600 indicator
    Args:
        data (pandas DataFrame): The last 600+ closing price
    Return: Nothing
    """
    data['SMA200'] = data['close'].rolling(200).mean()
    data['SMA600'] = data['close'].rolling(600).mean()
    data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()


def checkEntryTrade(data, onMarket):
    """
    Check if it's a good moment to get on the market
    Args:
        data (pandas DataFrame) : The last 600+ candle
        onMarket (bool) : If we are already positionate on the market
    Return: True, time to invest, False, keep money
    """
    balanceEUR = client.get_asset_balance(asset='EUR')

    totalEUR = float(balanceEUR['free'])

    if totalEUR > 1 and onMarket == False:
        if data['SMA200'].iloc[-1] > data['SMA600'].iloc[-1] and data['SMA200'].iloc[-2] < data['SMA600'].iloc[-2]:
            return True
    return False


def checkExitTrade(data, moneyInvest, onMarket):
    """
    Check if it's a good moment to get on the market
    Args:
        data (pandas DataFrame) : The last 600+ candle
        moneyInvest (float) : The money we invert on the last order
        onMarket (bool) : If we are already positionate on the market
    Return: True, time to get out, False, keep it on the market
    """
    balanceBTC = client.get_asset_balance(asset='BTC')

    totalBTC = float(balanceBTC['free'])
    if totalBTC > 0.00001 and onMarket == True:
        if data['SMA200'].iloc[-1] < data['SMA600'].iloc[-1] and data['SMA200'].iloc[-2] > data['SMA600'].iloc[-2] or data['close'].iloc[-1] < moneyInvest * 0.93:
            return True
    return False


def invest(data):
    """
    Make an order to buy BTC
    Args:
        data (pandas DataFrame) : The last 600+ candle
    Return: The amount of invested money
    """
    balanceEUR = client.get_asset_balance(asset='EUR')
    totalEUR = float(balanceEUR['free'])

    quant = totalEUR/data['close'].iloc[-1]
    order = client.order_market_buy(
        symbol='BTCEUR',
        quantity=quant)
    print("Buy BTC")
    return totalEUR


def withdraw(data):
    """
    Make an order to sell BTC
    Args:
        data (pandas DataFrame) : The last 600+ candle
    Return: Anything
    """
    balanceBTC = client.get_asset_balance(asset='BTC')
    totalBTC = float(balanceBTC['free'])
    order = client.order_market_sell(
        symbol='BTCEUR',
        quantity=totalBTC)
    print('Sell BTC')


if __name__ == '__main__':
    moneyInvest = 0
    onMarket = False
    while True:
        data = getHistoricalData()
        data = clearData(data)
        createIndicator(data)
        if checkEntryTrade(data, onMarket):
            moneyInvest = invest(data)
            onMarket = True
        if checkExitTrade(data, moneyInvest, onMarket):
            withdraw(data)
            onMarket = False
        print("Check for the hour data, sleep for 1h")

        sleep(3600)
