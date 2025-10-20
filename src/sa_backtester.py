"""
South African Backtester
Specialized backtesting for JSE (Johannesburg Stock Exchange) market
"""

import sys
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd

from src.backtester import Backtester
from src.config.sa_market_config import get_sa_config, TOP_STOCKS
from src.data.sa_data_adapter import get_sa_data_adapter
from src.main import run_hedge_fund

# Load environment variables
load_dotenv()


def main():
    """Main entry point for South African Backtester"""

    parser = argparse.ArgumentParser(
        description="South African AI Hedge Fund Backtester - JSE Market",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backtest top JSE stocks
  python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD
  
  # Backtest with custom date range
  python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --start-date 2023-01-01 --end-date 2024-01-01
  
  # Use local Ollama models
  python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --ollama
  
  # Show detailed reasoning
  python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --show-reasoning
  
  # SA-only agents
  python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --sa-only
        """,
    )

    parser.add_argument("--ticker", type=str, default=",".join(TOP_STOCKS[:5]), help=f"Comma-separated list of JSE tickers (default: {','.join(TOP_STOCKS[:5])})")  # Default to top 5 JSE stocks

    parser.add_argument("--start-date", type=str, default=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"), help="Start date for backtesting (YYYY-MM-DD)")

    parser.add_argument("--end-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="End date for backtesting (YYYY-MM-DD)")

    parser.add_argument("--ollama", action="store_true", help="Use local Ollama models instead of cloud LLMs")

    parser.add_argument("--show-reasoning", action="store_true", help="Show detailed reasoning from each agent")

    parser.add_argument("--model-name", type=str, default="gpt-4o-mini" if not parser.parse_args().ollama else "llama3.1:8b", help="LLM model to use")

    parser.add_argument("--model-provider", type=str, default="OpenAI" if not parser.parse_args().ollama else "Ollama", help="LLM provider to use")

    parser.add_argument("--sa-only", action="store_true", help="Use only SA-specific agents (exclude global agents)")

    parser.add_argument("--initial-capital", type=float, default=1000000, help="Initial capital in ZAR")  # 1M ZAR

    args = parser.parse_args()

    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]

    # Validate JSE tickers
    sa_data_adapter = get_sa_data_adapter()
    valid_tickers = []
    invalid_tickers = []

    for ticker in tickers:
        if sa_data_adapter.validate_sa_ticker(ticker):
            valid_tickers.append(ticker)
        else:
            invalid_tickers.append(ticker)

    if invalid_tickers:
        print(f"⚠️  Warning: Invalid JSE tickers: {', '.join(invalid_tickers)}")
        print(f"Valid JSE tickers: {', '.join(TOP_STOCKS)}")

    if not valid_tickers:
        print("❌ No valid JSE tickers provided. Exiting.")
        sys.exit(1)

    print(f"🇿🇦 South African AI Hedge Fund Backtester")
    print(f"📊 Backtesting: {', '.join(valid_tickers)}")
    print(f"📅 Date Range: {args.start_date} to {args.end_date}")
    print(f"💰 Initial Capital: R{args.initial_capital:,.2f}")
    print(f"🤖 Model: {args.model_name} ({args.model_provider})")
    print(f"🔍 Show Reasoning: {args.show_reasoning}")
    print(f"🇿🇦 SA-Only Mode: {args.sa_only}")
    print("-" * 60)

    # Select agents based on SA-only mode
    if args.sa_only:
        selected_analysts = ["sa_market_analyst", "sa_regulatory_compliance", "sa_currency_risk", "portfolio_manager"]
        print("🎯 Using SA-specific agents only")
    else:
        selected_analysts = []  # Use all agents
        print("🌍 Using all agents (global + SA-specific)")

    try:
        print("🔄 Running SA Market Backtest...")
        backtester = Backtester(
            agent=run_hedge_fund,
            tickers=valid_tickers,
            start_date=args.start_date,
            end_date=args.end_date,
            initial_capital=args.initial_capital,
            model_name=args.model_name,
            model_provider=args.model_provider,
            selected_analysts=selected_analysts,
            initial_margin_requirement=0.0,
        )
        performance_metrics = backtester.run_backtest()

        # Analyze performance to get detailed results
        performance_df = backtester.analyze_performance()

        # Display SA-specific backtest results
        print("\n" + "=" * 60)
        print("🇿🇦 SOUTH AFRICAN BACKTEST RESULTS")
        print("=" * 60)

        if len(backtester.portfolio_values) > 0:
            final_value = backtester.portfolio_values[-1]["Portfolio Value"]
            initial_value = args.initial_capital
            total_return = ((final_value - initial_value) / initial_value) * 100

            print(f"\n💰 Portfolio Performance:")
            print(f"  Initial Capital: R{initial_value:,.2f}")
            print(f"  Final Value: R{final_value:,.2f}")
            print(f"  Total Return: {total_return:+.2f}%")

            # Convert to USD for comparison (approximate)
            zar_usd_rate = 18.45  # Approximate rate
            usd_initial = initial_value / zar_usd_rate
            usd_final = final_value / zar_usd_rate
            print(f"  USD Equivalent: ${usd_initial:,.2f} → ${usd_final:,.2f}")

            # Display performance metrics
            if performance_metrics:
                print(f"\n📈 Performance Metrics:")
                if performance_metrics.get("sharpe_ratio") is not None:
                    print(f"  Sharpe Ratio: {performance_metrics['sharpe_ratio']:.2f}")
                if performance_metrics.get("sortino_ratio") is not None:
                    print(f"  Sortino Ratio: {performance_metrics['sortino_ratio']:.2f}")
                if performance_metrics.get("max_drawdown") is not None:
                    print(f"  Max Drawdown: {performance_metrics['max_drawdown']:.2f}%")

        # SA Market Context
        sa_config = get_sa_config()
        print(f"\n🇿🇦 SA Market Context:")
        print(f"  Currency: {sa_config.CURRENCY} ({sa_config.CURRENCY_SYMBOL})")
        print(f"  Exchange: {sa_config.EXCHANGE_NAME}")
        print(f"  Trading Hours: {sa_config.TRADING_START_TIME} - {sa_config.TRADING_END_TIME} SAST")
        print(f"  Settlement: T+{sa_config.SETTLEMENT_DAYS}")
        print(f"  Max Position Size: {sa_config.MAX_POSITION_SIZE:.1%}")
        print(f"  Max Sector Exposure: {sa_config.MAX_SECTOR_EXPOSURE:.1%}")
        print(f"  Stop Loss: {sa_config.STOP_LOSS_PERCENTAGE:.1%}")

        # Risk Analysis
        print(f"\n⚠️  SA Risk Factors Considered:")
        for risk in sa_config.RISK_FACTORS:
            print(f"  • {risk}")

        print("\n✅ Backtest complete!")

    except Exception as e:
        print(f"❌ Error during SA backtest: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
