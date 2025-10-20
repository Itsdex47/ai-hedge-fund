"""
Cryptocurrency Data Module
Fetches crypto price data, market metrics, and institutional flow indicators.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time


class CryptoDataFetcher:
    """Fetches cryptocurrency data from CoinGecko API (free tier)."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    # Supported crypto symbols mapped to CoinGecko IDs
    CRYPTO_MAP = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "ADA": "cardano",
        "DOT": "polkadot",
        "AVAX": "avalanche-2",
        "MATIC": "matic-network",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "ATOM": "cosmos"
    }

    def __init__(self):
        """Initialize crypto data fetcher."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI-Hedge-Fund/1.0',
            'Accept': 'application/json'
        })

    def get_crypto_id(self, symbol: str) -> Optional[str]:
        """Convert crypto symbol to CoinGecko ID."""
        symbol_upper = symbol.upper()
        return self.CRYPTO_MAP.get(symbol_upper)

    def fetch_current_price(self, symbol: str) -> Dict:
        """
        Fetch current price and key metrics for a cryptocurrency.

        Args:
            symbol: Crypto symbol (BTC, ETH, etc.)

        Returns:
            Dict with current price, market cap, volume, etc.
        """
        crypto_id = self.get_crypto_id(symbol)
        if not crypto_id:
            raise ValueError(f"Unsupported crypto symbol: {symbol}")

        endpoint = f"{self.BASE_URL}/coins/{crypto_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'false',
            'developer_data': 'false'
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            market_data = data.get('market_data', {})

            return {
                'symbol': symbol,
                'name': data.get('name'),
                'current_price': market_data.get('current_price', {}).get('usd'),
                'market_cap': market_data.get('market_cap', {}).get('usd'),
                'market_cap_rank': data.get('market_cap_rank'),
                'total_volume': market_data.get('total_volume', {}).get('usd'),
                'high_24h': market_data.get('high_24h', {}).get('usd'),
                'low_24h': market_data.get('low_24h', {}).get('usd'),
                'price_change_24h': market_data.get('price_change_24h'),
                'price_change_percentage_24h': market_data.get('price_change_percentage_24h'),
                'price_change_percentage_7d': market_data.get('price_change_percentage_7d'),
                'price_change_percentage_30d': market_data.get('price_change_percentage_30d'),
                'price_change_percentage_1y': market_data.get('price_change_percentage_1y'),
                'ath': market_data.get('ath', {}).get('usd'),  # All-time high
                'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd'),
                'ath_date': market_data.get('ath_date', {}).get('usd'),
                'atl': market_data.get('atl', {}).get('usd'),  # All-time low
                'atl_change_percentage': market_data.get('atl_change_percentage', {}).get('usd'),
                'circulating_supply': market_data.get('circulating_supply'),
                'total_supply': market_data.get('total_supply'),
                'max_supply': market_data.get('max_supply'),
                'last_updated': data.get('last_updated'),
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return None

    def fetch_historical_data(self, symbol: str, days: int = 365) -> List[Dict]:
        """
        Fetch historical price data for a cryptocurrency.

        Args:
            symbol: Crypto symbol (BTC, ETH, etc.)
            days: Number of days of history (max 365 for free tier)

        Returns:
            List of dicts with date, price, market_cap, total_volume
        """
        crypto_id = self.get_crypto_id(symbol)
        if not crypto_id:
            raise ValueError(f"Unsupported crypto symbol: {symbol}")

        endpoint = f"{self.BASE_URL}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            prices = data.get('prices', [])
            market_caps = data.get('market_caps', [])
            volumes = data.get('total_volumes', [])

            historical_data = []
            for i in range(len(prices)):
                historical_data.append({
                    'date': datetime.fromtimestamp(prices[i][0] / 1000).strftime('%Y-%m-%d'),
                    'price': prices[i][1],
                    'market_cap': market_caps[i][1] if i < len(market_caps) else None,
                    'volume': volumes[i][1] if i < len(volumes) else None
                })

            return historical_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return []

    def fetch_market_overview(self) -> Dict:
        """
        Fetch overall crypto market metrics.

        Returns:
            Dict with total market cap, BTC dominance, ETH dominance, etc.
        """
        endpoint = f"{self.BASE_URL}/global"

        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            data = response.json().get('data', {})

            return {
                'total_market_cap': data.get('total_market_cap', {}).get('usd'),
                'total_volume_24h': data.get('total_volume', {}).get('usd'),
                'btc_dominance': data.get('market_cap_percentage', {}).get('btc'),
                'eth_dominance': data.get('market_cap_percentage', {}).get('eth'),
                'market_cap_change_24h': data.get('market_cap_change_percentage_24h_usd'),
                'active_cryptocurrencies': data.get('active_cryptocurrencies'),
                'markets': data.get('markets'),
                'updated_at': data.get('updated_at'),
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching market overview: {e}")
            return None

    def fetch_fear_greed_index(self) -> Dict:
        """
        Fetch Crypto Fear & Greed Index (separate API).

        Returns:
            Dict with current fear/greed value and classification
        """
        endpoint = "https://api.alternative.me/fng/"

        try:
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            data = response.json().get('data', [])[0]

            return {
                'value': int(data.get('value')),
                'value_classification': data.get('value_classification'),
                'timestamp': data.get('timestamp'),
                'time_until_update': data.get('time_until_update')
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fear/greed index: {e}")
            return None

    def get_institutional_signals(self, symbol: str) -> Dict:
        """
        Analyze institutional interest signals for crypto.

        Args:
            symbol: Crypto symbol (BTC, ETH, etc.)

        Returns:
            Dict with institutional signals
        """
        current_data = self.fetch_current_price(symbol)
        if not current_data:
            return {}

        # Calculate institutional interest indicators
        volume_to_mcap_ratio = (
            current_data['total_volume'] / current_data['market_cap']
            if current_data.get('market_cap') and current_data.get('total_volume')
            else 0
        )

        # High volume/mcap ratio suggests institutional activity
        institutional_interest = "HIGH" if volume_to_mcap_ratio > 0.05 else "MEDIUM" if volume_to_mcap_ratio > 0.02 else "LOW"

        # Distance from ATH (institutions buy dips)
        ath_discount = current_data.get('ath_change_percentage', 0)
        buying_opportunity = "STRONG" if ath_discount < -50 else "MODERATE" if ath_discount < -30 else "WEAK"

        return {
            'symbol': symbol,
            'volume_to_mcap_ratio': volume_to_mcap_ratio,
            'institutional_interest': institutional_interest,
            'ath_discount_percent': ath_discount,
            'buying_opportunity_rating': buying_opportunity,
            'market_cap_rank': current_data.get('market_cap_rank'),
            'is_top_10': current_data.get('market_cap_rank', 999) <= 10
        }


# Convenience function for easy imports
def get_crypto_data(symbol: str) -> Dict:
    """
    Quick function to get current crypto data.

    Args:
        symbol: Crypto symbol (BTC, ETH, etc.)

    Returns:
        Dict with current price and metrics
    """
    fetcher = CryptoDataFetcher()
    return fetcher.fetch_current_price(symbol)


def get_crypto_historical(symbol: str, days: int = 90) -> List[Dict]:
    """
    Quick function to get historical crypto data.

    Args:
        symbol: Crypto symbol (BTC, ETH, etc.)
        days: Number of days of history

    Returns:
        List of historical data points
    """
    fetcher = CryptoDataFetcher()
    return fetcher.fetch_historical_data(symbol, days)
