"""
Configuration file for A1-WAVE Dashboard
Contains themes, tickers, and settings
"""

# Theme configurations
THEMES = {
    "Space Economy": {
        "name": "Space Economy Momentum",
        "sector_etfs": ["XAR", "UFO"],  # Aerospace & Defense, UFO ETF
        "tickers": ["RKLB", "RDW", "PL", "BKSY", "SPIR", "SATL", "LUNR", "ASTS", "SPCE", "MNTS"],
        "description": "Commercial space, satellite, and aerospace companies"
    },
    "AI & Technology": {
        "name": "AI Technology Momentum", 
        "sector_etfs": ["QQQ", "IGV"],  # NASDAQ, Software ETF
        "tickers": ["NVDA", "MSFT", "GOOGL", "META", "AMD", "SMCI", "PLTR", "AI", "TSLA", "CRM"],
        "description": "Artificial intelligence and semiconductor companies"
    },
    "Defense": {
        "name": "Defense & Aerospace Momentum",
        "sector_etfs": ["XAR", "ITA"],  # Aerospace & Defense ETFs
        "tickers": ["LMT", "RTX", "HII", "BA", "TDG", "TXT", "NOC", "GD", "HWM", "BWXT"],
        "description": "Defense contractors and aerospace companies"
    },
    "Clean Energy": {
        "name": "Clean Energy Transition",
        "sector_etfs": ["ICLN", "TAN"],  # Clean Energy, Solar ETFs
        "tickers": ["ENPH", "SEDG", "FSLR", "RUN", "PLUG", "BE", "CHPT", "NEE", "SRE", "XEL"],
        "description": "Solar, wind, hydrogen, and battery technology companies"
    },
    "Biotechnology": {
        "name": "Biotechnology Innovation",
        "sector_etfs": ["IBB", "XBI"],  # NASDAQ Biotech, S&P Biotech ETFs
        "tickers": ["GILD", "MRNA", "BNTX", "MODERNA", "CRSP", "EDIT", "NTLA", "BLUE", "BIIB", "REGN"],
        "description": "Gene editing, mRNA, and biopharmaceutical companies"
    },
    "Electric Vehicles": {
        "name": "Electric Vehicle Revolution",
        "sector_etfs": ["DRIV", "CARZ"],  # Global X Autonomous & Electric Vehicles ETFs
        "tickers": ["TSLA", "RIVN", "LCID", "FSR", "NIO", "XPEV", "LI", "RIVIAN", "GM", "F"],
        "description": "Electric vehicle manufacturers and autonomous driving technology"
    },
    "Fintech": {
        "name": "Financial Technology Disruption",
        "sector_etfs": ["ARKF", "FINX"],  # Fintech Innovation ETFs
        "tickers": ["SQ", "PYPL", "MELI", "AFRM", "UPST", "SOFI", "BK", "COIN", "V", "MA"],
        "description": "Digital payments, lending, and blockchain financial services"
    },
    "Cloud Computing": {
        "name": "Cloud Computing Growth",
        "sector_etfs": ["SKYY", "CLOU"],  # Cloud Computing ETFs
        "tickers": ["AMZN", "MSFT", "GOOGL", "CRM", "NOW", "SNOW", "ZS", "OKTA", "TEAM", "ADBE"],
        "description": "Cloud infrastructure, SaaS, and enterprise software companies"
    },
    "Cybersecurity": {
        "name": "Cybersecurity Defense",
        "sector_etfs": ["HACK", "CIBR"],  # Cybersecurity ETFs
        "tickers": ["CRWD", "ZS", "OKTA", "PANW", "FTNT", "MNDT", "Tenable", "Qualys", "SPLK", "CHKP"],
        "description": "Network security, endpoint protection, and threat intelligence companies"
    },
    "Semiconductors": {
        "name": "Semiconductor Supercycle",
        "sector_etfs": ["SOXX", "SMH"],  # Semiconductor ETFs
        "tickers": ["NVDA", "AMD", "INTC", "TSM", "ASML", "MU", "MRVL", "ON", "QCOM", "AVGO"],
        "description": "Chip designers, manufacturers, and equipment suppliers"
    },
    "Gaming & Esports": {
        "name": "Gaming & Esports Economy",
        "sector_etfs": ["GAMR", "ESPO"],  # Gaming & Esports ETFs
        "tickers": ["EA", "TTWO", "ATVI", "RBLX", "CD Projekt", "UBI", "NTDOY", "SCPL", "EMN", "SE"],
        "description": "Video game developers, publishers, and esports platforms"
    },
    "Renewable Energy": {
        "name": "Renewable Energy Transition",
        "sector_etfs": ["ICLN", "TAN", "FAN"],  # Clean Energy, Solar, Wind ETFs
        "tickers": ["NEE", "DUK", "AEP", "SRE", "XEL", "ED", "PEG", "EIX", "DTE", "WEC"],
        "description": "Utilities and companies focused on renewable energy generation"
    },
    "Digital Health": {
        "name": "Digital Health Transformation",
        "sector_etfs": ["THNQ", "HIML"],  # Digital Health ETFs
        "tickers": ["TELAD", "DOCS", "AMWL", "HIMS", "BARK", "GH", "LVGO", "RVL", "COV", "MD"],
        "description": "Telemedicine, digital therapeutics, and health technology platforms"
    },
    "Robotics & Automation": {
        "name": "Robotics & Automation Future",
        "sector_etfs": ["ROBO", "BOTZ"],  # Robotics & Automation ETFs
        "tickers": ["IRBT", "AUBO", "iRobot", "Teradyne", "Cognex", "Keyence", "Yaskawa", "ABB", "ROK", "HON"],
        "description": "Industrial robots, automation systems, and AI-powered machinery"
    },
    "5G & Telecom": {
        "name": "5G & Telecommunications Buildout",
        "sector_etfs": ["VOX", "IXP"],  # Telecom, Networking ETFs
        "tickers": ["VZ", "T", "TMUS", "S", "CMCSA", "CHTR", "EQIX", "AMT", "CCI", "SBAC"],
        "description": "5G infrastructure, fiber networks, and telecommunications services"
    },
    "Metaverse & Web3": {
        "name": "Metaverse & Web3 Economy",
        "sector_etfs": ["MESH", "W3R"],  # Metaverse, Web3 ETFs
        "tickers": ["META", "NVDA", "AMD", "ROBLOX", "Unity", "SNAP", "TWTR", "Coinbase", "U", "SAND"],
        "description": "Virtual reality, augmented reality, and blockchain-based platforms"
    }
}

# Market indicators for macro analysis
MARKET_INDICATORS = {
    "spy": "SPY",      # S&P 500
    "qqq": "QQQ",      # NASDAQ
    "dia": "DIA",      # Dow Jones
    "vix": "^VIX",     # VIX Index
    "tnx": "^TNX",     # 10-Year Treasury Yield
}

# Default settings
DEFAULT_SETTINGS = {
    "refresh_interval": 7200,  # 2 hours in seconds
    "theme": "Space Economy",
    "auto_refresh": True,
    "dark_mode": False
}

# Scoring thresholds
VELOCITY_THRESHOLDS = {
    "strong": 0.15,    # 15%+ returns
    "moderate": 0.05,  # 5-15% returns
    "weak": -0.05      # <5% or negative returns
}

VOLUME_DAYS = 10  # Days to analyze for volume profile
MA_DAYS = [20, 50]  # Moving average periods
