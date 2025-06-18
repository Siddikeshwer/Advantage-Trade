import pandas as pd
import numpy as np
import yfinance as yf
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def get_stock_data(symbol, period='1y'):
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_technical_indicators(df):
    """
    Calculate various technical indicators for the given stock data
    """
    if df is None or df.empty:
        return None
    
    # Calculate RSI
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    
    # Calculate MACD
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Histogram'] = macd.macd_diff()
    
    # Calculate Moving Averages
    sma_20 = SMAIndicator(close=df['Close'], window=20)
    sma_50 = SMAIndicator(close=df['Close'], window=50)
    df['SMA_20'] = sma_20.sma_indicator()
    df['SMA_50'] = sma_50.sma_indicator()
    
    # Calculate Bollinger Bands
    bb = BollingerBands(close=df['Close'])
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Lower'] = bb.bollinger_lband()
    df['BB_Middle'] = bb.bollinger_mavg()
    
    return df

def get_trading_signals(df):
    """
    Generate trading signals based on technical indicators
    """
    if df is None or df.empty:
        return None
    
    signals = {
        'RSI_Signal': 'Neutral',
        'MACD_Signal': 'Neutral',
        'MA_Signal': 'Neutral',
        'BB_Signal': 'Neutral'
    }
    
    # RSI Signals
    last_rsi = df['RSI'].iloc[-1]
    if last_rsi > 70:
        signals['RSI_Signal'] = 'Overbought'
    elif last_rsi < 30:
        signals['RSI_Signal'] = 'Oversold'
    
    # MACD Signals
    if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]:
        signals['MACD_Signal'] = 'Bullish'
    else:
        signals['MACD_Signal'] = 'Bearish'
    
    # Moving Average Signals
    if df['Close'].iloc[-1] > df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1]:
        signals['MA_Signal'] = 'Bullish'
    elif df['Close'].iloc[-1] < df['SMA_20'].iloc[-1] < df['SMA_50'].iloc[-1]:
        signals['MA_Signal'] = 'Bearish'
    
    # Bollinger Bands Signals
    if df['Close'].iloc[-1] > df['BB_Upper'].iloc[-1]:
        signals['BB_Signal'] = 'Overbought'
    elif df['Close'].iloc[-1] < df['BB_Lower'].iloc[-1]:
        signals['BB_Signal'] = 'Oversold'
    
    return signals

def analyze_stock(symbol):
    """
    Perform complete technical analysis for a stock
    """
    # Get stock data
    df = get_stock_data(symbol)
    if df is None:
        return None
    
    # Calculate indicators
    df = calculate_technical_indicators(df)
    if df is None:
        return None
    
    # Get trading signals
    signals = get_trading_signals(df)
    
    # Calculate additional metrics
    volatility = df['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
    returns = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100  # Total return
    
    analysis = {
        'symbol': symbol,
        'current_price': df['Close'].iloc[-1],
        'signals': signals,
        'volatility': volatility,
        'returns': returns,
        'technical_data': df
    }
    
    return analysis 