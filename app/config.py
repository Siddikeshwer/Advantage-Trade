import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'Ypt6THq45kRxL9oAGO20NLUM9jYYruyS')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '6CB73NPE4ZL1K3KX')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./stock_analyzer.db')

# Scraping Configuration
SCRAPING_INTERVAL = 3600  # 1 hour in seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# News Sources
NEWS_SOURCES = [
    'reuters.com',
    'bloomberg.com',
    'moneycontrol.com'
]

# Market Data Sources
MARKET_DATA_SOURCES = {
    'stocks': 'yahoo',
    'forex': 'alpha_vantage',
    'commodities': 'investing.com'
}

# Technical Analysis Parameters
TECHNICAL_INDICATORS = {
    'RSI': {'period': 14},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
    'SMA': {'short': 20, 'long': 50},
    'EMA': {'short': 20, 'long': 50}
}

# Risk Levels
RISK_LEVELS = {
    'LOW': {
        'equity_allocation': 0.3,
        'commodities_allocation': 0.2,
        'forex_allocation': 0.2,
        'fixed_income_allocation': 0.3
    },
    'MEDIUM': {
        'equity_allocation': 0.5,
        'commodities_allocation': 0.2,
        'forex_allocation': 0.2,
        'fixed_income_allocation': 0.1
    },
    'HIGH': {
        'equity_allocation': 0.7,
        'commodities_allocation': 0.15,
        'forex_allocation': 0.15,
        'fixed_income_allocation': 0.0
    }
}

# Investment Horizons
INVESTMENT_HORIZONS = {
    'SHORT_TERM': {'months': 3},
    'MEDIUM_TERM': {'months': 12},
    'LONG_TERM': {'months': 60}
}

# Sectors
SECTORS = [
    'Technology',
    'Healthcare',
    'Finance',
    'Energy',
    'Consumer Goods',
    'Industrial',
    'Materials',
    'Utilities',
    'Real Estate',
    'Communication Services'
] 