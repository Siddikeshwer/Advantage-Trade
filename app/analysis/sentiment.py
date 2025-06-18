import pandas as pd
import numpy as np
from newsapi import NewsApiClient
from transformers import pipeline
import spacy
from datetime import datetime, timedelta
from config import NEWS_API_KEY

# Initialize News API client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("Downloading spaCy model...")
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Initialize sentiment analyzer
sentiment_analyzer = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

def get_news_articles(query, days=7):
    """
    Fetch news articles related to the query
    """
    try:
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        articles = newsapi.get_everything(
            q=query,
            from_param=from_date,
            language='en',
            sort_by='relevancy'
        )
        return articles['articles']
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def analyze_text_sentiment(text):
    """
    Analyze sentiment of a given text using BERT
    """
    try:
        result = sentiment_analyzer(text)[0]
        return {
            'sentiment': result['label'],
            'score': result['score']
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return None

def extract_key_entities(text):
    """
    Extract key entities from text using spaCy
    """
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PERSON', 'GPE', 'MONEY']:
            entities.append({
                'text': ent.text,
                'label': ent.label_
            })
    return entities

def analyze_news_sentiment(query, days=7):
    """
    Perform complete news sentiment analysis
    """
    # Get news articles
    articles = get_news_articles(query, days)
    if not articles:
        return None
    
    # Analyze each article
    sentiment_results = []
    for article in articles:
        # Combine title and description for analysis
        text = f"{article['title']} {article['description']}"
        
        # Get sentiment
        sentiment = analyze_text_sentiment(text)
        if sentiment:
            # Extract entities
            entities = extract_key_entities(text)
            
            sentiment_results.append({
                'title': article['title'],
                'source': article['source']['name'],
                'published_at': article['publishedAt'],
                'sentiment': sentiment['sentiment'],
                'sentiment_score': sentiment['score'],
                'entities': entities,
                'url': article['url']
            })
    
    # Calculate aggregate sentiment
    if sentiment_results:
        sentiment_counts = pd.DataFrame(sentiment_results)['sentiment'].value_counts()
        total_articles = len(sentiment_results)
        
        sentiment_summary = {
            'positive': sentiment_counts.get('POS', 0) / total_articles * 100,
            'neutral': sentiment_counts.get('NEU', 0) / total_articles * 100,
            'negative': sentiment_counts.get('NEG', 0) / total_articles * 100,
            'articles': sentiment_results
        }
        
        return sentiment_summary
    
    return None

def get_market_sentiment():
    """
    Get overall market sentiment by analyzing multiple market-related queries
    """
    queries = [
        'stock market',
        'economy',
        'inflation',
        'interest rates',
        'federal reserve'
    ]
    
    all_sentiments = []
    for query in queries:
        sentiment = analyze_news_sentiment(query, days=3)
        if sentiment:
            all_sentiments.append(sentiment)
    
    if all_sentiments:
        # Calculate weighted average sentiment
        total_positive = sum(s['positive'] for s in all_sentiments)
        total_neutral = sum(s['neutral'] for s in all_sentiments)
        total_negative = sum(s['negative'] for s in all_sentiments)
        
        n = len(all_sentiments)
        return {
            'positive': total_positive / n,
            'neutral': total_neutral / n,
            'negative': total_negative / n,
            'overall_sentiment': 'positive' if total_positive > total_negative else 'negative'
        }
    
    return None 