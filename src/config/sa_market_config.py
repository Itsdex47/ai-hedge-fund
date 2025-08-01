"""
South African Market Configuration
Configuration settings for JSE (Johannesburg Stock Exchange) market operations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import time


@dataclass
class SAMarketConfig:
    """South African market configuration settings"""

    # Exchange Information
    EXCHANGE_NAME: str = "JSE"
    EXCHANGE_CODE: str = "JSE"
    CURRENCY: str = "ZAR"
    CURRENCY_SYMBOL: str = "R"

    # Trading Hours (SAST - South African Standard Time)
    TRADING_START_TIME: time = time(9, 0)  # 9:00 AM
    TRADING_END_TIME: time = time(17, 0)  # 5:00 PM
    MARKET_TIMEZONE: str = "Africa/Johannesburg"

    # Market Characteristics
    MIN_TICK_SIZE: float = 0.01  # 1 cent minimum tick
    SETTLEMENT_DAYS: int = 3  # T+3 settlement
    MARKET_CAP_THRESHOLD: float = 1000000  # 1M ZAR minimum for liquid stocks

    # JSE Indices
    MAJOR_INDICES: List[str] = field(
        default_factory=lambda: [
            "JSE:J203",  # FTSE/JSE Top 40
            "JSE:J200",  # FTSE/JSE All Share
            "JSE:J250",  # FTSE/JSE Mid Cap
            "JSE:J580",  # FTSE/JSE Small Cap
            "JSE:J433",  # FTSE/JSE Financial 15
            "JSE:J210",  # FTSE/JSE Industrial 25
            "JSE:J211",  # FTSE/JSE Resources 10
        ]
    )

    # Major Sectors in SA
    SECTORS: List[str] = field(default_factory=lambda: ["Financial Services", "Mining & Resources", "Industrial", "Consumer Goods", "Technology", "Healthcare", "Real Estate", "Telecommunications", "Energy", "Transportation"])

    # Top JSE Stocks by Market Cap (as of 2024)
    TOP_STOCKS: List[str] = field(
        default_factory=lambda: [
            "NPN",  # Naspers
            "BHP",  # BHP Group (dual-listed)
            "AGL",  # Anglo American (dual-listed)
            "MTN",  # MTN Group
            "VOD",  # Vodacom
            "SBK",  # Standard Bank
            "FSR",  # FirstRand
            "NED",  # Nedbank
            "ABG",  # Absa Group
            "SOL",  # Sasol
            "IMP",  # Impala Platinum
            "ANG",  # AngloGold Ashanti
            "AMS",  # Anglo American Platinum
            "SHP",  # Shoprite
            "WHL",  # Woolworths
            "TBS",  # Tiger Brands
            "BID",  # Bid Corporation
            "TFG",  # The Foschini Group
            "MRP",  # Mr Price Group
            "CLS",  # Clicks Group"
        ]
    )

    # Data Sources for SA Market
    DATA_SOURCES: Dict[str, str] = field(default_factory=lambda: {"prices": "https://api.financialdatasets.ai/prices/", "fundamentals": "https://api.financialdatasets.ai/financial-metrics/", "news": "https://api.financialdatasets.ai/news/", "insider_trades": "https://api.financialdatasets.ai/insider-trades/", "company_facts": "https://api.financialdatasets.ai/company-facts/"})  # Supports JSE tickers

    # Alternative SA-specific data sources
    SA_DATA_SOURCES: Dict[str, str] = field(default_factory=lambda: {"sharenet": "https://www.sharenet.co.za/", "jse_direct": "https://www.jse.co.za/", "moneyweb": "https://www.moneyweb.co.za/", "fin24": "https://www.fin24.com/", "business_live": "https://www.businesslive.co.za/"})

    # Regulatory Settings
    REGULATORY_BODY: str = "FSCA"  # Financial Sector Conduct Authority
    EXCHANGE_CONTROLS: bool = True
    FOREIGN_INVESTMENT_LIMITS: Dict[str, float] = field(default_factory=lambda: {"individual": 0.0, "institutional": 0.0})  # No individual foreign investment limits  # No institutional foreign investment limits

    # Risk Management Settings
    MAX_POSITION_SIZE: float = 0.05  # 5% max position per stock
    MAX_SECTOR_EXPOSURE: float = 0.30  # 30% max exposure per sector
    STOP_LOSS_PERCENTAGE: float = 0.15  # 15% stop loss
    MAX_DAILY_DRAWDOWN: float = 0.02  # 2% max daily drawdown

    # SA Market Specific Risk Factors
    RISK_FACTORS: List[str] = field(default_factory=lambda: ["Currency volatility (ZAR)", "Political risk", "Load shedding impact", "Commodity price exposure", "Emerging market volatility", "Regulatory changes", "Infrastructure challenges"])

    # Currency Pairs for FX Risk
    MAJOR_CURRENCY_PAIRS: List[str] = field(
        default_factory=lambda: [
            "USDZAR",  # US Dollar to Rand
            "EURZAR",  # Euro to Rand
            "GBPZAR",  # British Pound to Rand
            "JPYZAR",  # Japanese Yen to Rand
            "CNYZAR",  # Chinese Yuan to Rand
        ]
    )

    # Economic Indicators to Monitor
    ECONOMIC_INDICATORS: List[str] = field(
        default_factory=lambda: [
            "SA_CPI",  # Consumer Price Index
            "SA_REPO_RATE",  # Repo Rate
            "SA_GDP",  # Gross Domestic Product
            "SA_UNEMPLOYMENT",  # Unemployment Rate
            "SA_CURRENT_ACCOUNT",  # Current Account Balance
            "SA_BUDGET_DEFICIT",  # Budget Deficit
            "SA_CREDIT_RATING",  # Sovereign Credit Rating
        ]
    )


# Global instance
sa_config = SAMarketConfig()


def get_sa_config() -> SAMarketConfig:
    """Get the South African market configuration"""
    return sa_config


def is_jse_ticker(ticker: str) -> bool:
    """Check if a ticker is a JSE ticker"""
    # JSE tickers are typically 3-4 characters and in our known list
    return len(ticker) >= 3 and len(ticker) <= 4 and ticker.isalpha() and ticker in sa_config.TOP_STOCKS


def get_zar_currency_info() -> Dict[str, str]:
    """Get ZAR currency information"""
    return {"code": sa_config.CURRENCY, "symbol": sa_config.CURRENCY_SYMBOL, "name": "South African Rand", "decimal_places": 2}


# Export commonly used constants
TOP_STOCKS = sa_config.TOP_STOCKS
