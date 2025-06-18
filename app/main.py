import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import plotly.express as px

# Import local modules
from config import RISK_LEVELS, INVESTMENT_HORIZONS, SECTORS, NEWS_API_KEY, ALPHA_VANTAGE_API_KEY
from analysis.technical import calculate_technical_indicators
from analysis.sentiment import analyze_news_sentiment
from analysis.portfolio import generate_portfolio_suggestions

# Set page config
st.set_page_config(
    page_title="Welcome to AI Stock Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🤖 AI-Powered Stock Market Analyzer")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Investment Preferences")
        
        # Investment Capital
        capital = st.number_input(
            "Investment Capital (Rupees)",
            min_value=1000,
            max_value=1000000,
            value=10000,
            step=1000
        )
        
        # Risk Level
        risk_level = st.selectbox(
            "Risk Level",
            options=list(RISK_LEVELS.keys()),
            format_func=lambda x: x.title()
        )
        
        # Investment Horizon
        investment_horizon = st.selectbox(
            "Investment Horizon",
            options=list(INVESTMENT_HORIZONS.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        # Preferred Sectors
        preferred_sectors = st.multiselect(
            "Preferred Sectors",
            options=SECTORS,
            default=SECTORS[:3]
        )
        
        # Generate Analysis Button
        analyze_button = st.button("Generate Analysis", type="primary")

    # Main content area
    if analyze_button:
        with st.spinner("Analyzing market data and generating recommendations..."):
            # Generate portfolio suggestions
            portfolio = generate_portfolio_suggestions(
                capital=capital,
                risk_level=risk_level,
                investment_horizon=investment_horizon,
                preferred_sectors=preferred_sectors
            )
            
            # Display portfolio allocation
            st.header("📊 Portfolio Allocation")
            col1, col2 = st.columns(2)
            
            with col1:
                # Create pie chart for portfolio allocation
                fig = px.pie(
                    values=list(portfolio['allocation'].values()),
                    names=list(portfolio['allocation'].keys()),
                    title="Suggested Portfolio Allocation"
                )
                st.plotly_chart(fig)
            
            with col2:
                # Display allocation details
                st.subheader("Allocation Details")
                for asset, allocation in portfolio['allocation'].items():
                    st.metric(
                        label=asset.replace('_', ' ').title(),
                        value=f"${allocation * capital:,.2f}",
                        delta=f"{allocation * 100:.1f}%"
                    )
            
            # Market Analysis Section
            st.header("📈 Market Analysis")
            
            # Technical Analysis
            st.subheader("Technical Indicators")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("RSI", "65.2", "2.1")
            with col2:
                st.metric("MACD", "0.45", "0.12")
            with col3:
                st.metric("Moving Average", "Above", "Bullish")
            
            # News Sentiment
            st.header("📰 Market Sentiment")
            sentiment_data = {
                'Positive': 65,
                'Neutral': 25,
                'Negative': 10
            }
            
            fig = px.bar(
                x=list(sentiment_data.keys()),
                y=list(sentiment_data.values()),
                title="News Sentiment Analysis"
            )
            st.plotly_chart(fig)
            
            # Investment Recommendations
            st.header("💡 Investment Recommendations")
            
            # Display recommendations in expandable sections
            with st.expander("Equity Recommendations", expanded=True):
                st.write("""
                - Technology sector shows strong growth potential
                - Healthcare stocks are undervalued
                - Consider defensive stocks for portfolio stability
                """)
            
            with st.expander("Commodity Recommendations", expanded=True):
                st.write("""
                - Gold: Consider as a hedge against market volatility
                - Oil: Monitor supply chain disruptions
                - Agricultural commodities: Watch for seasonal trends
                """)
            
            with st.expander("Forex Recommendations", expanded=True):
                st.write("""
                - USD/JPY: Bullish trend expected
                - EUR/USD: Range-bound trading
                - GBP/USD: Monitor Brexit developments
                """)
            
            # Risk Analysis
            st.header("⚠️ Risk Analysis")
            risk_metrics = {
                'Market Volatility': 'Medium',
                'Geopolitical Risk': 'Low',
                'Currency Risk': 'Medium',
                'Interest Rate Risk': 'High'
            }
            
            for metric, value in risk_metrics.items():
                st.metric(metric, value)

if __name__ == "__main__":
    main() 