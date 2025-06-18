# API Endpoints
YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
NEWS_API_BASE_URL = "https://newsapi.org/v2"

# Market Data
MARKET_INDICES = {
    'S&P 500': '^GSPC',
    'Dow Jones': '^DJI',
    'NASDAQ': '^IXIC',
    'Russell 2000': '^RUT'
}

# Sector ETFs
SECTOR_ETFS = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Finance': 'XLF',
    'Energy': 'XLE',
    'Consumer Goods': 'XLP',
    'Industrial': 'XLI',
    'Materials': 'XLB',
    'Utilities': 'XLU',
    'Real Estate': 'XLRE',
    'Communication Services': 'XLC'
}

# Commodity Symbols
COMMODITY_SYMBOLS = {
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Crude Oil': 'CL=F',
    'Natural Gas': 'NG=F',
    'Copper': 'HG=F',
    'Platinum': 'PL=F',
    'Palladium': 'PA=F'
}

# Currency Pairs
FOREX_PAIRS = {
    'EUR/USD': 'EURUSD=X',
    'GBP/USD': 'GBPUSD=X',
    'USD/JPY': 'USDJPY=X',
    'USD/CHF': 'USDCHF=X',
    'AUD/USD': 'AUDUSD=X',
    'USD/CAD': 'USDCAD=X'
}

# Technical Indicators
TECHNICAL_INDICATORS = {
    'RSI': {
        'name': 'Relative Strength Index',
        'default_period': 14,
        'overbought': 70,
        'oversold': 30
    },
    'MACD': {
        'name': 'Moving Average Convergence Divergence',
        'fast_period': 12,
        'slow_period': 26,
        'signal_period': 9
    },
    'SMA': {
        'name': 'Simple Moving Average',
        'short_period': 20,
        'long_period': 50
    },
    'EMA': {
        'name': 'Exponential Moving Average',
        'short_period': 20,
        'long_period': 50
    },
    'BB': {
        'name': 'Bollinger Bands',
        'period': 20,
        'std_dev': 2
    }
}

# Risk Levels
RISK_LEVELS = {
    'LOW': {
        'max_equity_allocation': 0.3,
        'max_commodity_allocation': 0.2,
        'max_forex_allocation': 0.2,
        'min_fixed_income_allocation': 0.3
    },
    'MEDIUM': {
        'max_equity_allocation': 0.5,
        'max_commodity_allocation': 0.2,
        'max_forex_allocation': 0.2,
        'min_fixed_income_allocation': 0.1
    },
    'HIGH': {
        'max_equity_allocation': 0.7,
        'max_commodity_allocation': 0.15,
        'max_forex_allocation': 0.15,
        'min_fixed_income_allocation': 0.0
    }
}

# Investment Horizons
INVESTMENT_HORIZONS = {
    'SHORT_TERM': {
        'months': 3,
        'max_equity_allocation': 0.4,
        'min_fixed_income_allocation': 0.3
    },
    'MEDIUM_TERM': {
        'months': 12,
        'max_equity_allocation': 0.6,
        'min_fixed_income_allocation': 0.2
    },
    'LONG_TERM': {
        'months': 60,
        'max_equity_allocation': 0.8,
        'min_fixed_income_allocation': 0.1
    }
}

# News Sources
NEWS_SOURCES = [
    'reuters.com',
    'bloomberg.com',
    'moneycontrol.com',
    'cnbc.com',
    'wsj.com',
    'ft.com'
]

# Market Hours (EST)
MARKET_HOURS = {
    'pre_market': {
        'start': '04:00',
        'end': '09:30'
    },
    'regular': {
        'start': '09:30',
        'end': '16:00'
    },
    'after_hours': {
        'start': '16:00',
        'end': '20:00'
    }
}

# Error Messages
ERROR_MESSAGES = {
    'API_ERROR': 'Error fetching data from API',
    'NETWORK_ERROR': 'Network connection error',
    'INVALID_SYMBOL': 'Invalid symbol provided',
    'RATE_LIMIT': 'API rate limit exceeded',
    'DATA_NOT_FOUND': 'Requested data not found'
}

# Cache Settings
CACHE_SETTINGS = {
    'market_data': 300,  # 5 minutes
    'news_data': 900,    # 15 minutes
    'technical_indicators': 300,  # 5 minutes
    'portfolio_analysis': 3600  # 1 hour
} 