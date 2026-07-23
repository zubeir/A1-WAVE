# 🌊 A1-WAVE Dashboard

Ride macro waves. Exit before they break.

A tactical momentum strategy dashboard that analyzes market themes, classifies positions, and provides actionable trading insights.

## 🚀 Quick Start

### Option 1: Interactive Startup (Recommended)
```bash
python start_agent.py
```
This will show a menu with options to start the dashboard or agent.

### Option 2: Command Line Arguments
```bash
# Start dashboard only (manual refresh)
python start_agent.py --dashboard

# Start full agent with auto-refresh every 2 hours
python start_agent.py --agent

# Run data collection once
python start_agent.py --collect
```

### Option 3: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start dashboard
streamlit run dashboard.py

# Start agent (in separate terminal)
python agent.py
```

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection for market data
- No paid APIs required (uses free Yahoo Finance and RSS feeds)

## 🏗️ Project Structure

```
A1-WAVE/
├── dashboard.py          # Main Streamlit dashboard
├── agent.py              # Auto-refresh agent service
├── start_agent.py        # Startup script
├── analytics.py          # Scoring and classification logic
├── data_fetcher.py       # Market data and news fetching
├── config.py             # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md            # This file
├── data/                # Runtime data storage
├── exports/             # Exported dashboard data
├── snapshots/           # Historical data snapshots
└── logs/                # Agent logs
```

## 🎯 Features

### Dashboard Sections

1. **Theme Level Panel** - Macro market analysis and theme strength
2. **Position Classification** - Green/Yellow/Red position panels
3. **Weekly Rotation Plan** - Add/Trim/Exit/Rotate recommendations
4. **Notes & Journal** - Trading notes and decision journal

### Analytics

- **Velocity Score**: 1-month and 3-month return analysis
- **Trend Structure**: Moving average and price action analysis
- **Volume Profile**: Accumulation/Distribution analysis
- **Catalyst Status**: News sentiment analysis
- **Classification**: Automated GREEN/YELLOW/RED position classification

### Automation

- **Auto-refresh**: Data updates every 2 hours
- **Change Detection**: Alerts for significant position changes
- **Data Persistence**: Automatic saving of notes and analysis
- **Historical Snapshots**: Keeps 24 hourly snapshots for analysis

## 🎨 Themes

The dashboard comes with pre-configured themes:

- **Space Economy**: Commercial space, satellite, and aerospace companies
- **AI & Technology**: Artificial intelligence and semiconductor companies  
- **Defense**: Defense contractors and aerospace companies

### Adding Custom Themes

Edit `config.py` to add new themes:

```python
THEMES = {
    "Your Theme": {
        "name": "Your Theme Name",
        "sector_etfs": ["ETF1", "ETF2"],
        "tickers": ["TICKER1", "TICKER2", "TICKER3"],
        "description": "Theme description"
    }
}
```

## 📊 Data Sources

All data sources are free and publicly accessible:

- **Price/Volume Data**: Yahoo Finance (via yfinance)
- **News Sentiment**: Yahoo Finance RSS feeds
- **Market Indicators**: SPY, QQQ, VIX, Treasury yields
- **Sector ETFs**: Theme-specific ETFs for sector analysis

## 🔄 How It Works

### Classification Logic

**🟢 GREEN (Leaders)** - Add/Hold Full Weight
- Strong velocity (15%+ returns)
- Price above 20/50 day moving averages
- Accumulation volume pattern
- Positive news sentiment

**🟡 YELLOW (Slowing)** - Trim/Tighten Stops  
- Slowing velocity (5-15% returns)
- Testing 20-day moving average
- Mixed volume pattern
- Neutral news sentiment

**🔴 RED (Breaking)** - Exit/Rotate
- Weak velocity (<5% or negative returns)
- Price below 50-day moving average
- Distribution volume pattern
- Negative news sentiment

### Scoring System

Each position is scored on:
- Velocity (40% weight): Return performance
- Trend (30% weight): Moving average analysis  
- Volume (20% weight): Accumulation/Distribution
- Catalyst (10% weight): News sentiment

## 🛠️ Configuration

### Settings

Edit `config.py` to customize:

```python
DEFAULT_SETTINGS = {
    "refresh_interval": 7200,  # 2 hours in seconds
    "theme": "Space Economy",   # Default theme
    "auto_refresh": True,        # Enable auto-refresh
    "dark_mode": False          # Dark mode (future feature)
}
```

### Scoring Thresholds

```python
VELOCITY_THRESHOLDS = {
    "strong": 0.15,    # 15%+ returns
    "moderate": 0.05,  # 5-15% returns  
    "weak": -0.05      # <5% or negative returns
}
```

## 📱 Usage

### Dashboard Controls

- **Theme Selection**: Switch between different market themes
- **Refresh Data**: Manual data refresh
- **Export JSON**: Download dashboard data
- **Reset Notes**: Clear all notes and journal entries
- **Auto-save**: Notes are automatically saved

### Notes & Journal

Three journal fields for trading decisions:
- "Why I'm still in this wave"
- "What would make me exit"  
- "Next week's plan"

Notes are saved automatically and persist between sessions.

## 🔧 Troubleshooting

### Common Issues

**Dashboard won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r requirements.txt

# Check port availability
netstat -an | grep 8501
```

**No data showing**
```bash
# Check internet connection
ping finance.yahoo.com

# Run data collection manually
python start_agent.py --collect

# Check logs
tail -f logs/agent.log
```

**Agent not refreshing**
```bash
# Check agent status
ps aux | grep agent

# Restart agent
python agent.py --no-dashboard
```

### Logs

- **Agent logs**: `logs/agent.log`
- **Data files**: `data/latest_data.json`
- **Snapshots**: `snapshots/snapshot_*.json`

## 📈 Performance

- **Load time**: 3-5 seconds initial load
- **Refresh time**: 2-3 seconds for data update
- **Memory usage**: ~50-100MB
- **Data retention**: 24 hourly snapshots (~48 hours)

## 🔒 Security

- No API keys required
- All data sources are public
- Local data storage only
- No external data transmission

## 🤝 Contributing

To add features or fix issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the logs in `logs/agent.log`
3. Verify internet connectivity
4. Ensure all dependencies are installed

---

**🌊 Ride macro waves. Exit before they break.**
