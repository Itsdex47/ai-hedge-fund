#!/usr/bin/env python3
"""
Test script for South African market configuration
Verifies that all SA-specific components are working correctly
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_sa_config():
    """Test SA market configuration"""
    print("🇿🇦 Testing South African Market Configuration")
    print("=" * 50)

    try:
        # Test 1: Import SA config
        print("1. Testing SA Market Config Import...")
        from config.sa_market_config import get_sa_config, is_jse_ticker, get_zar_currency_info

        sa_config = get_sa_config()
        print("   ✅ SA config imported successfully")

        # Test 2: Check basic config values
        print("2. Testing Basic Config Values...")
        assert sa_config.CURRENCY == "ZAR"
        assert sa_config.EXCHANGE_NAME == "JSE"
        assert sa_config.REGULATORY_BODY == "FSCA"
        print("   ✅ Basic config values correct")

        # Test 3: Test JSE ticker validation
        print("3. Testing JSE Ticker Validation...")
        valid_tickers = ["NPN", "SBK", "MTN", "VOD"]
        invalid_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]

        for ticker in valid_tickers:
            assert is_jse_ticker(ticker), f"Valid ticker {ticker} failed validation"

        for ticker in invalid_tickers:
            assert not is_jse_ticker(ticker), f"Invalid ticker {ticker} passed validation"

        print("   ✅ JSE ticker validation working")

        # Test 4: Test currency info
        print("4. Testing Currency Info...")
        currency_info = get_zar_currency_info()
        assert currency_info["code"] == "ZAR"
        assert currency_info["symbol"] == "R"
        print("   ✅ Currency info correct")

        # Test 5: Import SA data adapter
        print("5. Testing SA Data Adapter Import...")
        from data.sa_data_adapter import get_sa_data_adapter

        sa_adapter = get_sa_data_adapter()
        print("   ✅ SA data adapter imported successfully")

        # Test 6: Test SA agents import
        print("6. Testing SA Agents Import...")
        from agents.sa_market_analyst import sa_market_analyst_agent, sa_regulatory_compliance_agent, sa_currency_risk_agent

        print("   ✅ SA agents imported successfully")

        # Test 7: Test SA main script
        print("7. Testing SA Main Script Import...")
        from sa_main import main

        print("   ✅ SA main script imported successfully")

        # Test 8: Test SA backtester
        print("8. Testing SA Backtester Import...")
        from sa_backtester import main as sa_backtest_main

        print("   ✅ SA backtester imported successfully")

        # Test 9: Check top stocks
        print("9. Testing Top JSE Stocks...")
        assert len(sa_config.TOP_STOCKS) >= 20, "Should have at least 20 top stocks"
        print(f"   ✅ Found {len(sa_config.TOP_STOCKS)} top JSE stocks")

        # Test 10: Check sectors
        print("10. Testing SA Sectors...")
        assert len(sa_config.SECTORS) >= 10, "Should have at least 10 sectors"
        print(f"   ✅ Found {len(sa_config.SECTORS)} SA sectors")

        # Test 11: Check risk factors
        print("11. Testing SA Risk Factors...")
        assert len(sa_config.RISK_FACTORS) >= 5, "Should have at least 5 risk factors"
        print(f"   ✅ Found {len(sa_config.RISK_FACTORS)} SA risk factors")

        # Test 12: Check economic indicators
        print("12. Testing SA Economic Indicators...")
        assert len(sa_config.ECONOMIC_INDICATORS) >= 5, "Should have at least 5 economic indicators"
        print(f"   ✅ Found {len(sa_config.ECONOMIC_INDICATORS)} SA economic indicators")

        print("\n" + "=" * 50)
        print("🎉 All SA Configuration Tests Passed!")
        print("=" * 50)

        # Display summary
        print(f"\n📊 SA Market Summary:")
        print(f"   Currency: {sa_config.CURRENCY} ({sa_config.CURRENCY_SYMBOL})")
        print(f"   Exchange: {sa_config.EXCHANGE_NAME}")
        print(f"   Trading Hours: {sa_config.TRADING_START_TIME} - {sa_config.TRADING_END_TIME} SAST")
        print(f"   Settlement: T+{sa_config.SETTLEMENT_DAYS}")
        print(f"   Regulatory Body: {sa_config.REGULATORY_BODY}")
        print(f"   Top Stocks: {len(sa_config.TOP_STOCKS)}")
        print(f"   Sectors: {len(sa_config.SECTORS)}")
        print(f"   Risk Factors: {len(sa_config.RISK_FACTORS)}")
        print(f"   Economic Indicators: {len(sa_config.ECONOMIC_INDICATORS)}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_sa_data_adapter():
    """Test SA data adapter functionality"""
    print("\n🔧 Testing SA Data Adapter Functionality")
    print("=" * 50)

    try:
        from data.sa_data_adapter import get_sa_data_adapter

        sa_adapter = get_sa_data_adapter()

        # Test economic indicators
        print("1. Testing Economic Indicators...")
        indicators = sa_adapter.get_sa_economic_indicators()
        assert isinstance(indicators, dict)
        assert "SA_CPI" in indicators
        assert "SA_REPO_RATE" in indicators
        print("   ✅ Economic indicators working")

        # Test FX rates
        print("2. Testing FX Rates...")
        fx_rates = sa_adapter.get_zar_fx_rates()
        assert isinstance(fx_rates, dict)
        assert "USDZAR" in fx_rates
        assert "EURZAR" in fx_rates
        print("   ✅ FX rates working")

        # Test sector mapping
        print("3. Testing Sector Mapping...")
        sector = sa_adapter.get_sa_sector_exposure("NPN")
        assert sector == "Technology"
        sector = sa_adapter.get_sa_sector_exposure("SBK")
        assert sector == "Financial Services"
        print("   ✅ Sector mapping working")

        # Test ticker validation
        print("4. Testing Ticker Validation...")
        assert sa_adapter.validate_sa_ticker("NPN")
        assert sa_adapter.validate_sa_ticker("SBK")
        assert not sa_adapter.validate_sa_ticker("AAPL")
        print("   ✅ Ticker validation working")

        print("\n✅ All SA Data Adapter Tests Passed!")
        return True

    except Exception as e:
        print(f"❌ SA Data Adapter test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🇿🇦 South African AI Hedge Fund - Configuration Test")
    print("=" * 60)

    # Run tests
    config_test = test_sa_config()
    adapter_test = test_sa_data_adapter()

    if config_test and adapter_test:
        print("\n🎉 All tests passed! SA configuration is ready.")
        print("\nNext steps:")
        print("1. Set up your API keys in .env file")
        print("2. Run: python src/sa_main.py --ticker NPN,SBK,MTN,VOD")
        print("3. Or run: python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
