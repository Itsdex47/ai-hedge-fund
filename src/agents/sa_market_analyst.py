"""
South African Market Analyst Agent
Specialized agent for analyzing South African market conditions and opportunities
"""

import json
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from src.data.models import AnalystSignal
from src.config.sa_market_config import get_sa_config
from src.data.sa_data_adapter import get_sa_data_adapter
from src.llm.models import get_model

sa_config = get_sa_config()
sa_data_adapter = get_sa_data_adapter()


def sa_market_analyst_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    South African Market Analyst Agent

    Analyzes SA-specific market conditions including:
    - Currency volatility (ZAR)
    - Political and regulatory risks
    - Load shedding impact on businesses
    - Commodity price exposure
    - Emerging market dynamics
    - Local economic indicators
    """

    llm = get_model(state["metadata"]["model_name"], state["metadata"]["model_provider"])

    # Get SA market context
    economic_indicators = sa_data_adapter.get_sa_economic_indicators()
    fx_rates = sa_data_adapter.get_zar_fx_rates()
    market_data = sa_data_adapter.get_sa_market_data()

    # Build SA market context
    sa_context = {
        "currency": "ZAR",
        "exchange": "JSE",
        "economic_indicators": economic_indicators,
        "fx_rates": fx_rates,
        "risk_factors": sa_config.RISK_FACTORS,
        "regulatory_body": sa_config.REGULATORY_BODY,
        "trading_hours": f"{sa_config.TRADING_START_TIME} - {sa_config.TRADING_END_TIME} SAST",
        "settlement": f"T+{sa_config.SETTLEMENT_DAYS}",
        "major_sectors": sa_config.SECTORS,
        "top_stocks": sa_config.TOP_STOCKS[:10],  # Top 10 for context
    }

    # Analyze each ticker for SA-specific factors
    ticker_analyses = {}

    for ticker in state["data"]["tickers"]:
        if not sa_data_adapter.validate_sa_ticker(ticker):
            continue

        # Get SA-specific data
        sector = sa_data_adapter.get_sa_sector_exposure(ticker)
        company_facts = sa_data_adapter.get_sa_company_facts(ticker)
        news = sa_data_adapter.get_sa_news(ticker, state["data"]["end_date"])

        # Build ticker-specific context
        ticker_context = {"ticker": ticker, "sector": sector, "company_info": company_facts.model_dump() if company_facts else {}, "recent_news": [n.model_dump() for n in news[:5]], "market_context": sa_context}  # Last 5 news items

        # Create analysis prompt
        system_prompt = f"""You are a South African market analyst specializing in JSE (Johannesburg Stock Exchange) investments.

Key SA Market Context:
- Currency: ZAR (South African Rand)
- Exchange: JSE (Johannesburg Stock Exchange)
- Regulatory Body: FSCA (Financial Sector Conduct Authority)
- Trading Hours: {sa_context['trading_hours']}
- Settlement: {sa_context['settlement']}

SA-Specific Risk Factors:
{chr(10).join(f"- {risk}" for risk in sa_context['risk_factors'])}

Economic Indicators:
{chr(10).join(f"- {k}: {v}" for k, v in economic_indicators.items())}

Major Currency Pairs:
{chr(10).join(f"- {pair}: {rate}" for pair, rate in fx_rates.items())}

Your analysis should consider:
1. ZAR currency volatility impact
2. Load shedding effects on business operations
3. Political and regulatory risks
4. Commodity price exposure (for mining/resource stocks)
5. Emerging market volatility
6. Local economic conditions
7. Sector-specific SA dynamics

Analyze the provided ticker data and provide trading recommendations based on SA market conditions.
"""

        user_prompt = f"""Analyze {ticker} for South African market conditions.

Ticker Context:
{json.dumps(ticker_context, indent=2)}

Provide a JSON response with:
{{
    "signal": "BUY/SELL/HOLD",
    "confidence": 0.0-1.0,
    "reasoning": {{
        "sa_market_factors": "Analysis of SA-specific factors",
        "currency_impact": "ZAR volatility considerations",
        "regulatory_risk": "FSCA and regulatory considerations",
        "sector_outlook": "SA sector-specific analysis",
        "risk_assessment": "SA risk factor analysis"
    }},
    "max_position_size": 0.0-0.05 (5% max for SA market),
    "stop_loss": "Recommended stop loss percentage",
    "time_horizon": "Short/Medium/Long term outlook"
}}"""

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

        try:
            response = llm.invoke(messages)
            analysis = json.loads(response.content)

            # Create analyst signal
            signal = AnalystSignal(signal=analysis.get("signal"), confidence=analysis.get("confidence"), reasoning=analysis.get("reasoning"), max_position_size=analysis.get("max_position_size"))

            ticker_analyses[ticker] = signal

        except Exception as e:
            print(f"Error analyzing {ticker} for SA market: {e}")
            # Default signal
            ticker_analyses[ticker] = AnalystSignal(signal="HOLD", confidence=0.5, reasoning={"error": f"Analysis failed: {str(e)}"}, max_position_size=0.02)

    # Update state with SA analyst signals
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}

    state["data"]["analyst_signals"]["sa_market_analyst"] = ticker_analyses

    return state


def sa_regulatory_compliance_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    South African Regulatory Compliance Agent

    Ensures compliance with:
    - FSCA regulations
    - Exchange controls
    - Foreign investment limits
    - Reporting requirements
    """

    llm = get_model(state["metadata"]["model_name"], state["metadata"]["model_provider"])

    # Get regulatory context
    regulatory_context = {"regulatory_body": sa_config.REGULATORY_BODY, "exchange_controls": sa_config.EXCHANGE_CONTROLS, "foreign_limits": sa_config.FOREIGN_INVESTMENT_LIMITS, "max_position_size": sa_config.MAX_POSITION_SIZE, "max_sector_exposure": sa_config.MAX_SECTOR_EXPOSURE, "stop_loss_percentage": sa_config.STOP_LOSS_PERCENTAGE, "max_daily_drawdown": sa_config.MAX_DAILY_DRAWDOWN}

    # Analyze portfolio for compliance
    portfolio = state["data"]["portfolio"]
    compliance_issues = []

    # Check position sizes
    total_portfolio_value = portfolio.total_cash
    for ticker, position in portfolio.positions.items():
        if position.shares > 0:
            # Calculate position size
            position_value = position.shares * 100  # Simplified valuation
            position_size = position_value / total_portfolio_value if total_portfolio_value > 0 else 0

            if position_size > regulatory_context["max_position_size"]:
                compliance_issues.append({"ticker": ticker, "issue": "Position size exceeds 5% limit", "current_size": f"{position_size:.2%}", "max_allowed": f"{regulatory_context['max_position_size']:.2%}"})

    # Check sector exposure
    sector_exposures = {}
    for ticker, position in portfolio.positions.items():
        if position.shares > 0:
            sector = sa_data_adapter.get_sa_sector_exposure(ticker)
            if sector:
                sector_exposures[sector] = sector_exposures.get(sector, 0) + position.shares

    for sector, exposure in sector_exposures.items():
        sector_exposure_ratio = exposure / sum(sector_exposures.values()) if sum(sector_exposures.values()) > 0 else 0
        if sector_exposure_ratio > regulatory_context["max_sector_exposure"]:
            compliance_issues.append({"sector": sector, "issue": "Sector exposure exceeds 30% limit", "current_exposure": f"{sector_exposure_ratio:.2%}", "max_allowed": f"{regulatory_context['max_sector_exposure']:.2%}"})

    # Create compliance signal
    compliance_signal = AnalystSignal(signal="COMPLIANT" if not compliance_issues else "NON_COMPLIANT", confidence=1.0 if not compliance_issues else 0.8, reasoning={"regulatory_body": regulatory_context["regulatory_body"], "compliance_issues": compliance_issues, "regulatory_limits": regulatory_context}, max_position_size=regulatory_context["max_position_size"])

    # Update state
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}

    state["data"]["analyst_signals"]["sa_regulatory_compliance"] = {"PORTFOLIO": compliance_signal}

    return state


def sa_currency_risk_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    South African Currency Risk Agent

    Analyzes ZAR currency risk and its impact on:
    - Import/export dependent companies
    - Dual-listed stocks
    - Foreign currency denominated assets
    - Inflation impact
    """

    llm = get_model(state["metadata"]["model_name"], state["metadata"]["model_provider"])

    # Get currency data
    fx_rates = sa_data_adapter.get_zar_fx_rates()
    economic_indicators = sa_data_adapter.get_sa_economic_indicators()

    currency_context = {"base_currency": "ZAR", "fx_rates": fx_rates, "inflation": economic_indicators.get("SA_CPI", 0), "repo_rate": economic_indicators.get("SA_REPO_RATE", 0), "current_account": economic_indicators.get("SA_CURRENT_ACCOUNT", 0), "budget_deficit": economic_indicators.get("SA_BUDGET_DEFICIT", 0)}

    # Analyze currency impact on each ticker
    ticker_analyses = {}

    for ticker in state["data"]["tickers"]:
        if not sa_data_adapter.validate_sa_ticker(ticker):
            continue

        # Determine currency sensitivity
        currency_sensitive_stocks = {
            "BHP": "high",  # Dual-listed, commodity exports
            "AGL": "high",  # Dual-listed, commodity exports
            "SOL": "high",  # Oil imports, chemical exports
            "MTN": "medium",  # African operations, USD revenue
            "VOD": "medium",  # African operations
            "NPN": "high",  # Global tech investments
            "SHP": "low",  # Domestic retail
            "WHL": "low",  # Domestic retail
            "TBS": "low",  # Domestic consumer goods
            "BID": "low",  # Domestic retail
            "TFG": "low",  # Domestic retail
            "MRP": "low",  # Domestic retail
            "CLS": "low",  # Domestic retail
            "SBK": "medium",  # Domestic but affected by interest rates
            "FSR": "medium",  # Domestic but affected by interest rates
            "NED": "medium",  # Domestic but affected by interest rates
            "ABG": "medium",  # Domestic but affected by interest rates
        }

        sensitivity = currency_sensitive_stocks.get(ticker, "low")

        # Create currency analysis
        currency_analysis = {"ticker": ticker, "currency_sensitivity": sensitivity, "zar_volatility_impact": "high" if sensitivity == "high" else "low", "inflation_impact": "high" if sensitivity == "high" else "medium", "interest_rate_impact": "high" if ticker in ["SBK", "FSR", "NED", "ABG"] else "low", "fx_context": currency_context}

        # Generate currency risk signal
        if sensitivity == "high":
            signal = "REDUCE" if currency_context["inflation"] > 6.0 else "HOLD"
            confidence = 0.8
        elif sensitivity == "medium":
            signal = "HOLD"
            confidence = 0.6
        else:
            signal = "BUY"  # Domestic stocks benefit from ZAR weakness
            confidence = 0.7

        ticker_analyses[ticker] = AnalystSignal(signal=signal, confidence=confidence, reasoning={"currency_sensitivity": sensitivity, "zar_analysis": currency_analysis, "inflation_impact": currency_context["inflation"], "interest_rate_impact": currency_context["repo_rate"]}, max_position_size=0.03 if sensitivity == "high" else 0.05)

    # Update state
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}

    state["data"]["analyst_signals"]["sa_currency_risk"] = ticker_analyses

    return state
