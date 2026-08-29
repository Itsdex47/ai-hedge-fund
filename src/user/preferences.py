"""
Investment Preferences and Filtering System
Applies user preferences to filter and adjust investment recommendations.
"""

from typing import List, Dict, Optional, Set
from src.user.profile import UserProfile


class PreferenceFilter:
    """Filters investment opportunities based on user preferences."""

    # Common ESG sector exclusions
    ESG_SECTORS = {
        'tobacco': ['Tobacco'],
        'fossil_fuels': ['Oil & Gas', 'Coal', 'Energy'],
        'weapons': ['Defense', 'Aerospace & Defense'],
        'gambling': ['Gambling', 'Casinos & Gaming'],
        'alcohol': ['Alcoholic Beverages', 'Brewers'],
        'adult_entertainment': ['Adult Entertainment'],
        'private_prisons': ['Private Prisons'],
        'predatory_lending': ['Payday Lending']
    }

    # Common controversial companies (can be customized per user)
    CONTROVERSIAL_TICKERS = {
        'tobacco': ['MO', 'PM', 'BTI'],
        'fossil_fuels': ['XOM', 'CVX', 'COP', 'SLB', 'HAL', 'COAL'],
        'weapons': ['LMT', 'RTX', 'BA', 'NOC', 'GD'],
        'gambling': ['DKNG', 'PENN', 'LVS', 'MGM', 'WYNN', 'CZR'],
        'alcohol': ['BUD', 'TAP', 'STZ', 'SAM', 'DEO'],
    }

    def __init__(self, profile: UserProfile):
        """Initialize filter with user profile."""
        self.profile = profile

    def is_ticker_allowed(self, ticker: str) -> tuple[bool, Optional[str]]:
        """
        Check if ticker is allowed based on user preferences.

        Returns:
            (is_allowed, reason_if_not_allowed)
        """
        # Check explicit ticker exclusions
        if ticker.upper() in [t.upper() for t in self.profile.exclude_tickers]:
            return False, f"Ticker {ticker} is in your exclusion list"

        # Check sector-based exclusions
        if self.profile.exclude_sectors:
            for excluded_category in self.profile.exclude_sectors:
                excluded_tickers = self.CONTROVERSIAL_TICKERS.get(excluded_category.lower(), [])
                if ticker.upper() in excluded_tickers:
                    return False, f"Ticker {ticker} excluded due to {excluded_category} category"

        return True, None

    def adjust_position_size(
        self,
        ticker: str,
        recommended_size: float,
        current_portfolio: Optional[Dict] = None
    ) -> tuple[float, str]:
        """
        Adjust recommended position size based on user constraints.

        Args:
            ticker: Stock ticker
            recommended_size: Original recommended position size (dollars)
            current_portfolio: Current portfolio holdings

        Returns:
            (adjusted_size, reason_for_adjustment)
        """
        portfolio_value = self.profile.portfolio_value
        max_position = portfolio_value * (self.profile.max_position_size_pct / 100.0)

        # Check if recommendation exceeds max position size
        if recommended_size > max_position:
            return max_position, f"Reduced from ${recommended_size:,.0f} to max position size ({self.profile.max_position_size_pct}% of portfolio)"

        # Check sector concentration if portfolio provided
        if current_portfolio:
            # This would check sector concentration
            # Implementation depends on portfolio structure
            pass

        return recommended_size, "Position size approved"

    def get_crypto_allocation_limit(self) -> float:
        """Get maximum crypto allocation in dollars."""
        return self.profile.portfolio_value * (self.profile.max_crypto_allocation_pct / 100.0)

    def is_margin_allowed(self) -> bool:
        """Check if margin/leverage is allowed."""
        return self.profile.enable_margin

    def get_max_leverage(self) -> float:
        """Get maximum leverage ratio allowed."""
        return self.profile.max_leverage_ratio if self.profile.enable_margin else 0.0

    def should_apply_tax_optimization(self) -> Dict[str, bool]:
        """Get tax optimization preferences."""
        return {
            'tax_loss_harvesting': self.profile.tax_loss_harvesting_enabled,
            'prefer_long_term_gains': self.profile.prefer_long_term_gains,
            'tax_aware_rebalancing': self.profile.tax_aware_rebalancing
        }

    def get_risk_adjusted_allocation(self, base_allocation: Dict[str, float]) -> Dict[str, float]:
        """
        Adjust asset allocation based on risk tolerance.

        Args:
            base_allocation: Dict of asset_class -> weight

        Returns:
            Adjusted allocation based on risk profile
        """
        risk_multipliers = {
            'conservative': {
                'stocks': 0.6,
                'bonds': 1.5,
                'crypto': 0.0,
                'alternatives': 0.8
            },
            'moderate': {
                'stocks': 1.0,
                'bonds': 1.0,
                'crypto': 0.5,
                'alternatives': 1.0
            },
            'aggressive': {
                'stocks': 1.3,
                'bonds': 0.5,
                'crypto': 2.0,
                'alternatives': 1.2
            }
        }

        multipliers = risk_multipliers.get(self.profile.risk_tolerance, risk_multipliers['moderate'])

        adjusted = {}
        for asset_class, weight in base_allocation.items():
            multiplier = multipliers.get(asset_class, 1.0)
            adjusted[asset_class] = weight * multiplier

        # Normalize to sum to 1.0
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}

        return adjusted

    def filter_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Filter a list of stock recommendations based on user preferences.

        Args:
            recommendations: List of dicts with ticker, signal, confidence, etc.

        Returns:
            Filtered list of recommendations
        """
        filtered = []

        for rec in recommendations:
            ticker = rec.get('ticker')
            if not ticker:
                continue

            # Check if ticker is allowed
            is_allowed, reason = self.is_ticker_allowed(ticker)

            if is_allowed:
                # Adjust position size if provided
                if 'position_size' in rec:
                    adjusted_size, size_reason = self.adjust_position_size(
                        ticker,
                        rec['position_size']
                    )
                    rec['position_size'] = adjusted_size
                    rec['position_adjustment_reason'] = size_reason

                filtered.append(rec)
            else:
                # Add filtered-out recommendation with reason
                rec['filtered'] = True
                rec['filter_reason'] = reason
                filtered.append(rec)

        return filtered

    def get_preference_summary(self) -> Dict:
        """Get a summary of active preferences for display."""
        return {
            'risk_tolerance': self.profile.risk_tolerance,
            'time_horizon': f"{self.profile.time_horizon} years",
            'max_position_size': f"{self.profile.max_position_size_pct}%",
            'max_crypto_allocation': f"{self.profile.max_crypto_allocation_pct}%",
            'margin_enabled': self.profile.enable_margin,
            'excluded_sectors': self.profile.exclude_sectors if self.profile.exclude_sectors else "None",
            'excluded_tickers': self.profile.exclude_tickers if self.profile.exclude_tickers else "None",
            'values_based': self.profile.values_based_investing,
            'tax_optimization': self.profile.tax_loss_harvesting_enabled,
        }


def apply_preferences_to_signals(
    analyst_signals: Dict,
    profile: UserProfile,
    tickers: List[str]
) -> Dict:
    """
    Apply user preferences to filter and adjust analyst signals.

    Args:
        analyst_signals: Dict of analyst_name -> {ticker -> signal}
        profile: User profile with preferences
        tickers: List of tickers being analyzed

    Returns:
        Filtered and adjusted analyst signals
    """
    filter = PreferenceFilter(profile)

    # Check each ticker
    filtered_signals = {}

    for analyst, signals in analyst_signals.items():
        filtered_signals[analyst] = {}

        for ticker in tickers:
            if ticker not in signals:
                continue

            # Check if ticker is allowed
            is_allowed, reason = filter.is_ticker_allowed(ticker)

            if is_allowed:
                filtered_signals[analyst][ticker] = signals[ticker]
            else:
                # Mark as filtered
                signal = signals[ticker]
                if hasattr(signal, 'reasoning'):
                    # It's an AnalystSignal object
                    signal.signal = "FILTERED"
                    signal.confidence = 0.0
                    signal.reasoning = f"FILTERED: {reason}"
                else:
                    # It's a dict
                    signal['signal'] = "FILTERED"
                    signal['confidence'] = 0.0
                    signal['reasoning'] = f"FILTERED: {reason}"

                filtered_signals[analyst][ticker] = signal

    return filtered_signals


if __name__ == "__main__":
    # Demo: Test preference filtering
    from src.user.profile import get_profile

    print("="*60)
    print("Investment Preferences Filtering Demo")
    print("="*60)

    # Load ESG profile
    profile = get_profile("Balanced ESG")
    if not profile:
        print("Error: Profile not found. Run profile.py first to create example profiles.")
        exit(1)

    filter = PreferenceFilter(profile)

    # Show preference summary
    print("\n📋 Active Preferences:")
    summary = filter.get_preference_summary()
    for key, value in summary.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")

    # Test ticker filtering
    print("\n\n🔍 Ticker Filtering Test:")
    test_tickers = ['AAPL', 'MSFT', 'XOM', 'MO', 'GOOGL', 'LMT']

    for ticker in test_tickers:
        is_allowed, reason = filter.is_ticker_allowed(ticker)
        status = "✅ ALLOWED" if is_allowed else "❌ FILTERED"
        print(f"  {ticker}: {status}")
        if reason:
            print(f"    Reason: {reason}")

    # Test position sizing
    print("\n\n💰 Position Sizing Test:")
    portfolio_value = profile.portfolio_value
    print(f"  Portfolio Value: ${portfolio_value:,.0f}")
    print(f"  Max Position Size: {profile.max_position_size_pct}% = ${portfolio_value * 0.10:,.0f}")

    test_sizes = [50000, 150000, 250000]
    for size in test_sizes:
        adjusted, reason = filter.adjust_position_size('AAPL', size)
        print(f"\n  Recommended: ${size:,.0f}")
        print(f"  Adjusted:    ${adjusted:,.0f}")
        print(f"  Reason:      {reason}")

    # Test crypto allocation
    print("\n\n🪙 Crypto Allocation Limit:")
    crypto_limit = filter.get_crypto_allocation_limit()
    print(f"  Max Crypto: {profile.max_crypto_allocation_pct}% = ${crypto_limit:,.0f}")

    # Test risk-adjusted allocation
    print("\n\n📊 Risk-Adjusted Allocation:")
    base_allocation = {
        'stocks': 0.60,
        'bonds': 0.30,
        'crypto': 0.05,
        'alternatives': 0.05
    }

    print(f"  Base Allocation:")
    for asset, weight in base_allocation.items():
        print(f"    {asset}: {weight*100:.1f}%")

    adjusted = filter.get_risk_adjusted_allocation(base_allocation)
    print(f"\n  Risk-Adjusted ({profile.risk_tolerance}):")
    for asset, weight in adjusted.items():
        print(f"    {asset}: {weight*100:.1f}%")
