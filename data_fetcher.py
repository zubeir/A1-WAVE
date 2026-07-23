"""
Data fetching module for A1-WAVE Dashboard
Handles Yahoo Finance data and news sentiment analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_market_data(self, tickers: List[str], period: str = "3mo") -> Dict[str, pd.DataFrame]:
        """
        Fetch market data for given tickers
        
        Args:
            tickers: List of ticker symbols
            period: Time period (1mo, 3mo, 6mo, 1y, etc.)
            
        Returns:
            Dictionary with ticker as key and DataFrame as value
        """
        try:
            data = {}
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                df = stock.history(period=period)
                if not df.empty:
                    data[ticker] = df
                else:
                    logger.warning(f"No data found for {ticker}")
            return data
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return {}
    
    def get_ticker_info(self, ticker: str) -> Dict:
        """Get basic ticker information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return {'name': ticker, 'sector': 'Unknown', 'market_cap': 0, 'currency': 'USD'}
    
    def calculate_returns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate various return metrics including MTD and 6-month"""
        if df.empty or len(df) < 20:
            return {}
        
        current_price = df['Close'].iloc[-1]
        
        # 1 month return (approximately 21 trading days)
        if len(df) >= 21:
            month_ago_price = df['Close'].iloc[-21]
            one_month_return = (current_price - month_ago_price) / month_ago_price
        else:
            one_month_return = 0
        
        # 3 month return (approximately 63 trading days)
        if len(df) >= 63:
            three_month_ago_price = df['Close'].iloc[-63]
            three_month_return = (current_price - three_month_ago_price) / three_month_ago_price
        else:
            three_month_ago_price = df['Close'].iloc[0]
            three_month_return = (current_price - three_month_ago_price) / three_month_ago_price
        
        # 6 month return (approximately 126 trading days)
        if len(df) >= 126:
            six_month_ago_price = df['Close'].iloc[-126]
            six_month_return = (current_price - six_month_ago_price) / six_month_ago_price
        else:
            six_month_ago_price = df['Close'].iloc[0]
            six_month_return = (current_price - six_month_ago_price) / six_month_ago_price
        
        # MTD (Month-to-Date) return
        current_date = df.index[-1]
        month_start = current_date.replace(day=1)
        
        # Find the first trading day of current month
        month_start_data = df[df.index >= month_start]
        if not month_start_data.empty:
            month_start_price = month_start_data['Close'].iloc[0]
            mtd_return = (current_price - month_start_price) / month_start_price
            logger.info(f"MTD calculation for {current_date.date()}: Current={current_price:.2f}, Month Start={month_start_price:.2f}, MTD={mtd_return:.2%}")
        else:
            mtd_return = 0
            logger.warning(f"No month start data found for {current_date.date()}")
        
        return {
            'one_month_return': one_month_return,
            'three_month_return': three_month_return,
            'six_month_return': six_month_return,
            'mtd_return': mtd_return,
            'current_price': current_price
        }
    
    def calculate_moving_averages(self, df: pd.DataFrame, periods: List[int] = [20, 50]) -> Dict[str, float]:
        """Calculate moving averages and current price relationship"""
        if df.empty:
            return {}
        
        current_price = df['Close'].iloc[-1]
        ma_data = {}
        
        for period in periods:
            if len(df) >= period:
                ma = df['Close'].rolling(window=period).mean().iloc[-1]
                ma_data[f'ma_{period}'] = ma
                ma_data[f'price_vs_ma_{period}'] = (current_price - ma) / ma
            else:
                ma_data[f'ma_{period}'] = current_price
                ma_data[f'price_vs_ma_{period}'] = 0
        
        return ma_data
    
    def analyze_volume_profile(self, df: pd.DataFrame, days: int = 10) -> Dict[str, str]:
        """Analyze volume profile over recent days"""
        if df.empty or len(df) < days:
            return {'volume_profile': 'Insufficient data', 'volume_trend': 'Unknown'}
        
        recent_df = df.tail(days)
        
        # Calculate up vs down volume
        up_days = recent_df[recent_df['Close'] > recent_df['Open']]
        down_days = recent_df[recent_df['Close'] < recent_df['Open']]
        
        avg_up_volume = up_days['Volume'].mean() if not up_days.empty else 0
        avg_down_volume = down_days['Volume'].mean() if not down_days.empty else 0
        
        total_volume = recent_df['Volume'].mean()
        
        # Determine volume profile
        if avg_up_volume > avg_down_volume * 1.2:
            profile = "Accumulation"
            trend = "Strong"
        elif avg_down_volume > avg_up_volume * 1.2:
            profile = "Distribution"
            trend = "Weak"
        else:
            profile = "Mixed"
            trend = "Neutral"
        
        return {
            'volume_profile': profile,
            'volume_trend': trend,
            'avg_volume': total_volume,
            'up_volume_ratio': avg_up_volume / (avg_down_volume + 1e-6)
        }
    
    def get_news_sentiment(self, ticker: str, days_back: int = 7) -> Dict[str, str]:
        """
        Get news sentiment for a ticker using free RSS feeds
        Returns basic sentiment analysis based on news headlines
        """
        try:
            # Yahoo Finance RSS feed
            rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
            
            feed = feedparser.parse(rss_url)
            headlines = [entry.title for entry in feed.entries[:10]]  # Last 10 headlines
            articles = []
            
            for entry in feed.entries[:5]:  # Get full content for top 5 articles
                articles.append({
                    'title': entry.title,
                    'summary': entry.summary if hasattr(entry, 'summary') else entry.title,
                    'published': entry.published if hasattr(entry, 'published') else '',
                    'link': entry.link if hasattr(entry, 'link') else ''
                })
            
            if not headlines:
                return {'sentiment': 'Neutral', 'catalyst_status': 'Stable', 'news_count': 0, 'articles': []}
            
            # Simple sentiment analysis based on keywords
            positive_words = ['up', 'rise', 'gain', 'growth', 'strong', 'beat', 'win', 'bull', 'buy', 'positive', 'breakthrough', 'partnership']
            negative_words = ['down', 'fall', 'drop', 'loss', 'weak', 'miss', 'bear', 'sell', 'cut', 'negative', 'concern', 'risk', 'decline']
            
            positive_count = sum(1 for headline in headlines 
                               for word in positive_words if word.lower() in headline.lower())
            negative_count = sum(1 for headline in headlines 
                               for word in negative_words if word.lower() in headline.lower())
            
            # Determine sentiment
            if positive_count > negative_count * 1.5:
                sentiment = "Positive"
                catalyst = "Active"
            elif negative_count > positive_count * 1.5:
                sentiment = "Negative" 
                catalyst = "Fading"
            else:
                sentiment = "Neutral"
                catalyst = "Stable"
            
            # Generate AI-like summary
            summary = self.generate_news_summary(ticker, articles, sentiment)
            
            return {
                'sentiment': sentiment,
                'catalyst_status': catalyst,
                'news_count': len(headlines),
                'positive_mentions': positive_count,
                'negative_mentions': negative_count,
                'articles': articles,
                'summary': summary
            }
            
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return {'sentiment': 'Neutral', 'catalyst_status': 'Stable', 'news_count': 0, 'articles': [], 'summary': ''}
    
    def generate_news_summary(self, ticker: str, articles: list, sentiment: str) -> str:
        """
        Generate an AI-like summary of news articles with decision guidance
        """
        if not articles:
            return "No recent news available."
        
        try:
            # Extract key themes and topics
            all_text = " ".join([article['title'] + " " + article['summary'] for article in articles])
            
            # Common financial themes to look for
            themes = {
                'earnings': ['earnings', 'revenue', 'profit', 'eps', 'quarterly'],
                'partnership': ['partnership', 'deal', 'agreement', 'collaboration', 'joint'],
                'regulation': ['regulation', 'fda', 'approval', 'compliance', 'legal'],
                'technology': ['technology', 'innovation', 'patent', 'breakthrough', 'ai'],
                'market': ['market', 'stock', 'shares', 'trading', 'volume'],
                'expansion': ['expansion', 'growth', 'new', 'launch', 'open'],
                'risk': ['risk', 'concern', 'warning', 'challenge', 'difficulty']
            }
            
            detected_themes = []
            for theme, keywords in themes.items():
                if any(keyword in all_text.lower() for keyword in keywords):
                    detected_themes.append(theme)
            
            # Build comprehensive summary
            summary_parts = []
            
            # Sentiment overview with emoji
            if sentiment == "Positive":
                summary_parts.append(f"🟢 **Bullish Sentiment** - Recent news for {ticker} is predominantly positive with several favorable developments driving momentum.")
            elif sentiment == "Negative":
                summary_parts.append(f"🔴 **Bearish Sentiment** - {ticker} is facing challenges based on recent news coverage with several concerning reports creating headwinds.")
            else:
                summary_parts.append(f"🟡 **Neutral Sentiment** - Recent news for {ticker} shows mixed sentiment with balanced coverage lacking clear directional bias.")
            
            # Key themes with detailed analysis
            if detected_themes:
                theme_analysis = {
                    'earnings': '💰 **Financial Performance** - Strong earnings results and revenue growth indicate solid business fundamentals',
                    'partnership': '🤝 **Strategic Partnerships** - New business agreements and collaborations suggest expansion opportunities',
                    'regulation': '⚖️ **Regulatory Developments** - Compliance matters and approvals could impact operations',
                    'technology': '🚀 **Technology Innovation** - Breakthrough developments and patents indicate competitive advantages',
                    'market': '📊 **Market Dynamics** - Trading activity and market sentiment suggest investor interest',
                    'expansion': '📈 **Business Expansion** - Growth initiatives and new market penetration indicate scaling efforts',
                    'risk': '⚠️ **Risk Factors** - Identified challenges and concerns require careful monitoring'
                }
                
                for theme in detected_themes[:3]:
                    if theme in theme_analysis:
                        summary_parts.append(theme_analysis[theme])
            
            # Decision guidance based on sentiment and themes
            summary_parts.append("\n---")
            summary_parts.append("## 🎯 **Trading Decision Guidance**")
            
            if sentiment == "Positive":
                if 'earnings' in detected_themes:
                    summary_parts.append("✅ **CONSIDER ADDING** - Strong earnings combined with positive news suggest upward momentum")
                elif 'technology' in detected_themes:
                    summary_parts.append("✅ **GROWTH POTENTIAL** - Innovation breakthroughs could drive long-term value")
                else:
                    summary_parts.append("✅ **BULLISH BIAS** - Positive news flow supports position accumulation or holding")
            
            elif sentiment == "Negative":
                if 'regulation' in detected_themes:
                    summary_parts.append("⚠️ **RISK MANAGEMENT** - Regulatory concerns suggest defensive positioning")
                elif 'risk' in detected_themes:
                    summary_parts.append("🛑 **REDUCE EXPOSURE** - Multiple risk factors warrant position reduction")
                else:
                    summary_parts.append("⚠️ **CAUTIOUS STANCE** - Negative sentiment suggests waiting for clearer signals")
            
            else:  # Neutral
                if 'partnership' in detected_themes or 'expansion' in detected_themes:
                    summary_parts.append("🟡 **MONITOR CATALYSTS** - Neutral news with positive developments could trigger breakout")
                else:
                    summary_parts.append("⏸️ **WAIT-AND-SEE** - Mixed sentiment suggests holding current positions until clearer trend emerges")
            
            # Key takeaway summary
            summary_parts.append("\n---")
            summary_parts.append("## 📋 **Key Takeaways**")
            
            if len(articles) >= 3:
                summary_parts.append(f"• **High News Activity** - {len(articles)} recent articles indicate active market interest and ongoing developments")
            
            if sentiment == "Positive":
                summary_parts.append("• **Momentum Support** - News flow supports potential price appreciation and continued upward movement")
            elif sentiment == "Negative":
                summary_parts.append("• **Caution Warranted** - Negative developments may pressure prices and increase volatility")
            else:
                summary_parts.append("• **Neutral Bias** - Balanced coverage suggests waiting for definitive directional signals")
            
            # Action recommendation
            summary_parts.append("\n---")
            summary_parts.append("## 🎬 **Recommended Action**")
            
            if sentiment == "Positive":
                summary_parts.append("🟢 **POSITION ACCUMULATION** - Consider adding to positions on any pullbacks, maintain core holdings")
            elif sentiment == "Negative":
                summary_parts.append("🔴 **RISK REDUCTION** - Tighten stops, reduce exposure, prepare for potential rotation")
            else:
                summary_parts.append("🟡 **MAINTAIN STATUS** - Hold current positions, monitor for confirming signals before making changes")
            
            return "\n\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error generating news summary: {e}")
            return f"Recent news coverage for {ticker} shows {sentiment.lower()} sentiment with {len(articles)} articles."
    
    def get_macro_indicators(self) -> Dict[str, Dict]:
        """Get macro indicators (SPY, VIX, etc.)"""
        from config import MARKET_INDICATORS
        
        macro_data = {}
        tickers = list(MARKET_INDICATORS.values())
        
        try:
            data = self.get_market_data(tickers, period="1mo")
            
            for key, ticker in MARKET_INDICATORS.items():
                if ticker in data:
                    df = data[ticker]
                    if not df.empty:
                        current_price = df['Close'].iloc[-1]
                        
                        # Calculate returns
                        returns = self.calculate_returns(df)
                        
                        # Moving averages for trend
                        ma_data = self.calculate_moving_averages(df, [20])
                        
                        macro_data[key] = {
                            'ticker': ticker,
                            'current_price': current_price,
                            'one_month_return': returns.get('one_month_return', 0),
                            'price_vs_ma_20': ma_data.get('price_vs_ma_20', 0),
                            'trend': 'Up' if ma_data.get('price_vs_ma_20', 0) > 0.02 else 'Down' if ma_data.get('price_vs_ma_20', 0) < -0.02 else 'Flat'
                        }
                        
                        # Special handling for VIX
                        if ticker == "^VIX":
                            macro_data[key]['level'] = 'Low' if current_price < 20 else 'Medium' if current_price < 30 else 'High'
                        
        except Exception as e:
            logger.error(f"Error fetching macro indicators: {e}")
        
        return macro_data
