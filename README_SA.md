# 🇿🇦 South African AI Hedge Fund

A specialized version of the AI Hedge Fund project configured for the South African market, specifically the JSE (Johannesburg Stock Exchange).

## 🎯 Overview

This project has been reconfigured to operate holistically in the South African market, incorporating:

- **JSE Market Integration**: Native support for Johannesburg Stock Exchange tickers
- **ZAR Currency**: All calculations and reporting in South African Rand
- **SA Regulatory Compliance**: FSCA (Financial Sector Conduct Authority) compliance checks
- **Local Market Dynamics**: Understanding of load shedding, political risks, and emerging market volatility
- **SA-Specific Agents**: Specialized AI agents for South African market analysis

## 🏗️ Architecture

### Core Components

1. **SA Market Configuration** (`src/config/sa_market_config.py`)
   - JSE exchange settings
   - ZAR currency configuration
   - SA trading hours and settlement rules
   - FSCA regulatory limits

2. **SA Data Adapter** (`src/data/sa_data_adapter.py`)
   - JSE-specific data fetching
   - SA economic indicators
   - ZAR exchange rates
   - Local news sentiment analysis

3. **SA Market Agents** (`src/agents/sa_market_analyst.py`)
   - **SA Market Analyst**: Analyzes SA-specific market conditions
   - **SA Regulatory Compliance**: Ensures FSCA compliance
   - **SA Currency Risk**: Analyzes ZAR volatility impact

### Key Features

- **Currency**: ZAR (South African Rand) throughout
- **Exchange**: JSE (Johannesburg Stock Exchange)
- **Trading Hours**: 9:00 AM - 5:00 PM SAST
- **Settlement**: T+3
- **Regulatory Body**: FSCA
- **Risk Management**: SA-specific limits and controls

## 📊 Supported JSE Stocks

### Top 20 JSE Stocks by Market Cap

| Ticker | Company | Sector | Market Cap (ZAR) |
|--------|---------|--------|------------------|
| NPN | Naspers | Technology | ~R1.2T |
| BHP | BHP Group | Mining & Resources | ~R800B |
| AGL | Anglo American | Mining & Resources | ~R600B |
| MTN | MTN Group | Telecommunications | ~R200B |
| VOD | Vodacom | Telecommunications | ~R180B |
| SBK | Standard Bank | Financial Services | ~R150B |
| FSR | FirstRand | Financial Services | ~R140B |
| NED | Nedbank | Financial Services | ~R80B |
| ABG | Absa Group | Financial Services | ~R70B |
| SOL | Sasol | Energy | ~R60B |
| IMP | Impala Platinum | Mining & Resources | ~R50B |
| ANG | AngloGold Ashanti | Mining & Resources | ~R45B |
| AMS | Anglo American Platinum | Mining & Resources | ~R40B |
| SHP | Shoprite | Consumer Goods | ~R35B |
| WHL | Woolworths | Consumer Goods | ~R30B |
| TBS | Tiger Brands | Consumer Goods | ~R25B |
| BID | Bid Corporation | Consumer Goods | ~R20B |
| TFG | The Foschini Group | Consumer Goods | ~R18B |
| MRP | Mr Price Group | Consumer Goods | ~R15B |
| CLS | Clicks Group | Consumer Goods | ~R12B |

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Poetry** (recommended) or pip
3. **API Keys** (see Configuration section)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-hedge-fund

# Install dependencies
poetry install
# OR
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

#### 1. SA Market Analysis

```bash
# Analyze top JSE stocks
python src/sa_main.py --ticker NPN,SBK,MTN,VOD

# Use SA-specific agents only
python src/sa_main.py --ticker NPN,SBK,MTN,VOD --sa-only

# Show detailed reasoning
python src/sa_main.py --ticker NPN,SBK,MTN,VOD --show-reasoning
```

#### 2. SA Market Backtesting

```bash
# Backtest with 1M ZAR initial capital
python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD

# Custom date range
python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --start-date 2023-01-01 --end-date 2024-01-01

# Custom initial capital
python src/sa_backtester.py --ticker NPN,SBK,MTN,VOD --initial-capital 500000
```

#### 3. Web Application

```bash
# Start the full-stack web application
cd app && ./run.sh
# OR on Windows: cd app && run.bat
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# LLM API Keys (required)
OPENAI_API_KEY=your-openai-api-key
# OR
GROQ_API_KEY=your-groq-api-key
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key

# Financial Data API (optional for JSE stocks)
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# SA-specific settings
SA_MARKET_MODE=true
SA_CURRENCY=ZAR
SA_EXCHANGE=JSE
```

### SA Market Settings

Key configuration in `src/config/sa_market_config.py`:

```python
# Risk Management
MAX_POSITION_SIZE = 0.05  # 5% max position per stock
MAX_SECTOR_EXPOSURE = 0.30  # 30% max exposure per sector
STOP_LOSS_PERCENTAGE = 0.15  # 15% stop loss
MAX_DAILY_DRAWDOWN = 0.02  # 2% max daily drawdown

# Trading Hours (SAST)
TRADING_START_TIME = time(9, 0)  # 9:00 AM
TRADING_END_TIME = time(17, 0)   # 5:00 PM
```

## 🤖 SA-Specific AI Agents

### 1. SA Market Analyst
- Analyzes SA-specific market conditions
- Considers load shedding impact on businesses
- Evaluates political and regulatory risks
- Assesses commodity price exposure
- Monitors emerging market volatility

### 2. SA Regulatory Compliance
- Ensures FSCA compliance
- Checks exchange controls
- Validates foreign investment limits
- Monitors position size limits
- Tracks sector exposure limits

### 3. SA Currency Risk
- Analyzes ZAR volatility impact
- Evaluates import/export dependencies
- Assesses dual-listed stock exposure
- Monitors inflation impact
- Tracks interest rate sensitivity

## 📈 SA Market Characteristics

### Risk Factors
- **Currency Volatility**: ZAR fluctuations
- **Political Risk**: Policy uncertainty
- **Load Shedding**: Infrastructure challenges
- **Commodity Exposure**: Mining sector dependency
- **Emerging Market Volatility**: Global risk sentiment
- **Regulatory Changes**: FSCA oversight
- **Infrastructure Challenges**: Power and logistics

### Economic Indicators
- **CPI**: Consumer Price Index
- **Repo Rate**: South African Reserve Bank rate
- **GDP Growth**: Economic expansion
- **Unemployment Rate**: Labor market conditions
- **Current Account**: Balance of payments
- **Budget Deficit**: Fiscal position
- **Credit Rating**: Sovereign risk

### Major Sectors
1. **Financial Services**: Banks, insurance, asset management
2. **Mining & Resources**: Gold, platinum, coal, iron ore
3. **Industrial**: Manufacturing, construction, transport
4. **Consumer Goods**: Retail, food, beverages
5. **Technology**: Software, telecommunications
6. **Healthcare**: Pharmaceuticals, medical services
7. **Real Estate**: Property development, REITs
8. **Telecommunications**: Mobile, internet, media
9. **Energy**: Oil, gas, renewable energy
10. **Transportation**: Logistics, aviation, shipping

## 🔧 Advanced Usage

### Custom SA Agents

You can create custom SA-specific agents by extending the base agent pattern:

```python
from src.agents.sa_market_analyst import sa_market_analyst_agent

def custom_sa_agent(state):
    # Your custom SA market logic
    return state
```

### SA Data Integration

Integrate additional SA data sources:

```python
from src.data.sa_data_adapter import get_sa_data_adapter

sa_adapter = get_sa_data_adapter()
economic_data = sa_adapter.get_sa_economic_indicators()
fx_rates = sa_adapter.get_zar_fx_rates()
```

### SA Risk Management

Customize risk parameters for SA market:

```python
from src.config.sa_market_config import get_sa_config

sa_config = get_sa_config()
max_position = sa_config.MAX_POSITION_SIZE
max_sector = sa_config.MAX_SECTOR_EXPOSURE
```

## 📊 Performance Monitoring

### SA-Specific Metrics
- **ZAR Performance**: Returns in South African Rand
- **Sector Exposure**: Compliance with 30% sector limits
- **Currency Risk**: ZAR volatility impact
- **Regulatory Compliance**: FSCA adherence
- **Load Shedding Impact**: Infrastructure risk assessment

### Reporting
- Portfolio value in ZAR
- Performance vs JSE indices
- Currency-adjusted returns
- SA risk factor analysis
- Regulatory compliance status

## 🛡️ Risk Management

### SA-Specific Risk Controls
1. **Position Limits**: 5% maximum per stock
2. **Sector Limits**: 30% maximum per sector
3. **Stop Losses**: 15% automatic stop loss
4. **Currency Hedging**: ZAR volatility management
5. **Regulatory Compliance**: FSCA requirements
6. **Liquidity Management**: JSE trading constraints

### Compliance Monitoring
- Real-time position size checks
- Sector exposure monitoring
- Regulatory limit validation
- Currency risk assessment
- Settlement cycle compliance

## 🌐 Integration Options

### Data Sources
- **Primary**: Financial Datasets API (JSE support)
- **Alternative**: Sharenet, JSE Direct, Moneyweb
- **Economic**: SARB, Stats SA, Treasury
- **News**: Fin24, Business Live, Moneyweb

### Broker Integration
- **EasyEquities**: Popular SA retail broker
- **Standard Bank**: Institutional trading
- **Absa**: Corporate and retail
- **Interactive Brokers**: International access

## 🚨 Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results
- SA market has unique risks and challenges

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused.

## 📞 Support

For questions about the SA market adaptation:
- Create an issue on GitHub
- Check the documentation
- Review the SA-specific examples

---

**🇿🇦 Built for the South African Market** 