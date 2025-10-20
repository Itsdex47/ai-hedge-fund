# 🪙 Cryptocurrency Support - LIVE!

## What's New

The AI Hedge Fund now supports **cryptocurrency analysis** with institutional-grade insights!

### ✅ Completed Features

1. **Crypto Data Module** (`src/data/crypto_data.py`)
   - Real-time price data from CoinGecko API
   - Historical data (up to 365 days)
   - Market metrics (market cap, volume, dominance)
   - Fear & Greed Index integration
   - Institutional flow indicators

2. **Crypto Analyst Agent** (`src/agents/crypto_analyst.py`)
   - Institutional adoption analysis
   - Volatility and risk assessment
   - Supply dynamics evaluation
   - Market sentiment integration
   - Regulatory clarity assessment

3. **Supported Cryptocurrencies**
   - Bitcoin (BTC) ⭐
   - Ethereum (ETH) ⭐
   - Solana (SOL)
   - Cardano (ADA)
   - Polkadot (DOT)
   - Avalanche (AVAX)
   - Polygon (MATIC)
   - Chainlink (LINK)
   - Uniswap (UNI)
   - Cosmos (ATOM)

4. **New Strategy**
   - `--strategy crypto` - Crypto-focused analysis

---

## 🚀 How to Use

### Analyze Bitcoin
```bash
poetry run python src/main.py --crypto BTC --strategy crypto --ollama
```

### Analyze Ethereum
```bash
poetry run python src/main.py --crypto ETH --strategy crypto --ollama
```

### Compare Multiple Cryptos
```bash
poetry run python src/main.py --crypto BTC,ETH,SOL --strategy crypto --ollama
```

### Mix Stocks and Crypto
```bash
# Coming soon - multi-asset support
```

---

## 📊 What the Crypto Analyst Provides

### 1. Institutional Adoption Signals
- ETF inflows tracking
- Corporate treasury adoption (e.g., MicroStrategy)
- Regulatory clarity assessment
- Custody solution availability

### 2. Market Metrics
- Current price and market cap
- 24h/7d/30d/1y performance
- All-time high/low analysis
- Volume/market cap ratio (institutional interest)

### 3. Supply Dynamics
- Circulating vs total supply
- Max supply (scarcity analysis)
- Supply inflation rate

### 4. Market Context
- Overall crypto market cap
- BTC/ETH dominance
- Fear & Greed Index (0-100)
- Recent price trends

### 5. Risk Assessment
- Volatility analysis
- Regulatory risks
- Market manipulation concerns
- Recommended allocation % (typically 1-5% for institutions)

---

## 🎯 Real-World Data (Current)

**As of testing:**
- Bitcoin: $110,806 (ATH: $109k on Jan 20, 2025)
- Market Cap: $2.2T
- 24h Change: +2.71%

**Institutional Context:**
- Bitcoin ETFs: $50B+ AUM (BlackRock leads)
- SAB 121 rescinded: Custody barriers removed
- Trump Executive Order: Crypto framework mandate
- Corporate adoption: MicroStrategy holds 461,000 BTC

---

## 💡 Institutional Use Cases

### 1. Portfolio Diversification (1-5% allocation)
```bash
poetry run python src/main.py --crypto BTC --strategy crypto --ollama
```
**Use:** Evaluate BTC for small allocation in balanced portfolio

### 2. Inflation Hedge Assessment
```bash
poetry run python src/main.py --crypto BTC,ETH --strategy crypto --ollama
```
**Use:** Compare crypto as alternative to gold

### 3. Tech Exposure via Crypto
```bash
poetry run python src/main.py --crypto ETH,SOL --strategy crypto --ollama
```
**Use:** Evaluate smart contract platforms as tech plays

### 4. Market Sentiment Gauge
- Crypto analyst provides Fear & Greed Index
- Helps time entry/exit for volatile assets

---

## 🔧 Technical Details

### API Used
- **CoinGecko API** (Free Tier)
  - No API key required
  - 50 calls/minute limit
  - Comprehensive data coverage

### Data Points Collected
- Price (current, historical)
- Market cap & ranking
- Trading volume (24h)
- Supply metrics (circulating, total, max)
- All-time high/low
- Performance (24h, 7d, 30d, 1y)
- Fear & Greed Index
- BTC/ETH dominance

### Analyst Framework
- Uses same LLM models as stock analysts
- Institutional perspective (not retail trading)
- Focus on wealth preservation allocation (1-5%)
- Risk-first approach

---

## 📈 Next Steps (Future Enhancements)

1. **On-Chain Metrics** (Week 2)
   - Active addresses
   - Transaction volume
   - Network hash rate (BTC)
   - Staking metrics (ETH)

2. **DeFi Analysis** (Week 3)
   - DeFi TVL tracking
   - Yield opportunities
   - Protocol risk assessment

3. **Crypto ETF Support** (Week 3)
   - BlackRock iShares Bitcoin Trust
   - Other Bitcoin/Ethereum ETFs
   - Traditional brokerage access

4. **Multi-Asset Portfolios** (Week 4)
   - Stocks + Crypto + Bonds
   - Correlation analysis
   - Portfolio optimization with crypto

5. **Options on Crypto** (Week 5)
   - Bitcoin futures
   - Options strategies
   - Hedging mechanisms

---

## 🎓 Educational Context

### Why Institutions Care About Crypto Now (2025)

1. **Regulatory Clarity**
   - Trump admin pro-crypto stance
   - SAB 121 rescinded (custody barriers gone)
   - Federal framework mandated

2. **ETF Revolution**
   - $50B+ in Bitcoin ETF AUM
   - Traditional 401k access
   - Institutional custody solved

3. **Corporate Adoption**
   - MicroStrategy: 461,000 BTC
   - Corporate treasuries diversifying
   - Payment integration growing

4. **Market Maturity**
   - Lower volatility vs 2017/2021
   - Deeper liquidity
   - Professional market makers

5. **Inflation Hedge**
   - Digital gold narrative
   - Fixed supply (BTC)
   - Uncorrelated to stocks (sometimes)

---

## ⚠️ Important Disclaimers

### For Institutional Use:
- **Start small:** 1-5% allocation typical
- **Volatility expected:** Crypto is 3-5x more volatile than stocks
- **Not for everyone:** Only suitable for long-term investors
- **Regulatory evolving:** Stay informed on policy changes
- **Custody critical:** Use institutional-grade custody

### Risk Factors:
- ❌ High volatility (can drop 50%+ in months)
- ❌ Regulatory uncertainty (still evolving)
- ❌ Technical risks (hacks, smart contract bugs)
- ❌ Market manipulation concerns
- ❌ Concentration risk (BTC dominates market)

### Recommended Approach:
✅ Small allocation (1-5% of portfolio)
✅ Long-term horizon (5-10+ years)
✅ Dollar-cost averaging (DCA)
✅ Institutional custody
✅ Regular rebalancing

---

## 🧪 Testing

Test the crypto feature:
```bash
# With your local Ollama model (free)
poetry run python src/main.py --crypto BTC --strategy crypto --ollama

# With OpenAI (if you have API key)
poetry run python src/main.py --crypto BTC,ETH --strategy crypto

# Show detailed reasoning
poetry run python src/main.py --crypto BTC --strategy crypto --ollama --show-reasoning
```

---

## 📚 Resources

- **CoinGecko API:** https://www.coingecko.com/en/api
- **Fear & Greed Index:** https://alternative.me/crypto/fear-and-greed-index/
- **Bitcoin ETF Data:** https://www.blackrock.com/
- **Institutional Research:** https://www.coinbase.com/institutional

---

**Status:** ✅ LIVE and ready to use!

**Next Feature:** Macro Economic Agent (Week 2)

---

Made with ❤️ for institutional crypto analysis
