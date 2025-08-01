"""
South African Data Adapter
Handles JSE-specific data sources and market characteristics
"""

import os
import requests
import pandas as pd
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import time

from src.config.sa_market_config import get_sa_config, is_jse_ticker
from src.data.models import Price, FinancialMetrics, CompanyNews, CompanyFacts
from src.data.cache import get_cache

# Global cache instance
_cache = get_cache()
sa_config = get_sa_config()


class SADataAdapter:
    """Adapter for South African market data sources"""

    def __init__(self):
        self.config = sa_config
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AI-Hedge-Fund-SA/1.0"})

    def get_jse_prices(self, ticker: str, start_date: str, end_date: str) -> List[Price]:
        """Get JSE price data with SA-specific handling"""

        # Validate JSE ticker format
        if not is_jse_ticker(ticker):
            raise ValueError(f"Invalid JSE ticker format: {ticker}")

        # Create cache key
        cache_key = f"JSE_{ticker}_{start_date}_{end_date}"

        # Check cache first
        if cached_data := _cache.get_prices(cache_key):
            return [Price(**price) for price in cached_data]

        # Fetch from API with JSE-specific parameters
        headers = {}
        financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
        if financial_api_key:
            headers["X-API-KEY"] = financial_api_key

        # Try different JSE ticker formats
        ticker_formats = [
            ticker,  # Try original format first
            f"JSE:{ticker}",  # Try JSE: prefix
            f"{ticker}.JSE",  # Try .JSE suffix
            f"{ticker}.JO",  # Try .JO suffix (Johannesburg)
        ]

        for ticker_format in ticker_formats:
            try:
                url = f"{self.config.DATA_SOURCES['prices']}?ticker={ticker_format}&interval=day&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                continue

        # If all formats fail, return empty data
        return {"prices": []}

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            prices = []

            for price_data in data.get("prices", []):
                # Convert to ZAR if needed
                price_data["currency"] = "ZAR"
                prices.append(Price(**price_data))

            # Cache results
            _cache.set_prices(cache_key, [p.model_dump() for p in prices])
            return prices

        except requests.RequestException as e:
            print(f"Error fetching JSE data for {ticker}: {e}")
            return []

    def get_sa_financial_metrics(self, ticker: str, end_date: str, period: str = "ttm") -> List[FinancialMetrics]:
        """Get SA-specific financial metrics"""

        cache_key = f"JSE_FIN_{ticker}_{end_date}_{period}"

        if cached_data := _cache.get_financial_metrics(cache_key):
            return [FinancialMetrics(**metric) for metric in cached_data]

        headers = {}
        financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
        if financial_api_key:
            headers["X-API-KEY"] = financial_api_key

        jse_ticker = f"JSE:{ticker}"
        url = f"{self.config.DATA_SOURCES['fundamentals']}?ticker={jse_ticker}&end_date={end_date}&period={period}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            metrics = []

            for metric_data in data.get("financial_metrics", []):
                metric_data["currency"] = "ZAR"
                metrics.append(FinancialMetrics(**metric_data))

            _cache.set_financial_metrics(cache_key, [m.model_dump() for m in metrics])
            return metrics

        except requests.RequestException as e:
            print(f"Error fetching SA financial metrics for {ticker}: {e}")
            return []

    def get_sa_news(self, ticker: str, end_date: str, start_date: Optional[str] = None) -> List[CompanyNews]:
        """Get SA-specific news with local sources"""

        cache_key = f"JSE_NEWS_{ticker}_{end_date}_{start_date or 'all'}"

        if cached_data := _cache.get_news(cache_key):
            return [CompanyNews(**news) for news in cached_data]

        headers = {}
        financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
        if financial_api_key:
            headers["X-API-KEY"] = financial_api_key

        jse_ticker = f"JSE:{ticker}"
        url = f"{self.config.DATA_SOURCES['news']}?ticker={jse_ticker}&end_date={end_date}"
        if start_date:
            url += f"&start_date={start_date}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            news_items = []

            for news_data in data.get("news", []):
                # Add SA-specific sentiment analysis
                news_data["sentiment"] = self._analyze_sa_sentiment(news_data.get("title", ""))
                news_items.append(CompanyNews(**news_data))

            _cache.set_news(cache_key, [n.model_dump() for n in news_items])
            return news_items

        except requests.RequestException as e:
            print(f"Error fetching SA news for {ticker}: {e}")
            return []

    def get_sa_company_facts(self, ticker: str) -> Optional[CompanyFacts]:
        """Get SA company information"""

        cache_key = f"JSE_FACTS_{ticker}"

        if cached_data := _cache.get_company_facts(cache_key):
            return CompanyFacts(**cached_data)

        headers = {}
        financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
        if financial_api_key:
            headers["X-API-KEY"] = financial_api_key

        jse_ticker = f"JSE:{ticker}"
        url = f"{self.config.DATA_SOURCES['company_facts']}?ticker={jse_ticker}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            company_facts = data.get("company_facts", {})
            company_facts["exchange"] = "JSE"
            company_facts["currency"] = "ZAR"

            facts = CompanyFacts(**company_facts)
            _cache.set_company_facts(cache_key, facts.model_dump())
            return facts

        except requests.RequestException as e:
            print(f"Error fetching SA company facts for {ticker}: {e}")
            return None

    def get_sa_market_data(self, indices: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get SA market overview data"""

        if indices is None:
            indices = self.config.MAJOR_INDICES[:3]  # Top 3 indices

        market_data = {}

        for index in indices:
            cache_key = f"JSE_INDEX_{index}"

            if cached_data := _cache.get_prices(cache_key):
                market_data[index] = cached_data
                continue

            # Fetch index data
            headers = {}
            financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
            if financial_api_key:
                headers["X-API-KEY"] = financial_api_key

            url = f"{self.config.DATA_SOURCES['prices']}?ticker={index}&interval=day&interval_multiplier=1&start_date={datetime.now().strftime('%Y-%m-%d')}&end_date={datetime.now().strftime('%Y-%m-%d')}"

            try:
                response = self.session.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                market_data[index] = data.get("prices", [])
                _cache.set_prices(cache_key, data.get("prices", []))

            except requests.RequestException as e:
                print(f"Error fetching SA market data for {index}: {e}")
                market_data[index] = []

        return market_data

    def get_sa_economic_indicators(self) -> Dict[str, float]:
        """Get SA economic indicators"""

        cache_key = "SA_ECONOMIC_INDICATORS"

        if cached_data := _cache.get_economic_indicators(cache_key):
            return cached_data

        # This would integrate with SA-specific economic data APIs
        # For now, return placeholder data
        indicators = {
            "SA_CPI": 5.2,  # Consumer Price Index
            "SA_REPO_RATE": 8.25,  # Repo Rate
            "SA_GDP_GROWTH": 1.8,  # GDP Growth
            "SA_UNEMPLOYMENT": 32.1,  # Unemployment Rate
            "SA_CURRENT_ACCOUNT": -2.1,  # Current Account % of GDP
            "SA_BUDGET_DEFICIT": -4.9,  # Budget Deficit % of GDP
        }

        _cache.set_economic_indicators(cache_key, indicators)
        return indicators

    def get_zar_fx_rates(self) -> Dict[str, float]:
        """Get ZAR exchange rates"""

        cache_key = "ZAR_FX_RATES"

        if cached_data := _cache.get_fx_rates(cache_key):
            return cached_data

        # This would integrate with FX data APIs
        # For now, return placeholder data
        fx_rates = {
            "USDZAR": 18.45,
            "EURZAR": 20.12,
            "GBPZAR": 23.67,
            "JPYZAR": 0.123,
            "CNYZAR": 2.56,
        }

        _cache.set_fx_rates(cache_key, fx_rates)
        return fx_rates

    def _analyze_sa_sentiment(self, text: str) -> str:
        """Analyze sentiment for SA-specific context"""

        # Simple keyword-based sentiment analysis for SA context
        positive_words = ["growth", "profit", "dividend", "expansion", "recovery", "rand", "zar", "jse", "johannesburg", "south africa"]

        negative_words = ["load shedding", "eskom", "corruption", "strike", "protest", "inflation", "recession", "debt", "default"]

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def validate_sa_ticker(self, ticker: str) -> bool:
        """Validate if ticker is valid for SA market"""
        return is_jse_ticker(ticker) and ticker in self.config.TOP_STOCKS

    def get_sa_sector_exposure(self, ticker: str) -> Optional[str]:
        """Get sector exposure for SA stock"""

        # SA sector mapping (simplified)
        sector_mapping = {
            # Financial Services
            "SBK": "Financial Services",
            "FSR": "Financial Services",
            "NED": "Financial Services",
            "ABG": "Financial Services",
            # Mining & Resources
            "BHP": "Mining & Resources",
            "AGL": "Mining & Resources",
            "SOL": "Mining & Resources",
            "IMP": "Mining & Resources",
            "ANG": "Mining & Resources",
            "AMS": "Mining & Resources",
            # Consumer Goods
            "SHP": "Consumer Goods",
            "WHL": "Consumer Goods",
            "TBS": "Consumer Goods",
            "BID": "Consumer Goods",
            "TFG": "Consumer Goods",
            "MRP": "Consumer Goods",
            "CLS": "Consumer Goods",
            # Telecommunications
            "MTN": "Telecommunications",
            "VOD": "Telecommunications",
            # Technology
            "NPN": "Technology",
        }

        return sector_mapping.get(ticker)


# Global instance
sa_data_adapter = SADataAdapter()


def get_sa_data_adapter() -> SADataAdapter:
    """Get the South African data adapter instance"""
    return sa_data_adapter
