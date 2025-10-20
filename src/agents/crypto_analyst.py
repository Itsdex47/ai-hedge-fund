"""
Cryptocurrency Analyst Agent
Analyzes crypto assets using on-chain metrics, institutional flows, market sentiment, and volatility.
"""

from src.graph.state import AgentState
from src.llm.models import get_model
from langchain_core.messages import HumanMessage
from src.data.crypto_data import CryptoDataFetcher


def crypto_analyst_agent(state: AgentState):
    """
    Analyzes cryptocurrency from an institutional perspective.

    Focuses on:
    - Institutional adoption signals
    - Market sentiment (Fear & Greed)
    - Volatility and risk metrics
    - Supply dynamics
    - Correlation with traditional assets
    - Regulatory clarity
    """

    llm = get_model(state["metadata"]["model_name"], state["metadata"]["model_provider"])
    fetcher = CryptoDataFetcher()

    crypto_signals = {}

    for crypto_symbol in state["data"]["crypto_symbols"]:
        # Fetch comprehensive crypto data
        current_data = fetcher.fetch_current_price(crypto_symbol)
        if not current_data:
            continue

        historical_data = fetcher.fetch_historical_data(crypto_symbol, days=90)
        market_overview = fetcher.fetch_market_overview()
        fear_greed = fetcher.fetch_fear_greed_index()
        institutional_signals = fetcher.get_institutional_signals(crypto_symbol)

        # Build analysis context
        crypto_context = f"""
        Cryptocurrency: {current_data['name']} ({crypto_symbol})

        CURRENT METRICS:
        - Current Price: ${current_data['current_price']:,.2f}
        - Market Cap: ${current_data['market_cap']/1e9:.2f}B
        - Market Cap Rank: #{current_data['market_cap_rank']}
        - 24h Volume: ${current_data['total_volume']/1e9:.2f}B

        PRICE PERFORMANCE:
        - 24h Change: {current_data['price_change_percentage_24h']:.2f}%
        - 7d Change: {current_data.get('price_change_percentage_7d', 0):.2f}%
        - 30d Change: {current_data.get('price_change_percentage_30d', 0):.2f}%
        - 1y Change: {current_data.get('price_change_percentage_1y', 0):.2f}%

        SUPPLY DYNAMICS:
        - Circulating Supply: {current_data.get('circulating_supply', 0):,.0f}
        - Total Supply: {current_data.get('total_supply', 'Unknown')}
        - Max Supply: {current_data.get('max_supply', 'Unlimited')}

        ALL-TIME METRICS:
        - All-Time High: ${current_data['ath']:,.2f}
        - ATH Discount: {current_data['ath_change_percentage']:.2f}%
        - All-Time Low: ${current_data['atl']:,.2f}
        - ATL Gain: {current_data['atl_change_percentage']:.2f}%

        INSTITUTIONAL SIGNALS:
        - Volume/Market Cap Ratio: {institutional_signals['volume_to_mcap_ratio']:.4f}
        - Institutional Interest: {institutional_signals['institutional_interest']}
        - Buying Opportunity: {institutional_signals['buying_opportunity_rating']}
        - Top 10 Asset: {institutional_signals['is_top_10']}

        OVERALL MARKET CONTEXT:
        - Total Crypto Market Cap: ${market_overview['total_market_cap']/1e12:.2f}T
        - BTC Dominance: {market_overview['btc_dominance']:.1f}%
        - ETH Dominance: {market_overview['eth_dominance']:.1f}%
        - Market Sentiment (Fear & Greed): {fear_greed['value']}/100 ({fear_greed['value_classification']})

        RECENT PRICE ACTION (Last 30 days):
        {self._format_recent_prices(historical_data[-30:])}

        INSTITUTIONAL CONTEXT (January 2025):
        - Bitcoin ETFs: $50B+ in AUM (BlackRock largest)
        - Regulatory: Trump Executive Order mandated crypto framework
        - SAB 121 Rescinded: Institutional custody barriers removed
        - Corporate Treasuries: MicroStrategy holds 461,000 BTC
        - Bitcoin ATH: $109,000 (January 20, 2025)
        """

        prompt = f"""You are a cryptocurrency analyst advising institutional investors on digital asset exposure.

        {crypto_context}

        ANALYSIS FRAMEWORK:

        1. INSTITUTIONAL ADOPTION (Most Important for Wealth Preservation)
           - Is this asset gaining institutional acceptance?
           - ETF flows, custody solutions, corporate treasuries
           - Regulatory clarity improving or worsening?

        2. VOLATILITY ASSESSMENT
           - Historical volatility vs traditional assets
           - Current volatility regime (Fear & Greed index)
           - Suitable for conservative allocation (1-5%)?

        3. MARKET STRUCTURE
           - Liquidity depth (volume/market cap)
           - Market cap size (top 10 = less risky)
           - Supply dynamics (scarce = bullish long-term)

        4. CORRELATION & DIVERSIFICATION
           - Correlation with stocks (is it truly diversifying?)
           - Safe haven properties during market stress
           - Inflation hedge characteristics

        5. RISK FACTORS
           - Regulatory uncertainty
           - Technical/security risks
           - Market manipulation concerns
           - Concentration risk

        INVESTMENT THESIS:
        - For LONG-TERM wealth preservation investors
        - Typical allocation: 1-5% of portfolio
        - Focus on BTC/ETH (most institutional)
        - Treat as asymmetric growth option, not core holding

        Provide a structured analysis with:
        1. Overall Signal (BULLISH/BEARISH/NEUTRAL)
        2. Confidence Level (0-100%)
        3. Detailed Reasoning
        4. Recommended Allocation % (for institutional portfolio)
        5. Key Risks to Monitor

        Return ONLY valid JSON:
        {{
            "signal": "bullish|bearish|neutral",
            "confidence": <0-100>,
            "reasoning": "<detailed analysis>",
            "recommended_allocation_pct": <1-10>,
            "key_risks": ["risk1", "risk2", "risk3"],
            "institutional_suitability": "high|medium|low"
        }}
        """

        try:
            message = HumanMessage(content=prompt)
            response = llm.invoke([message])

            # Parse JSON response
            import json
            analysis = json.loads(response.content)

            from src.agents.state import AnalystSignal
            crypto_signals[crypto_symbol] = AnalystSignal(
                signal=analysis["signal"].upper(),
                confidence=analysis["confidence"] / 100.0,
                reasoning=analysis
            )

        except Exception as e:
            print(f"Error in crypto analysis for {crypto_symbol}: {e}")
            from src.agents.state import AnalystSignal
            crypto_signals[crypto_symbol] = AnalystSignal(
                signal="NEUTRAL",
                confidence=0.0,
                reasoning=f"Error in analysis: {str(e)}"
            )

    # Update state
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}

    state["data"]["analyst_signals"]["crypto_analyst"] = crypto_signals

    return state


def _format_recent_prices(self, historical_data: list) -> str:
    """Format recent price data for context."""
    if not historical_data:
        return "No recent data available"

    output = []
    for i in range(0, len(historical_data), 7):  # Weekly samples
        point = historical_data[i]
        output.append(f"{point['date']}: ${point['price']:,.2f}")

    return "\n".join(output[-5:])  # Last 5 weeks
