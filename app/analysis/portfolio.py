import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from config import RISK_LEVELS, INVESTMENT_HORIZONS, SECTORS

def get_sector_performance():
    """
    Get performance metrics for different sectors
    """
    sector_etfs = {
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
    
    performance = {}
    for sector, etf in sector_etfs.items():
        try:
            data = yf.download(etf, period='1y')
            if data.empty:
                raise ValueError(f"No data available for {sector}")
                
            returns = (data['Close'][-1] / data['Close'][0] - 1) * 100
            volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
            
            # Ensure we have valid numbers
            if np.isnan(returns) or np.isnan(volatility):
                raise ValueError(f"Invalid data for {sector}")
                
            performance[sector] = {
                'returns': float(returns),
                'volatility': float(volatility),
                'sharpe_ratio': float(returns / volatility if volatility != 0 else 0)
            }
        except Exception as e:
            print(f"Error fetching data for {sector}: {str(e)}")
            # Provide default values that won't cause issues
            performance[sector] = {
                'returns': 0.0,
                'volatility': 1.0,  # Use 1.0 instead of 0 to avoid division by zero
                'sharpe_ratio': 0.0
            }
    
    # Ensure we have at least one valid sector
    if not performance:
        # Provide default values for all sectors
        for sector in sector_etfs.keys():
            performance[sector] = {
                'returns': 0.0,
                'volatility': 1.0,
                'sharpe_ratio': 0.0
            }
    
    return performance

def calculate_asset_correlation():
    """
    Calculate correlation between different asset classes
    """
    assets = {
        'SPY': 'Equity',
        'GLD': 'Gold',
        'TLT': 'Bonds',
        'UUP': 'USD',
        'DBC': 'Commodities'
    }
    
    # Get historical data
    data = pd.DataFrame()
    valid_assets = []
    
    for symbol in assets.keys():
        try:
            prices = yf.download(symbol, period='1y')['Close']
            if not prices.empty and not prices.isna().all():
                data[symbol] = prices
                valid_assets.append(symbol)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
    
    # If we have no valid data, return a default correlation matrix
    if data.empty or len(valid_assets) < 2:
        default_corr = pd.DataFrame(
            np.eye(len(assets)),  # Identity matrix (no correlation)
            index=assets.keys(),
            columns=assets.keys()
        )
        return default_corr
    
    # Calculate correlation
    try:
        correlation = data.pct_change().corr()
        # Fill any NaN values with 0 (no correlation)
        correlation = correlation.fillna(0)
        return correlation
    except Exception as e:
        print(f"Error calculating correlation: {str(e)}")
        # Return default correlation matrix if calculation fails
        return pd.DataFrame(
            np.eye(len(assets)),
            index=assets.keys(),
            columns=assets.keys()
        )

def generate_portfolio_suggestions(capital, risk_level, investment_horizon, preferred_sectors):
    """
    Generate portfolio allocation suggestions based on user preferences
    """
    try:
        # Get market data
        sector_performance = get_sector_performance()
        asset_correlation = calculate_asset_correlation()
        
        # Get base allocation from risk level
        base_allocation = RISK_LEVELS[risk_level].copy()
        
        # Adjust allocation based on investment horizon
        horizon_months = INVESTMENT_HORIZONS[investment_horizon]['months']
        if horizon_months <= 3:  # Short term
            base_allocation['equity_allocation'] *= 0.8
            base_allocation['fixed_income_allocation'] *= 1.2
        elif horizon_months >= 60:  # Long term
            base_allocation['equity_allocation'] *= 1.2
            base_allocation['fixed_income_allocation'] *= 0.8
        
        # Calculate sector weights within equity allocation
        sector_weights = {}
        total_weight = 0
        
        # If no sectors are selected, use all sectors
        if not preferred_sectors:
            preferred_sectors = SECTORS
        
        for sector in preferred_sectors:
            if sector in sector_performance:
                # Weight based on Sharpe ratio and recent performance
                performance = sector_performance[sector]
                weight = (performance['sharpe_ratio'] + 1) * (1 + performance['returns'] / 100)
                sector_weights[sector] = max(weight, 0)  # Ensure non-negative weights
                total_weight += sector_weights[sector]
        
        # If no valid weights were calculated, use equal weights
        if total_weight == 0:
            for sector in preferred_sectors:
                sector_weights[sector] = 1.0 / len(preferred_sectors)
        else:
            # Normalize sector weights
            for sector in sector_weights:
                sector_weights[sector] = sector_weights[sector] / total_weight
        
        # Calculate final allocation
        allocation = {
            'equity': base_allocation['equity_allocation'],
            'commodities': base_allocation['commodities_allocation'],
            'forex': base_allocation['forex_allocation'],
            'fixed_income': base_allocation['fixed_income_allocation']
        }
        
        # Add sector breakdown
        sector_allocation = {}
        for sector, weight in sector_weights.items():
            sector_allocation[sector] = weight * allocation['equity']
        
        # Generate recommendations
        recommendations = {
            'allocation': allocation,
            'sector_breakdown': sector_allocation,
            'total_capital': capital,
            'risk_level': risk_level,
            'investment_horizon': investment_horizon,
            'market_analysis': {
                'sector_performance': sector_performance,
                'asset_correlation': asset_correlation
            }
        }
        
        return recommendations
        
    except Exception as e:
        print(f"Error generating portfolio suggestions: {str(e)}")
        # Return a default portfolio if something goes wrong
        return {
            'allocation': {
                'equity': 0.4,
                'commodities': 0.2,
                'forex': 0.2,
                'fixed_income': 0.2
            },
            'sector_breakdown': {sector: 0.1 for sector in SECTORS},
            'total_capital': capital,
            'risk_level': risk_level,
            'investment_horizon': investment_horizon,
            'market_analysis': {
                'sector_performance': {sector: {'returns': 0, 'volatility': 1, 'sharpe_ratio': 0} for sector in SECTORS},
                'asset_correlation': pd.DataFrame(np.eye(5), index=['SPY', 'GLD', 'TLT', 'UUP', 'DBC'], columns=['SPY', 'GLD', 'TLT', 'UUP', 'DBC'])
            }
        }

def calculate_portfolio_metrics(portfolio):
    """
    Calculate key portfolio metrics
    """
    allocation = portfolio['allocation']
    market_analysis = portfolio['market_analysis']
    
    # Calculate expected return
    expected_return = 0
    for asset, weight in allocation.items():
        if asset in market_analysis['sector_performance']:
            expected_return += weight * market_analysis['sector_performance'][asset]['returns']
    
    # Calculate portfolio volatility
    volatility = 0
    for asset1, weight1 in allocation.items():
        for asset2, weight2 in allocation.items():
            if asset1 in market_analysis['asset_correlation'] and asset2 in market_analysis['asset_correlation']:
                corr = market_analysis['asset_correlation'].loc[asset1, asset2]
                vol1 = market_analysis['sector_performance'][asset1]['volatility'] if asset1 in market_analysis['sector_performance'] else 0
                vol2 = market_analysis['sector_performance'][asset2]['volatility'] if asset2 in market_analysis['sector_performance'] else 0
                volatility += weight1 * weight2 * corr * vol1 * vol2
    
    volatility = np.sqrt(volatility)
    
    # Calculate Sharpe ratio
    risk_free_rate = 0.02  # Assuming 2% risk-free rate
    sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility != 0 else 0
    
    return {
        'expected_return': expected_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    } 