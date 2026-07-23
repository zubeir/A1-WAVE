"""
A1-WAVE Dashboard - Main Streamlit Application
Ride macro waves. Exit before they break.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List
import plotly.express as px
import plotly.graph_objects as go

from config import THEMES, DEFAULT_SETTINGS
from analytics import Analytics
from data_fetcher import DataFetcher

# Page configuration
st.set_page_config(
    page_title="A1-WAVE Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .theme-panel {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .green-panel {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .yellow-panel {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .red-panel {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = DEFAULT_SETTINGS['theme']
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = None
    if 'notes' not in st.session_state:
        st.session_state.notes = {
            'why_still_in': '',
            'what_would_exit': '',
            'next_week_plan': ''
        }
    if 'ticker_notes' not in st.session_state:
        st.session_state.ticker_notes = {}

def save_notes_to_file():
    """Save notes to JSON file"""
    notes_data = {
        'timestamp': datetime.now().isoformat(),
        'theme': st.session_state.current_theme,
        'notes': st.session_state.notes,
        'ticker_notes': st.session_state.ticker_notes
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/notes.json', 'w') as f:
        json.dump(notes_data, f, indent=2)

def load_notes_from_file():
    """Load notes from JSON file"""
    try:
        if os.path.exists('data/notes.json'):
            with open('data/notes.json', 'r') as f:
                notes_data = json.load(f)
                st.session_state.notes = notes_data.get('notes', st.session_state.notes)
                st.session_state.ticker_notes = notes_data.get('ticker_notes', {})
    except Exception as e:
        st.warning(f"Could not load notes: {e}")

def render_theme_panel(macro_analysis: Dict, theme_metrics: Dict):
    """Render Section 1 - Theme Level Panel"""
    st.markdown("## 📊 Theme Level Analysis")
    
    # Get current theme info
    theme_info = THEMES[st.session_state.current_theme]
    
    # Determine sector strength from theme metrics
    green_pct = theme_metrics.get('green_percentage', 0)
    if green_pct >= 60:
        sector_strength = "Strong"
    elif green_pct >= 40:
        sector_strength = "Moderate"
    else:
        sector_strength = "Weak"
    
    # ETF Trend (simplified - would need actual ETF data)
    etf_trend = "Above 20 day MA" if macro_analysis.get('spy_trend') == 'Up' else "Below 20 day MA"
    
    # Narrative status (simplified)
    narrative = "Strengthening" if green_pct > 50 else "Stable" if green_pct > 30 else "Weakening"
    
    # Decision logic
    macro_status = macro_analysis.get('macro_status', 'Neutral')
    if macro_status == 'Risk On' and green_pct >= 60:
        decision = "Maintain Wave"
    elif macro_status == 'Risk Off' or green_pct <= 30:
        decision = "Exit"
    else:
        decision = "Reduce Exposure"
    
    # Display theme panel
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Theme", theme_info['name'])
    
    with col2:
        st.metric("Macro Status", macro_status)
    
    with col3:
        st.metric("Sector Strength", sector_strength)
    
    with col4:
        st.metric("ETF Trend", etf_trend)
    
    with col5:
        st.metric("Decision", decision)
    
    st.markdown("---")

def render_position_panels(theme_analysis: Dict):
    """Render Section 2 - Green/Yellow/Red Position Panels"""
    
    # First, show a summary table of all positions
    st.markdown("## 📋 All Positions Summary")
    
    all_positions = []
    for classification in ['GREEN', 'YELLOW', 'RED']:
        for pos in theme_analysis.get(classification, []):
            all_positions.append({
                'Ticker': pos['ticker'],
                'Classification': classification,
                'Tier': pos.get('tier', 'Tier 3'),
                'Velocity': f"{pos['velocity_score']} ({pos['velocity_value']:.1%})",
                'Trend': pos['trend_structure'],
                'Volume': pos['volume_profile'],
                'Catalyst': pos['catalyst_status'],
                'Action': pos['action'],
                'Price': f"${pos['current_price']:.2f}",
                'MTD': f"{pos.get('mtd_return', 0):.1%}",
                '1M Return': f"{pos['one_month_return']:.1%}",
                '3M Return': f"{pos['three_month_return']:.1%}",
                '6M Return': f"{pos.get('six_month_return', 0):.1%}"
            })
    
    if all_positions:
        # Create DataFrame for the summary table
        df_summary = pd.DataFrame(all_positions)
        
        # Display summary table with tooltips
        st.dataframe(
            df_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Classification": st.column_config.TextColumn(
                    "Classification",
                    help="📊 **Position Classification**\n\n• **GREEN**: Strong momentum, add/hold positions\n• **YELLOW**: Slowing momentum, tighten/trim positions\n• **RED**: Weak momentum, exit positions\n\nBased on velocity, trend, volume, and catalyst analysis"
                ),
                "Tier": st.column_config.TextColumn(
                    "Tier",
                    help="🏆 **Conviction Level Classification**\n\n• **Tier 1**: High conviction leaders\n  - Strong velocity (≥15%)\n  - Active catalysts\n  - Strong uptrend\n  - Accumulation volume\n  - Example: LMT, RTX, HII\n\n• **Tier 2**: Strong but volatile\n  - Moderate velocity (≥8%)\n  - Mixed volume signals\n  - Active/stable catalysts\n  - Example: BA, TDG, TXT\n\n• **Tier 3**: Watchlist/speculative\n  - Slowing momentum\n  - Unclear catalysts\n  - Weak trend signals\n  - Example: NOC, GD (if flattening)"
                ),
                "Ticker": st.column_config.TextColumn(
                    "Ticker",
                    help="🏷️ **Stock Symbol**\n\nCompany ticker symbol used for trading and identification"
                ),
                "Velocity": st.column_config.TextColumn(
                    "Velocity",
                    help="🚀 **Price Momentum Score**\n\n**Scoring Methodology:**\n- Weighted average of 1M (40%) and 3M (60%) returns\n- **Strong**: ≥15% weighted return\n- **Moderate**: ≥8% weighted return\n- **Slowing**: ≥3% weighted return\n- **Weak**: <3% weighted return\n\nHigher velocity indicates stronger price momentum"
                ),
                "Trend": st.column_config.TextColumn(
                    "Trend",
                    help="📈 **Technical Trend Structure**\n\n**Trend Analysis:**\n- **HH/HL**: Higher Highs, Higher Lows (Strong Uptrend)\n- **Above MA20**: Price above 20-day moving average\n- **Testing MA20**: Price at key support level\n- **Near MA20**: Within 5% of 20-day MA\n- **LHL**: Lower Highs, Lower Lows (Breakdown)\n\nBased on moving averages and price action"
                ),
                "Volume": st.column_config.TextColumn(
                    "Volume",
                    help="📊 **Volume Profile Analysis**\n\n**Volume Patterns:**\n- **Accum.**: Accumulation - Buying pressure dominates\n- **Mixed**: Balanced buying/selling pressure\n- **Dist.**: Distribution - Selling pressure dominates\n\nAnalyzed over recent trading days to identify institutional flow"
                ),
                "Catalyst": st.column_config.TextColumn(
                    "Catalyst",
                    help="⚡ **News Sentiment Catalyst**\n\n**Catalyst Status:**\n- **Active**: Positive news flow, multiple positive articles\n- **Stable**: Neutral news flow, balanced coverage\n- **Fading**: Negative news flow, concerning developments\n\nBased on recent news sentiment analysis"
                ),
                "Action": st.column_config.TextColumn(
                    "Action",
                    help="🎯 **Recommended Trading Action**\n\n**Action Framework:**\n- **Add**: Strong momentum, consider position accumulation\n- **Hold**: Maintain current position size\n- **Tighten**: Raise stop losses, reduce risk\n- **Trim**: Reduce position size gradually\n- **Exit**: Close position completely\n\nActions based on classification and velocity"
                ),
                "Price": st.column_config.TextColumn(
                    "Price",
                    help="💰 **Current Stock Price**\n\nLatest closing price from Yahoo Finance data"
                ),
                "MTD": st.column_config.TextColumn(
                    "MTD",
                    help="📅 **Month-to-Date Return**\n\nPerformance from first trading day of current month to today\n\nShows current month's momentum and trend strength"
                ),
                "1M Return": st.column_config.TextColumn(
                    "1M Return",
                    help="📊 **1-Month Return**\n\nPerformance over approximately 21 trading days\n\nShort-term momentum indicator for recent price action"
                ),
                "3M Return": st.column_config.TextColumn(
                    "3M Return",
                    help="📈 **3-Month Return**\n\nPerformance over approximately 63 trading days\n\nMedium-term trend indicator and momentum confirmation"
                ),
                "6M Return": st.column_config.TextColumn(
                    "6M Return",
                    help="📊 **6-Month Return**\n\nPerformance over approximately 126 trading days\n\nLong-term trend strength and sustainable momentum"
                )
            }
        )
    
    st.markdown("---")
    
    # Create three columns for detailed panels
    col1, col2, col3 = st.columns(3)
    
    # GREEN Panel
    with col1:
        st.markdown("### 🟢 GREEN - Leaders")
        st.markdown("(Add / Hold Full Weight)")
        
        green_positions = theme_analysis.get('GREEN', [])
        if green_positions:
            for pos in green_positions:
                with st.container():
                    # Create a more detailed display with all metrics
                    col_a, col_b = st.columns([1, 2])
                    
                    with col_a:
                        st.markdown(f"""
                        <div class="green-panel">
                            <h4><strong>{pos['ticker']}</strong> - {pos.get('tier', 'Tier 3')}</h4>
                            <div style="font-size: 0.9em;">
                                <b>Velocity:</b> {pos['velocity_score']} ({pos['velocity_value']:.1%})<br>
                                <b>Trend:</b> {pos['trend_structure']}<br>
                                <b>Volume:</b> {pos['volume_profile']}<br>
                                <b>Catalyst:</b> {pos['catalyst_status']}<br>
                                <b>Action:</b> <span style="color: #0d6efd; font-weight: bold;">{pos['action']}</span><br>
                                <b>Price:</b> ${pos['current_price']:.2f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        # Additional metrics in a compact format
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 0.8em;">
                            <strong>Performance Metrics:</strong><br>
                            MTD: {pos.get('mtd_return', 0):.1%} | 1M: {pos['one_month_return']:.1%} | 3M: {pos['three_month_return']:.1%} | 6M: {pos.get('six_month_return', 0):.1%}<br>
                            <strong>News:</strong> {pos['news_count']} articles ({pos['sentiment']})
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add collapsible news summary
                        if pos.get('news_summary') and pos['news_count'] > 0:
                            with st.expander(f"📰 AI News Summary for {pos['ticker']}", expanded=False):
                                st.markdown(f"""
                                <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3;">
                                    <h4 style="margin-top: 0; color: #1976d2;">🤖 AI-Generated News Analysis</h4>
                                    <p style="margin-bottom: 10px;"><strong>Key Takeaways:</strong></p>
                                    <p style="line-height: 1.6;">{pos['news_summary']}</p>
                                    
                                    <p style="margin-top: 15px; margin-bottom: 5px;"><strong>Recent Articles:</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Show individual articles
                                articles = pos.get('articles', [])
                                for i, article in enumerate(articles[:3], 1):
                                    st.markdown(f"""
                                    <div style="background: white; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #e0e0e0;">
                                        <p style="margin: 0; font-weight: bold; color: #333;">{i}. {article['title']}</p>
                                        <p style="margin: 5px 0; font-size: 0.9em; color: #666;">{article['summary'][:200]}...</p>
                                        <a href="{article['link']}" target="_blank" style="font-size: 0.8em; color: #2196f3;">Read more →</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    # Add ticker notes
                    ticker_key = f"note_{pos['ticker']}"
                    if ticker_key not in st.session_state.ticker_notes:
                        st.session_state.ticker_notes[ticker_key] = ""
                    
                    note = st.text_area(
                        f"Notes for {pos['ticker']}",
                        value=st.session_state.ticker_notes[ticker_key],
                        key=f"textarea_{pos['ticker']}",
                        height=50
                    )
                    st.session_state.ticker_notes[ticker_key] = note
        else:
            st.info("No GREEN positions")
    
    # YELLOW Panel
    with col2:
        st.markdown("### 🟡 YELLOW - Slowing")
        st.markdown("(Trim / Tighten Stops)")
        
        yellow_positions = theme_analysis.get('YELLOW', [])
        if yellow_positions:
            for pos in yellow_positions:
                with st.container():
                    # Create a more detailed display with all metrics
                    col_a, col_b = st.columns([1, 2])
                    
                    with col_a:
                        st.markdown(f"""
                        <div class="yellow-panel">
                            <h4><strong>{pos['ticker']}</strong> - {pos.get('tier', 'Tier 3')}</h4>
                            <div style="font-size: 0.9em;">
                                <b>Velocity:</b> {pos['velocity_score']} ({pos['velocity_value']:.1%})<br>
                                <b>Trend:</b> {pos['trend_structure']}<br>
                                <b>Volume:</b> {pos['volume_profile']}<br>
                                <b>Catalyst:</b> {pos['catalyst_status']}<br>
                                <b>Action:</b> <span style="color: #fd7e14; font-weight: bold;">{pos['action']}</span><br>
                                <b>Price:</b> ${pos['current_price']:.2f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        # Additional metrics in a compact format
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 0.8em;">
                            <strong>Performance Metrics:</strong><br>
                            MTD: {pos.get('mtd_return', 0):.1%} | 1M: {pos['one_month_return']:.1%} | 3M: {pos['three_month_return']:.1%} | 6M: {pos.get('six_month_return', 0):.1%}<br>
                            <strong>News:</strong> {pos['news_count']} articles ({pos['sentiment']})
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add collapsible news summary
                        if pos.get('news_summary') and pos['news_count'] > 0:
                            with st.expander(f"📰 AI News Summary for {pos['ticker']}", expanded=False):
                                st.markdown(f"""
                                <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3;">
                                    <h4 style="margin-top: 0; color: #1976d2;">🤖 AI-Generated News Analysis</h4>
                                    <p style="margin-bottom: 10px;"><strong>Key Takeaways:</strong></p>
                                    <p style="line-height: 1.6;">{pos['news_summary']}</p>
                                    
                                    <p style="margin-top: 15px; margin-bottom: 5px;"><strong>Recent Articles:</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Show individual articles
                                articles = pos.get('articles', [])
                                for i, article in enumerate(articles[:3], 1):
                                    st.markdown(f"""
                                    <div style="background: white; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #e0e0e0;">
                                        <p style="margin: 0; font-weight: bold; color: #333;">{i}. {article['title']}</p>
                                        <p style="margin: 5px 0; font-size: 0.9em; color: #666;">{article['summary'][:200]}...</p>
                                        <a href="{article['link']}" target="_blank" style="font-size: 0.8em; color: #2196f3;">Read more →</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    # Add ticker notes
                    ticker_key = f"note_{pos['ticker']}"
                    if ticker_key not in st.session_state.ticker_notes:
                        st.session_state.ticker_notes[ticker_key] = ""
                    
                    note = st.text_area(
                        f"Notes for {pos['ticker']}",
                        value=st.session_state.ticker_notes[ticker_key],
                        key=f"textarea_{pos['ticker']}",
                        height=50
                    )
                    st.session_state.ticker_notes[ticker_key] = note
        else:
            st.info("No YELLOW positions")
    
    # RED Panel
    with col3:
        st.markdown("### 🔴 RED - Breaking")
        st.markdown("(Exit / Rotate)")
        
        red_positions = theme_analysis.get('RED', [])
        if red_positions:
            for pos in red_positions:
                with st.container():
                    # Create a more detailed display with all metrics
                    col_a, col_b = st.columns([1, 2])
                    
                    with col_a:
                        st.markdown(f"""
                        <div class="red-panel">
                            <h4><strong>{pos['ticker']}</strong> - {pos.get('tier', 'Tier 3')}</h4>
                            <div style="font-size: 0.9em;">
                                <b>Velocity:</b> {pos['velocity_score']} ({pos['velocity_value']:.1%})<br>
                                <b>Trend:</b> {pos['trend_structure']}<br>
                                <b>Volume:</b> {pos['volume_profile']}<br>
                                <b>Catalyst:</b> {pos['catalyst_status']}<br>
                                <b>Action:</b> <span style="color: #dc3545; font-weight: bold;">{pos['action']}</span><br>
                                <b>Price:</b> ${pos['current_price']:.2f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        # Additional metrics in a compact format
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 0.8em;">
                            <strong>Performance Metrics:</strong><br>
                            MTD: {pos.get('mtd_return', 0):.1%} | 1M: {pos['one_month_return']:.1%} | 3M: {pos['three_month_return']:.1%} | 6M: {pos.get('six_month_return', 0):.1%}<br>
                            <strong>News:</strong> {pos['news_count']} articles ({pos['sentiment']})
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add collapsible news summary
                        if pos.get('news_summary') and pos['news_count'] > 0:
                            with st.expander(f"📰 AI News Summary for {pos['ticker']}", expanded=False):
                                st.markdown(f"""
                                <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3;">
                                    <h4 style="margin-top: 0; color: #1976d2;">🤖 AI-Generated News Analysis</h4>
                                    <p style="margin-bottom: 10px;"><strong>Key Takeaways:</strong></p>
                                    <p style="line-height: 1.6;">{pos['news_summary']}</p>
                                    
                                    <p style="margin-top: 15px; margin-bottom: 5px;"><strong>Recent Articles:</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Show individual articles
                                articles = pos.get('articles', [])
                                for i, article in enumerate(articles[:3], 1):
                                    st.markdown(f"""
                                    <div style="background: white; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #e0e0e0;">
                                        <p style="margin: 0; font-weight: bold; color: #333;">{i}. {article['title']}</p>
                                        <p style="margin: 5px 0; font-size: 0.9em; color: #666;">{article['summary'][:200]}...</p>
                                        <a href="{article['link']}" target="_blank" style="font-size: 0.8em; color: #2196f3;">Read more →</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    # Add ticker notes
                    ticker_key = f"note_{pos['ticker']}"
                    if ticker_key not in st.session_state.ticker_notes:
                        st.session_state.ticker_notes[ticker_key] = ""
                    
                    note = st.text_area(
                        f"Notes for {pos['ticker']}",
                        value=st.session_state.ticker_notes[ticker_key],
                        key=f"textarea_{pos['ticker']}",
                        height=50
                    )
                    st.session_state.ticker_notes[ticker_key] = note
        else:
            st.info("No RED positions")
    
    st.markdown("---")

def render_rotation_panel(theme_analysis: Dict):
    """Render Section 3 - Weekly Rotation Panel"""
    st.markdown("## 🔄 Weekly Rotation Plan")
    
    green_positions = theme_analysis.get('GREEN', [])
    yellow_positions = theme_analysis.get('YELLOW', [])
    red_positions = theme_analysis.get('RED', [])
    
    # Generate rotation suggestions
    add_tickers = [pos['ticker'] for pos in green_positions if pos['action'] == 'Add']
    trim_tickers = [pos['ticker'] for pos in yellow_positions if pos['action'] in ['Trim', 'Tighten']]
    exit_tickers = [pos['ticker'] for pos in red_positions]
    
    # Rotation suggestions
    rotate_suggestions = []
    for red_pos in red_positions:
        for green_pos in green_positions:
            if green_pos['action'] == 'Add':
                rotate_suggestions.append(f"{red_pos['ticker']} → {green_pos['ticker']}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("### **ADD**")
        st.write("\n".join(add_tickers) if add_tickers else "None")
    
    with col2:
        st.markdown("### **TRIM**")
        st.write("\n".join(trim_tickers) if trim_tickers else "None")
    
    with col3:
        st.markdown("### **EXIT**")
        st.write("\n".join(exit_tickers) if exit_tickers else "None")
    
    with col4:
        st.markdown("### **ROTATE**")
        st.write("\n".join(rotate_suggestions[:3]) if rotate_suggestions else "None")
    
    with col5:
        st.markdown("### **REBALANCE**")
        total = len(green_positions) + len(yellow_positions) + len(red_positions)
        if total > 0:
            st.write(f"Green: {len(green_positions)}/{total}")
            st.write(f"Yellow: {len(yellow_positions)}/{total}")
            st.write(f"Red: {len(red_positions)}/{total}")
        else:
            st.write("No positions")
    
    st.markdown("---")

def render_notes_panel():
    """Render Section 4 - Notes & Journal Panel"""
    st.markdown("## 📝 Notes & Journal")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### **Why I'm still in this wave**")
        note1 = st.text_area(
            "Enter your notes here...",
            value=st.session_state.notes['why_still_in'],
            key="note1",
            height=150,
            label_visibility="collapsed"
        )
        st.session_state.notes['why_still_in'] = note1
    
    with col2:
        st.markdown("### **What would make me exit**")
        note2 = st.text_area(
            "Enter your notes here...",
            value=st.session_state.notes['what_would_exit'],
            key="note2",
            height=150,
            label_visibility="collapsed"
        )
        st.session_state.notes['what_would_exit'] = note2
    
    with col3:
        st.markdown("### **Next week's plan**")
        note3 = st.text_area(
            "Enter your notes here...",
            value=st.session_state.notes['next_week_plan'],
            key="note3",
            height=150,
            label_visibility="collapsed"
        )
        st.session_state.notes['next_week_plan'] = note3
    
    st.markdown("---")

def render_sidebar():
    """Render sidebar with controls"""
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    
    # Theme selection
    theme_options = list(THEMES.keys())
    selected_theme = st.sidebar.selectbox(
        "Select Theme",
        theme_options,
        index=theme_options.index(st.session_state.current_theme)
    )
    
    if selected_theme != st.session_state.current_theme:
        st.session_state.current_theme = selected_theme
        st.rerun()
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    # Export/Import buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("💾 Export"):
            export_data()
    
    with col2:
        if st.button("📂 Reset Notes"):
            st.session_state.notes = {
                'why_still_in': '',
                'what_would_exit': '',
                'next_week_plan': ''
            }
            st.session_state.ticker_notes = {}
            save_notes_to_file()
            st.success("Notes reset!")
    
    # Last refresh time
    if st.session_state.last_refresh:
        st.sidebar.info(f"Last refreshed: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    # Auto-refresh info
    st.sidebar.info("Auto-refresh: Every 2 hours")

def export_data():
    """Export dashboard data to JSON"""
    try:
        # Get current analytics data
        analytics = Analytics()
        theme_info = THEMES[st.session_state.current_theme]
        theme_analysis = analytics.analyze_theme(theme_info['tickers'])
        macro_analysis = analytics.get_macro_analysis()
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'theme': st.session_state.current_theme,
            'theme_analysis': theme_analysis,
            'macro_analysis': macro_analysis,
            'notes': st.session_state.notes,
            'ticker_notes': st.session_state.ticker_notes
        }
        
        # Save to file
        os.makedirs('exports', exist_ok=True)
        filename = f"exports/a1wave_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        st.success(f"Data exported to {filename}")
        
    except Exception as e:
        st.error(f"Export failed: {e}")

def main():
    """Main dashboard function"""
    load_css()
    initialize_session_state()
    load_notes_from_file()
    
    # Header
    st.markdown('<div class="main-header">🌊 A1-WAVE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ride macro waves. Exit before they break.</div>', unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Initialize analytics
    analytics = Analytics()
    
    # Get current theme info
    theme_info = THEMES[st.session_state.current_theme]
    
    # Load data with progress indicator
    with st.spinner("Analyzing market data..."):
        try:
            # Get theme analysis
            theme_analysis = analytics.analyze_theme(theme_info['tickers'])
            macro_analysis = analytics.get_macro_analysis()
            
            # Update last refresh time
            if not st.session_state.last_refresh:
                st.session_state.last_refresh = datetime.now()
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return
    
    # Render all sections
    render_theme_panel(macro_analysis, theme_analysis.get('theme_metrics', {}))
    render_position_panels(theme_analysis)
    render_rotation_panel(theme_analysis)
    render_notes_panel()
    
    # Auto-save notes
    save_notes_to_file()
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        f"A1-WAVE Dashboard v1.0 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
