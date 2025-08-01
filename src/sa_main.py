"""
South African AI Hedge Fund Main Script
Specialized version for JSE (Johannesburg Stock Exchange) market
"""

import sys
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv

from src.main import run_hedge_fund
from src.backtester import Backtester
from src.config.sa_market_config import get_sa_config, TOP_STOCKS
from src.data.sa_data_adapter import get_sa_data_adapter

# Load environment variables
load_dotenv()


def main():
    """Main entry point for South African AI Hedge Fund"""

    parser = argparse.ArgumentParser(
        description="South African AI Hedge Fund - JSE Market Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze top JSE stocks
  python src/sa_main.py --ticker NPN,SBK,MTN,VOD
  
  # Run with SA-specific backtesting
  python src/sa_main.py --ticker NPN,SBK,MTN,VOD --backtest
  
  # Use local Ollama models
  python src/sa_main.py --ticker NPN,SBK,MTN,VOD --ollama
  
  # Show detailed reasoning
  python src/sa_main.py --ticker NPN,SBK,MTN,VOD --show-reasoning
  
  # Custom date range
  python src/sa_main.py --ticker NPN,SBK,MTN,VOD --start-date 2024-01-01 --end-date 2024-03-01
        """,
    )

    parser.add_argument("--ticker", type=str, default=",".join(TOP_STOCKS[:5]), help=f"Comma-separated list of JSE tickers (default: {','.join(TOP_STOCKS[:5])})")  # Default to top 5 JSE stocks

    parser.add_argument("--start-date", type=str, default=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), help="Start date for analysis (YYYY-MM-DD)")

    parser.add_argument("--end-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="End date for analysis (YYYY-MM-DD)")

    parser.add_argument("--backtest", action="store_true", help="Run backtesting instead of live analysis")

    parser.add_argument("--ollama", action="store_true", help="Use local Ollama models instead of cloud LLMs")

    parser.add_argument("--show-reasoning", action="store_true", help="Show detailed reasoning from each agent")

    parser.add_argument("--model-name", type=str, default="gpt-4o-mini" if not parser.parse_args().ollama else "llama3.1:8b", help="LLM model to use")

    parser.add_argument("--model-provider", type=str, default="OpenAI" if not parser.parse_args().ollama else "Ollama", help="LLM provider to use")

    parser.add_argument("--sa-only", action="store_true", help="Use only SA-specific agents (exclude global agents)")

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

    print(f"🇿🇦 South African AI Hedge Fund - JSE Market Analysis")
    print(f"📊 Analyzing: {', '.join(valid_tickers)}")
    print(f"📅 Date Range: {args.start_date} to {args.end_date}")
    print(f"🤖 Model: {args.model_name} ({args.model_provider})")
    print(f"🔍 Show Reasoning: {args.show_reasoning}")
    print(f"🇿🇦 SA-Only Mode: {args.sa_only}")
    print("-" * 60)

    # Initialize portfolio
    portfolio = {"total_cash": 1000000, "positions": {}}  # 1M ZAR starting capital

    # Select agents based on SA-only mode
    if args.sa_only:
        selected_analysts = ["sa_market_analyst", "sa_regulatory_compliance", "sa_currency_risk", "portfolio_manager"]
        print("🎯 Using SA-specific agents only")
    else:
        selected_analysts = []  # Use all agents
        print("🌍 Using all agents (global + SA-specific)")

    try:
        if args.backtest:
            print("🔄 Running SA Market Backtest...")
            backtester = Backtester(tickers=valid_tickers, start_date=args.start_date, end_date=args.end_date, portfolio=portfolio, show_reasoning=args.show_reasoning, selected_analysts=selected_analysts, model_name=args.model_name, model_provider=args.model_provider)
            results = backtester.run_backtest()
        else:
            print("📈 Running SA Market Analysis...")
            results = run_hedge_fund(tickers=valid_tickers, start_date=args.start_date, end_date=args.end_date, portfolio=portfolio, show_reasoning=args.show_reasoning, selected_analysts=selected_analysts, model_name=args.model_name, model_provider=args.model_provider)

        # Display SA-specific results
        print("\n" + "=" * 60)
        print("🇿🇦 SOUTH AFRICAN MARKET ANALYSIS RESULTS")
        print("=" * 60)

        if "decisions" in results:
            decisions = results["decisions"]
            if decisions and "trades" in decisions:
                print(f"\n📊 Trading Decisions:")
                for trade in decisions["trades"]:
                    ticker = trade.get("ticker", "Unknown")
                    action = trade.get("action", "Unknown")
                    shares = trade.get("shares", 0)
                    price = trade.get("price", 0)
                    print(f"  {ticker}: {action} {shares} shares @ R{price:.2f}")

        if "analyst_signals" in results:
            print(f"\n🤖 Agent Signals:")
            for agent_name, signals in results["analyst_signals"].items():
                if agent_name.startswith("sa_"):
                    print(f"  {agent_name.upper()}:")
                    for ticker, signal in signals.items():
                        if hasattr(signal, "signal"):
                            print(f"    {ticker}: {signal.signal} (confidence: {signal.confidence:.2f})")

        # SA Market Summary
        sa_config = get_sa_config()
        print(f"\n🇿🇦 SA Market Context:")
        print(f"  Currency: {sa_config.CURRENCY} ({sa_config.CURRENCY_SYMBOL})")
        print(f"  Exchange: {sa_config.EXCHANGE_NAME}")
        print(f"  Trading Hours: {sa_config.TRADING_START_TIME} - {sa_config.TRADING_END_TIME} SAST")
        print(f"  Settlement: T+{sa_config.SETTLEMENT_DAYS}")
        print(f"  Regulatory Body: {sa_config.REGULATORY_BODY}")

        print("\n✅ Analysis complete!")

    except Exception as e:
        print(f"❌ Error during SA market analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
