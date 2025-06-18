import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import time

def format_currency(value):
    """
    Format number as currency
    """
    return f"${value:,.2f}"

def format_percentage(value):
    """
    Format number as percentage
    """
    return f"{value:.2f}%"

def get_market_status():
    """
    Check if market is open
    """
    try:
        # Get SPY data to check market status
        spy = yf.Ticker("SPY")
        info = spy.info
        return info['regularMarketPrice'] is not None
    except:
        return False

def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """
    Retry a function with exponential backoff
    """
    retries = 0
    delay = initial_delay
    
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries == max_retries:
                raise e
            time.sleep(delay)
            delay *= 2

def fetch_webpage(url, headers=None):
    """
    Fetch webpage content with error handling
    """
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def parse_html_table(html, table_class=None):
    """
    Parse HTML table into pandas DataFrame
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        if table_class:
            table = soup.find('table', class_=table_class)
        else:
            table = soup.find('table')
        
        if table:
            return pd.read_html(str(table))[0]
        return None
    except Exception as e:
        print(f"Error parsing table: {str(e)}")
        return None

def calculate_returns(prices):
    """
    Calculate returns from price series
    """
    returns = prices.pct_change()
    return returns

def calculate_volatility(returns, window=252):
    """
    Calculate rolling volatility
    """
    return returns.rolling(window=window).std() * np.sqrt(252)

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio
    """
    excess_returns = returns - risk_free_rate/252
    return np.sqrt(252) * excess_returns.mean() / returns.std()

def get_trading_days(start_date, end_date=None):
    """
    Get list of trading days between dates
    """
    if end_date is None:
        end_date = datetime.now()
    
    # Get SPY data for trading days
    spy = yf.Ticker("SPY")
    hist = spy.history(start=start_date, end=end_date)
    return hist.index.tolist()

def format_timestamp(timestamp):
    """
    Format timestamp for display
    """
    if isinstance(timestamp, str):
        timestamp = pd.to_datetime(timestamp)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def calculate_drawdown(returns):
    """
    Calculate drawdown series
    """
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative / running_max) - 1
    return drawdown

def calculate_max_drawdown(returns):
    """
    Calculate maximum drawdown
    """
    drawdown = calculate_drawdown(returns)
    return drawdown.min()

def calculate_calmar_ratio(returns, window=252):
    """
    Calculate Calmar ratio
    """
    annual_return = returns.mean() * 252
    max_drawdown = calculate_max_drawdown(returns)
    return annual_return / abs(max_drawdown) if max_drawdown != 0 else 0 