"""
User Profile Management System
Stores investor preferences, risk tolerance, goals, and constraints.
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class InvestmentGoal(BaseModel):
    """Individual investment goal with timeline and target."""
    name: str
    target_amount: float
    target_date: str  # YYYY-MM-DD format
    priority: str = Field(default="medium")  # low, medium, high
    description: Optional[str] = None


class UserProfile(BaseModel):
    """Complete user investment profile."""

    # Basic Info
    profile_name: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

    # Financial Situation
    portfolio_value: float = Field(default=100000.0)
    annual_income: Optional[float] = None
    tax_bracket: Optional[float] = None  # e.g., 0.24 for 24%
    state: Optional[str] = None  # For state tax calculations

    # Risk Profile
    risk_tolerance: str = Field(default="moderate")  # conservative, moderate, aggressive
    time_horizon: int = Field(default=10)  # years
    liquidity_needs: str = Field(default="low")  # low, medium, high

    # Investment Preferences
    max_position_size_pct: float = Field(default=10.0)  # Max % in single stock
    max_sector_concentration_pct: float = Field(default=30.0)  # Max % in sector
    max_crypto_allocation_pct: float = Field(default=5.0)  # Max % in crypto
    enable_margin: bool = Field(default=False)
    max_leverage_ratio: float = Field(default=0.0)

    # ESG & Values
    exclude_sectors: List[str] = Field(default_factory=list)  # e.g., ["tobacco", "fossil_fuels"]
    exclude_tickers: List[str] = Field(default_factory=list)  # e.g., ["META", "TSLA"]
    require_esg_rating: Optional[str] = None  # "A", "B", "C" minimum
    values_based_investing: bool = Field(default=False)

    # Geographic Preferences
    geographic_focus: str = Field(default="global")  # us_only, developed, global, emerging
    prefer_domestic: float = Field(default=0.7)  # Preferred % in US stocks

    # Investment Goals
    goals: List[InvestmentGoal] = Field(default_factory=list)
    primary_objective: str = Field(default="wealth_growth")  # wealth_growth, income, preservation

    # Tax Preferences
    tax_loss_harvesting_enabled: bool = Field(default=True)
    prefer_long_term_gains: bool = Field(default=True)
    tax_aware_rebalancing: bool = Field(default=True)

    # Notification Preferences
    email_notifications: bool = Field(default=False)
    notification_threshold: float = Field(default=5.0)  # Alert on >5% price moves

    @field_validator('risk_tolerance')
    @classmethod
    def validate_risk_tolerance(cls, v):
        allowed = ['conservative', 'moderate', 'aggressive']
        if v not in allowed:
            raise ValueError(f'risk_tolerance must be one of {allowed}')
        return v

    @field_validator('primary_objective')
    @classmethod
    def validate_objective(cls, v):
        allowed = ['wealth_growth', 'income', 'preservation', 'balanced']
        if v not in allowed:
            raise ValueError(f'primary_objective must be one of {allowed}')
        return v

    def to_dict(self) -> Dict:
        """Convert profile to dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert profile to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Create profile from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'UserProfile':
        """Create profile from JSON string."""
        return cls.model_validate_json(json_str)


class ProfileManager:
    """Manages loading, saving, and updating user profiles."""

    def __init__(self, profiles_dir: Optional[str] = None):
        """Initialize profile manager with profiles directory."""
        if profiles_dir is None:
            # Default to ~/.ai-hedge-fund/profiles/
            home = Path.home()
            profiles_dir = home / ".ai-hedge-fund" / "profiles"

        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def save_profile(self, profile: UserProfile) -> str:
        """Save profile to disk. Returns file path."""
        # Sanitize profile name for filename
        filename = profile.profile_name.lower().replace(" ", "_").replace("/", "_")
        filepath = self.profiles_dir / f"{filename}.json"

        # Update last_updated timestamp
        profile.last_updated = datetime.now().isoformat()

        # Save to file
        with open(filepath, 'w') as f:
            f.write(profile.to_json())

        return str(filepath)

    def load_profile(self, profile_name: str) -> Optional[UserProfile]:
        """Load profile by name. Returns None if not found."""
        filename = profile_name.lower().replace(" ", "_").replace("/", "_")
        filepath = self.profiles_dir / f"{filename}.json"

        if not filepath.exists():
            return None

        with open(filepath, 'r') as f:
            json_data = f.read()

        return UserProfile.from_json(json_data)

    def list_profiles(self) -> List[str]:
        """List all available profile names."""
        profiles = []
        for filepath in self.profiles_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    profiles.append(data.get('profile_name', filepath.stem))
            except:
                continue

        return sorted(profiles)

    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile. Returns True if successful."""
        filename = profile_name.lower().replace(" ", "_").replace("/", "_")
        filepath = self.profiles_dir / f"{filename}.json"

        if filepath.exists():
            filepath.unlink()
            return True

        return False

    def create_default_profiles(self):
        """Create example profiles for common investor types."""

        # Conservative Retirement (Near retirement, preservation focused)
        conservative = UserProfile(
            profile_name="Conservative Retirement",
            portfolio_value=2000000.0,
            risk_tolerance="conservative",
            time_horizon=5,
            primary_objective="preservation",
            max_position_size_pct=5.0,
            max_sector_concentration_pct=20.0,
            max_crypto_allocation_pct=0.0,
            enable_margin=False,
            tax_loss_harvesting_enabled=True,
            prefer_long_term_gains=True,
            goals=[
                InvestmentGoal(
                    name="Retirement Income",
                    target_amount=80000.0,  # Annual income needed
                    target_date="2030-01-01",
                    priority="high",
                    description="Generate stable income for retirement"
                )
            ]
        )

        # Aggressive Growth (Young investor, long time horizon)
        aggressive = UserProfile(
            profile_name="Aggressive Growth",
            portfolio_value=500000.0,
            risk_tolerance="aggressive",
            time_horizon=20,
            primary_objective="wealth_growth",
            max_position_size_pct=15.0,
            max_sector_concentration_pct=40.0,
            max_crypto_allocation_pct=10.0,
            enable_margin=True,
            max_leverage_ratio=0.3,
            tax_loss_harvesting_enabled=True,
            goals=[
                InvestmentGoal(
                    name="Financial Independence",
                    target_amount=5000000.0,
                    target_date="2045-01-01",
                    priority="high",
                    description="Achieve financial independence"
                )
            ]
        )

        # Balanced ESG (Values-based, moderate risk)
        esg = UserProfile(
            profile_name="Balanced ESG",
            portfolio_value=1000000.0,
            risk_tolerance="moderate",
            time_horizon=15,
            primary_objective="balanced",
            max_position_size_pct=10.0,
            max_sector_concentration_pct=30.0,
            max_crypto_allocation_pct=3.0,
            values_based_investing=True,
            exclude_sectors=["tobacco", "fossil_fuels", "weapons", "gambling"],
            require_esg_rating="B",
            tax_loss_harvesting_enabled=True,
            goals=[
                InvestmentGoal(
                    name="Sustainable Wealth Growth",
                    target_amount=3000000.0,
                    target_date="2040-01-01",
                    priority="high",
                    description="Grow wealth while investing ethically"
                )
            ]
        )

        # Save all default profiles
        self.save_profile(conservative)
        self.save_profile(aggressive)
        self.save_profile(esg)

        return [conservative.profile_name, aggressive.profile_name, esg.profile_name]


# Convenience functions
def get_profile(profile_name: str) -> Optional[UserProfile]:
    """Load a profile by name."""
    manager = ProfileManager()
    return manager.load_profile(profile_name)


def save_profile(profile: UserProfile) -> str:
    """Save a profile. Returns file path."""
    manager = ProfileManager()
    return manager.save_profile(profile)


def list_profiles() -> List[str]:
    """List all available profile names."""
    manager = ProfileManager()
    return manager.list_profiles()


def create_default_profiles():
    """Create example profiles."""
    manager = ProfileManager()
    return manager.create_default_profiles()


if __name__ == "__main__":
    # Demo: Create and save example profiles
    print("Creating example user profiles...")
    manager = ProfileManager()
    profiles = manager.create_default_profiles()

    print(f"\n✅ Created {len(profiles)} example profiles:")
    for name in profiles:
        print(f"  - {name}")

    print(f"\n📁 Profiles saved to: {manager.profiles_dir}")

    # Demo: Load and display a profile
    print("\n" + "="*60)
    print("Example Profile: Aggressive Growth")
    print("="*60)

    profile = manager.load_profile("Aggressive Growth")
    if profile:
        print(f"\nRisk Tolerance: {profile.risk_tolerance}")
        print(f"Time Horizon: {profile.time_horizon} years")
        print(f"Primary Objective: {profile.primary_objective}")
        print(f"Max Crypto Allocation: {profile.max_crypto_allocation_pct}%")
        print(f"Margin Enabled: {profile.enable_margin}")
        print(f"\nInvestment Goals:")
        for goal in profile.goals:
            print(f"  - {goal.name}: ${goal.target_amount:,.0f} by {goal.target_date}")
