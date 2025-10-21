"""
Macro Economist Agent
Analyzes macroeconomic conditions and provides market regime context for investment decisions.
"""

from src.graph.state import AgentState
from src.llm.models import get_model
from langchain_core.messages import HumanMessage
from src.data.macro_data import MacroDataFetcher


def macro_economist_agent(state: AgentState):
    """
    Analyzes macroeconomic environment and market regime.

    Focuses on:
    - Federal Reserve policy stance (hawkish/neutral/dovish)
    - Inflation trends and target deviation
    - Economic growth cycle phase
    - Yield curve signals (recession risk)
    - Market volatility regime
    - Sector rotation recommendations
    - Investment timing assessment
    """

    llm = get_model(state["metadata"]["model_name"], state["metadata"]["model_provider"])
    fetcher = MacroDataFetcher()

    # Fetch comprehensive macro data (once for all tickers)
    macro_summary = fetcher.get_macro_summary()
    market_cycle = fetcher.get_market_cycle_indicator()
    fed_stance = fetcher.get_fed_policy_stance()

    macro_signals = {}

    # Build macro context
    fed_data = macro_summary['fed_funds_rate']
    inflation_data = macro_summary['inflation']
    unemployment_data = macro_summary['unemployment']
    gdp_data = macro_summary['gdp_growth']
    volatility_data = macro_summary['volatility']
    yields_data = macro_summary['treasury_yields']

    macro_context = f"""
    MACROECONOMIC ENVIRONMENT ANALYSIS

    FEDERAL RESERVE POLICY:
    - Current Fed Funds Rate: {fed_data['current']}%
    - Rate Trend: {fed_data['trend'].upper()}
    - Policy Stance: {fed_stance.upper()}
    - Previous Rate: {fed_data.get('previous', 'N/A')}%

    INFLATION METRICS:
    - CPI (Year-over-Year): {inflation_data['cpi_yoy']}%
    - Core CPI: {inflation_data.get('core_cpi_yoy', 'N/A')}%
    - Fed's Target: {inflation_data['target']}%
    - Above Target: {"YES - CONCERNING" if inflation_data['above_target'] else "NO - WITHIN BOUNDS"}
    - Trend: {inflation_data['trend'].upper()}

    EMPLOYMENT SITUATION:
    - Unemployment Rate: {unemployment_data['current']}%
    - 6-Month Ago: {unemployment_data.get('six_months_ago', 'N/A')}%
    - Trend: {unemployment_data['trend'].upper()}
    - Labor Market: {"TIGHT" if unemployment_data['current'] < 4.5 else "LOOSENING" if unemployment_data['current'] > 5.0 else "BALANCED"}

    ECONOMIC GROWTH:
    - GDP Growth Rate: {gdp_data['current']}%
    - Year Ago: {gdp_data.get('year_ago', 'N/A')}%
    - Trend: {gdp_data['trend'].upper()}
    - Recession Risk: {gdp_data['recession_risk'].upper()}

    MARKET VOLATILITY:
    - VIX Index: {volatility_data['current']}
    - 30-Day Average: {volatility_data['avg_30d']}
    - Volatility Regime: {volatility_data['regime'].upper()}
    - Fear Level: {volatility_data['fear_level'].upper()}

    YIELD CURVE:
    - 10-Year Treasury: {yields_data['10_year']}%
    - 2-Year Treasury: {yields_data['2_year']}%
    - 3-Month Treasury: {yields_data['3_month']}%
    - 10Y-2Y Spread: {yields_data['spread_10y_2y']}%
    - Curve Status: {yields_data['curve_status'].upper()}
    - Recession Signal: {"YES - INVERTED CURVE" if yields_data['recession_signal'] else "NO - NORMAL CURVE"}

    MARKET CYCLE PHASE: {market_cycle.upper()}
    """

    # Analyze each ticker with macro context
    for ticker in state['data']['tickers']:
        ticker_prompt = f"""You are a Chief Macro Economist advising institutional investors on market conditions and portfolio positioning.

ANALYZING TICKER: {ticker}


    {macro_context}

    ANALYSIS FRAMEWORK:

    1. ECONOMIC CYCLE ASSESSMENT
       - Where are we in the business cycle?
       - What's the likely path forward (6-12 months)?
       - Key inflection points to watch

    2. FEDERAL RESERVE POLICY IMPACT
       - How will current Fed stance affect markets?
       - Rate hike/cut expectations and timing
       - Impact on different asset classes (stocks, bonds, crypto)

    3. INFLATION & PURCHASING POWER
       - Is inflation under control or accelerating?
       - Implications for equity valuations
       - Real return expectations (nominal - inflation)

    4. RECESSION RISK ASSESSMENT
       - Probability of recession in next 12 months
       - Leading indicators (yield curve, unemployment, GDP)
       - Defensive positioning recommendations

    5. MARKET REGIME & VOLATILITY
       - Current volatility regime and sustainability
       - Risk-on vs risk-off environment
       - Position sizing implications

    6. SECTOR ROTATION STRATEGY
       - Which sectors benefit in current environment?
       - Cyclical vs Defensive positioning
       - Growth vs Value tilt
       - International exposure recommendations

    7. PORTFOLIO IMPLICATIONS FOR {ticker}
       - How should macro conditions affect analysis of this stock?
       - Timing considerations (good/bad time to invest?)
       - Position sizing recommendations based on macro risk

    INVESTMENT CONTEXT (January 2025):
    - Bitcoin reached ATH $109,000 on Jan 20, 2025
    - Trump Executive Order mandated crypto regulatory framework
    - Fed paused rate hikes but watching inflation closely
    - AI/Tech sector continuing strong performance
    - Geopolitical risks: Middle East tensions, China/Taiwan

    Provide a structured macro analysis:
    1. Overall Macro Signal (BULLISH/BEARISH/NEUTRAL for equities)
    2. Confidence Level (0-100%)
    3. Detailed Economic Analysis
    4. Sector Recommendations (which sectors to overweight/underweight)
    5. Risk Factors and Hedging Recommendations
    6. Investment Timing Assessment (good/bad time to deploy capital)

    Return ONLY valid JSON:
    {{
        "signal": "bullish|bearish|neutral",
        "confidence": <0-100>,
        "reasoning": "<detailed macro analysis>",
        "market_cycle": "{market_cycle}",
        "fed_stance": "{fed_stance}",
        "recession_probability": <0-100>,
        "sector_recommendations": {{
            "overweight": ["sector1", "sector2"],
            "neutral": ["sector3"],
            "underweight": ["sector4", "sector5"]
        }},
        "timing_assessment": "excellent|good|neutral|poor|terrible",
        "key_risks": ["risk1", "risk2", "risk3"],
        "hedging_recommendations": ["recommendation1", "recommendation2"]
    }}
    """

        try:
            message = HumanMessage(content=ticker_prompt)
            response = llm.invoke([message])

            # Parse JSON response
            import json
            import re

            # Try to extract JSON from response (in case there's extra text)
            content = response.content.strip()

            # Look for JSON block in markdown code fences
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            # Or try to find raw JSON object
            elif not content.startswith('{'):
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)

            analysis = json.loads(content)

            from src.data.models import AnalystSignal
            macro_signals[ticker] = AnalystSignal(
                signal=analysis["signal"].upper(),
                confidence=analysis["confidence"] / 100.0,
                reasoning=analysis
            )

        except Exception as e:
            print(f"Error in macro economist analysis for {ticker}: {e}")
            print(f"Response content preview: {response.content[:200] if response and hasattr(response, 'content') else 'No response'}")
            from src.data.models import AnalystSignal
            macro_signals[ticker] = AnalystSignal(
                signal="NEUTRAL",
                confidence=0.0,
                reasoning=f"Error in macro analysis: {str(e)}"
            )

    # Update state
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}

    state["data"]["analyst_signals"]["macro_economist"] = macro_signals

    # Store macro context for other agents to reference
    state["data"]["macro_context"] = {
        "market_cycle": market_cycle,
        "fed_stance": fed_stance,
        "macro_summary": macro_summary
    }

    return state
