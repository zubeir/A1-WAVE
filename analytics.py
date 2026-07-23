"""
Analytics module for A1-WAVE Dashboard
Implements scoring algorithms for velocity, trend, volume, and catalyst analysis
"""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
from data_fetcher import DataFetcher
from config import VELOCITY_THRESHOLDS, VOLUME_DAYS, MA_DAYS
import logging

logger = logging.getLogger(__name__)

class Analytics:
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def calculate_velocity_score(self, returns_data: Dict) -> Tuple[str, float]:
        """
        Calculate velocity score based on 1-month and 3-month returns
        
        Returns:
            Tuple of (score_label, score_value)
        """
        one_month = returns_data.get('one_month_return', 0)
        three_month = returns_data.get('three_month_return', 0)
        
        # Weighted average (3-month gets more weight)
        weighted_return = (one_month * 0.4 + three_month * 0.6)
        
        # Determine score
        if weighted_return >= VELOCITY_THRESHOLDS["strong"]:
            score = "Strong"
        elif weighted_return >= VELOCITY_THRESHOLDS["moderate"]:
            score = "Moderate"
        elif weighted_return >= VELOCITY_THRESHOLDS["weak"]:
            score = "Slowing"
        else:
            score = "Weak"
        
        return score, weighted_return
    
    def analyze_trend_structure(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Analyze trend structure based on moving averages and price action
        """
        if df.empty:
            return {'trend_structure': 'No Data', 'trend_strength': 'Unknown'}
        
        current_price = df['Close'].iloc[-1]
        ma_data = self.data_fetcher.calculate_moving_averages(df, MA_DAYS)
        
        ma_20 = ma_data.get('ma_20', current_price)
        ma_50 = ma_data.get('ma_50', current_price)
        
        # Determine trend structure
        if current_price > ma_20 > ma_50:
            structure = "HH/HL"  # Higher Highs, Higher Lows
            strength = "Strong Uptrend"
        elif current_price > ma_20:
            structure = "Above MA20"
            strength = "Uptrend"
        elif current_price > ma_50:
            structure = "Testing MA20"
            strength = "Flattening"
        elif current_price > ma_20 * 0.95:  # Within 5% of MA20
            structure = "Near MA20"
            strength = "Consolidating"
        else:
            structure = "LHL"  # Lower Highs, Lower Lows
            strength = "Breakdown"
        
        return {
            'trend_structure': structure,
            'trend_strength': strength,
            'price_vs_ma_20': ma_data.get('price_vs_ma_20', 0),
            'price_vs_ma_50': ma_data.get('price_vs_ma_50', 0)
        }
    
    def get_volume_analysis(self, df: pd.DataFrame) -> Dict[str, str]:
        """Get comprehensive volume analysis"""
        volume_data = self.data_fetcher.analyze_volume_profile(df, VOLUME_DAYS)
        
        # Map to dashboard terms
        profile_map = {
            "Accumulation": "Accum.",
            "Distribution": "Dist.",
            "Mixed": "Mixed"
        }
        
        return {
            'volume_profile': profile_map.get(volume_data['volume_profile'], volume_data['volume_profile']),
            'volume_trend': volume_data['volume_trend'],
            'avg_volume': volume_data.get('avg_volume', 0)
        }
    
    def get_catalyst_status(self, ticker: str) -> Dict[str, str]:
        """Get catalyst status from news sentiment"""
        news_data = self.data_fetcher.get_news_sentiment(ticker)
        
        return {
            'catalyst_status': news_data['catalyst_status'],
            'sentiment': news_data['sentiment'],
            'news_count': news_data['news_count'],
            'articles': news_data.get('articles', []),
            'summary': news_data.get('summary', '')
        }
    
    def classify_position(self, ticker: str, velocity_score: str, trend_strength: str, 
                        volume_profile: str, catalyst_status: str) -> str:
        """
        Classify position as GREEN, YELLOW, or RED based on all factors
        
        Args:
            ticker: Stock ticker
            velocity_score: Strong/Moderate/Slowing/Weak
            trend_strength: Trend strength description
            volume_profile: Accum./Dist./Mixed
            catalyst_status: Active/Stable/Fading
            
        Returns:
            Classification: 'GREEN', 'YELLOW', or 'RED'
        """
        # Scoring system
        green_score = 0
        yellow_score = 0
        red_score = 0
        
        # Velocity scoring
        if velocity_score == "Strong":
            green_score += 3
        elif velocity_score == "Moderate":
            green_score += 1
            yellow_score += 1
        elif velocity_score == "Slowing":
            yellow_score += 2
        else:  # Weak
            red_score += 3
        
        # Trend scoring
        if "Strong" in trend_strength or "Uptrend" in trend_strength:
            green_score += 2
        elif "Flattening" in trend_strength or "Consolidating" in trend_strength:
            yellow_score += 2
        else:  # Breakdown
            red_score += 2
        
        # Volume scoring
        if volume_profile == "Accum.":
            green_score += 1
        elif volume_profile == "Mixed":
            yellow_score += 1
        else:  # Dist.
            red_score += 1
        
        # Catalyst scoring
        if catalyst_status == "Active":
            green_score += 1
        elif catalyst_status == "Stable":
            yellow_score += 1
        else:  # Fading
            red_score += 1
        
        # Determine classification
        if green_score >= yellow_score and green_score >= red_score and green_score >= 4:
            return "GREEN"
        elif red_score >= green_score and red_score >= yellow_score and red_score >= 4:
            return "RED"
        else:
            return "YELLOW"
    
    def classify_tier(self, ticker: str, velocity_score: str, velocity_value: float, 
                   catalyst_status: str, volume_profile: str, trend_strength: str) -> str:
        """
        Classify position into Tier 1, Tier 2, or Tier 3 based on conviction level
        
        Args:
            ticker: Stock ticker
            velocity_score: Strong/Moderate/Slowing/Weak
            velocity_value: Actual velocity percentage
            catalyst_status: Active/Stable/Fading
            volume_profile: Accum./Dist./Mixed
            trend_strength: Trend strength description
            
        Returns:
            Tier classification: 'Tier 1', 'Tier 2', or 'Tier 3'
        """
        # Tier 1: High conviction leaders
        # Strong velocity + active catalysts + good trend
        if (velocity_score == "Strong" and velocity_value >= 0.15 and 
            catalyst_status == "Active" and 
            ("Strong" in trend_strength or "Uptrend" in trend_strength) and
            volume_profile == "Accum."):
            return "Tier 1"
        
        # Tier 1 alternative: Very strong velocity with active catalysts
        elif (velocity_score == "Strong" and velocity_value >= 0.20 and 
              catalyst_status == "Active"):
            return "Tier 1"
        
        # Tier 2: Strong but volatile
        # Moderate velocity + mixed volume OR Strong velocity with mixed signals
        elif ((velocity_score == "Moderate" and 
               volume_profile in ["Accum.", "Mixed"] and
               catalyst_status in ["Active", "Stable"]) or
              (velocity_score == "Strong" and 
               volume_profile == "Mixed" and
               trend_strength in ["Flattening", "Consolidating"])):
            return "Tier 2"
        
        # Tier 2 alternative: Good velocity with decent catalysts
        elif (velocity_score in ["Strong", "Moderate"] and 
              velocity_value >= 0.08 and
              catalyst_status == "Active"):
            return "Tier 2"
        
        # Tier 3: Watchlist / speculative
        # Slowing momentum or unclear catalysts
        else:
            return "Tier 3"
    
    def get_market_data(self, tickers: List[str], period: str = "6mo") -> Dict[str, pd.DataFrame]:
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
    
    def analyze_ticker(self, ticker: str) -> Dict:
        """
        Complete analysis of a single ticker
        
        Returns:
            Dictionary with all analysis results
        """
        try:
            # Get market data with 6-month period for proper calculations
            data = self.get_market_data([ticker], period="6mo")
            
            if ticker not in data or data[ticker].empty:
                return {
                    'ticker': ticker,
                    'error': 'No data available',
                    'classification': 'UNKNOWN'
                }
            
            df = data[ticker]
            
            # Calculate all metrics
            returns_data = self.data_fetcher.calculate_returns(df)
            velocity_score, velocity_value = self.calculate_velocity_score(returns_data)
            trend_analysis = self.analyze_trend_structure(df)
            volume_analysis = self.get_volume_analysis(df)
            catalyst_analysis = self.get_catalyst_status(ticker)
            
            # Classify position
            classification = self.classify_position(
                ticker, velocity_score, trend_analysis['trend_strength'],
                volume_analysis['volume_profile'], catalyst_analysis['catalyst_status']
            )
            
            # Determine action based on classification
            if classification == "GREEN":
                action = "Add" if velocity_score == "Strong" else "Hold"
            elif classification == "YELLOW":
                action = "Tighten" if "Slowing" in velocity_score else "Trim"
            else:  # RED
                action = "Exit"
            
            # Classify tier
            tier = self.classify_tier(
                ticker, velocity_score, velocity_value, catalyst_analysis['catalyst_status'],
                volume_analysis['volume_profile'], trend_analysis['trend_strength']
            )
            
            return {
                'ticker': ticker,
                'current_price': returns_data.get('current_price', 0),
                'velocity_score': velocity_score,
                'velocity_value': velocity_value,
                'trend_structure': trend_analysis['trend_structure'],
                'trend_strength': trend_analysis['trend_strength'],
                'volume_profile': volume_analysis['volume_profile'],
                'volume_trend': volume_analysis['volume_trend'],
                'catalyst_status': catalyst_analysis['catalyst_status'],
                'sentiment': catalyst_analysis['sentiment'],
                'news_count': catalyst_analysis['news_count'],
                'articles': catalyst_analysis.get('articles', []),
                'news_summary': catalyst_analysis.get('summary', ''),
                'classification': classification,
                'tier': tier,
                'action': action,
                'one_month_return': returns_data.get('one_month_return', 0),
                'three_month_return': returns_data.get('three_month_return', 0),
                'six_month_return': returns_data.get('six_month_return', 0),
                'mtd_return': returns_data.get('mtd_return', 0)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': str(e),
                'classification': 'UNKNOWN'
            }
    
    def analyze_theme(self, theme_tickers: List[str]) -> Dict:
        """
        Analyze all tickers in a theme and return classified results
        
        Returns:
            Dictionary with GREEN, YELLOW, RED lists and theme analysis
        """
        results = {
            'GREEN': [],
            'YELLOW': [],
            'RED': [],
            'UNKNOWN': [],
            'theme_metrics': {}
        }
        
        all_analyses = []
        
        for ticker in theme_tickers:
            analysis = self.analyze_ticker(ticker)
            classification = analysis.get('classification', 'UNKNOWN')
            results[classification].append(analysis)
            all_analyses.append(analysis)
        
        # Calculate theme metrics
        if all_analyses:
            total_positions = len([a for a in all_analyses if a.get('classification') != 'UNKNOWN'])
            green_count = len(results['GREEN'])
            yellow_count = len(results['YELLOW'])
            red_count = len(results['RED'])
            
            results['theme_metrics'] = {
                'total_positions': total_positions,
                'green_count': green_count,
                'yellow_count': yellow_count,
                'red_count': red_count,
                'green_percentage': (green_count / total_positions * 100) if total_positions > 0 else 0,
                'red_percentage': (red_count / total_positions * 100) if total_positions > 0 else 0
            }
        
        return results
    
    def get_macro_analysis(self) -> Dict:
        """Get macro market analysis"""
        macro_data = self.data_fetcher.get_macro_indicators()
        
        # Determine macro status
        spy_data = macro_data.get('spy', {})
        vix_data = macro_data.get('vix', {})
        
        spy_trend = spy_data.get('trend', 'Flat')
        vix_level = vix_data.get('level', 'Medium')
        
        # Macro status logic
        if spy_trend == 'Up' and vix_level == 'Low':
            macro_status = 'Risk On'
        elif spy_trend == 'Down' or vix_level == 'High':
            macro_status = 'Risk Off'
        else:
            macro_status = 'Neutral'
        
        return {
            'macro_status': macro_status,
            'spy_trend': spy_trend,
            'vix_level': vix_level,
            'spy_return': spy_data.get('one_month_return', 0),
            'vix_value': vix_data.get('current_price', 0),
            'all_indicators': macro_data
        }
