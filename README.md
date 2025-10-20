# 🤖 AI Hedge Fund - SIMPLIFIED VERSION

An AI-powered hedge fund that uses AI investor agents to make trading decisions. This **simplified version** is faster, cheaper, and easier to use than traditional implementations.

⚠️ **EDUCATIONAL USE ONLY** - Not for real trading or investment.

## ✨ What Makes This Version Better

### **Simplified From:**
- ❌ 18 AI analyst agents → ✅ **6 core analysts**
- ❌ 6 LLM providers → ✅ **3 top providers** (OpenAI, Anthropic, Ollama)
- ❌ Complex setup → ✅ **Strategy presets**
- ❌ 222MB web app → ✅ **CLI only** (under 2MB)

### **Results:**
- ⚡ **3x faster** execution
- 💰 **70% cheaper** to run
- 🧠 **Easier** to understand and use
- 🎯 **More focused** analysis

---

## 🎯 The 6 Core AI Analysts

1. **Warren Buffett** - Value investing with strong fundamentals
2. **Peter Lynch** - Growth at reasonable price ("ten-baggers")
3. **Technical Analyst** - Chart patterns and momentum
4. **Fundamentals Analyst** - Financial statement deep dive
5. **Sentiment Analyst** - Market sentiment and news analysis
6. **Valuation Analyst** - Intrinsic value calculation

Plus: **Risk Manager** and **Portfolio Manager** coordinate the final decision.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone repository
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund

# Install with Poetry
poetry install
```

### 2. Set Up API Keys

Create a `.env` file:
```bash
cp .env.example .env
```

Add your API key (choose ONE):
```bash
# Option 1: OpenAI (recommended)
OPENAI_API_KEY=your-key-here

# Option 2: Anthropic Claude
ANTHROPIC_API_KEY=your-key-here

# Option 3: Use local Ollama (free, no API key needed)
# Just install Ollama and use --ollama flag
```

### 3. Run Analysis

```bash
# Use a strategy preset (RECOMMENDED)
poetry run python src/main.py --tickers AAPL --strategy conservative

# Or choose analysts interactively
poetry run python src/main.py --tickers AAPL
```

---

## 📊 Strategy Presets

The easiest way to use the platform:

### **Conservative Strategy**
Value-focused analysis for long-term investors
```bash
poetry run python src/main.py --tickers AAPL --strategy conservative
```
**Analysts:** Warren Buffett, Fundamentals, Valuation

### **Growth Strategy**
High-growth opportunities with momentum
```bash
poetry run python src/main.py --tickers TSLA --strategy growth
```
**Analysts:** Peter Lynch, Technical, Sentiment

### **Balanced Strategy**
Mix of value, growth, and technical analysis
```bash
poetry run python src/main.py --tickers MSFT --strategy balanced
```
**Analysts:** Buffett, Lynch, Technical, Valuation

### **All Analysts**
Comprehensive analysis (slower, more expensive)
```bash
poetry run python src/main.py --tickers GOOGL --strategy all
```
**Analysts:** All 6 analysts

---

## 💡 Usage Examples

### Basic Analysis
```bash
poetry run python src/main.py --tickers AAPL
```

### Multiple Stocks
```bash
poetry run python src/main.py --tickers AAPL,MSFT,GOOGL --strategy balanced
```

### Show Detailed Reasoning
```bash
poetry run python src/main.py --tickers AAPL --strategy conservative --show-reasoning
```

### Custom Date Range
```bash
poetry run python src/main.py --tickers AAPL --start-date 2024-01-01 --end-date 2024-06-01
```

### Use Local Models (Free, Private)
```bash
# First install Ollama: https://ollama.ai
poetry run python src/main.py --tickers AAPL --ollama
```

---

## 🧪 Backtesting

Test strategies on historical data:

```bash
# Basic backtest
poetry run python src/backtester.py --tickers AAPL,MSFT

# With strategy and custom dates
poetry run python src/backtester.py \
  --tickers AAPL,MSFT,NVDA \
  --start-date 2024-01-01 \
  --end-date 2024-06-01 \
  --analysts-all
```

---

## 🔧 Available Options

### Main Analysis (`main.py`)
- `--tickers` - Stock symbols (required)
- `--strategy` - Preset strategy (conservative/growth/balanced/all)
- `--initial-cash` - Starting capital (default: $100,000)
- `--start-date` - Analysis start date (YYYY-MM-DD)
- `--end-date` - Analysis end date (YYYY-MM-DD)
- `--show-reasoning` - Show detailed analyst reasoning
- `--ollama` - Use local Ollama models

### Backtesting (`backtester.py`)
- `--tickers` - Stock symbols
- `--start-date` - Backtest start date
- `--end-date` - Backtest end date
- `--initial-capital` - Starting capital
- `--analysts-all` - Use all analysts
- `--ollama` - Use local models

---

## 🎓 How It Works

1. **Fetch Data** - Gets financial data, news, insider trades for selected stocks
2. **Analyze** - Each AI analyst evaluates the stock from their perspective
3. **Risk Assessment** - Risk manager evaluates portfolio risk metrics
4. **Decision** - Portfolio manager combines all signals into final recommendation
5. **Output** - Shows analysis summary and trading recommendation

---

## 💰 Cost Comparison

| Analysts | API Calls | Estimated Cost* |
|----------|-----------|-----------------|
| Conservative (3) | ~15 | $0.05-0.15 |
| Growth (3) | ~15 | $0.05-0.15 |
| Balanced (4) | ~20 | $0.10-0.20 |
| All (6) | ~30 | $0.15-0.30 |

*Per stock analyzed using GPT-4o-mini. Claude Haiku is similar.

---

## 📦 Supported Data Sources

- **Free tickers:** AAPL, GOOGL, MSFT, NVDA, TSLA (no API key needed)
- **All other tickers:** Requires `FINANCIAL_DATASETS_API_KEY`

Get your key at: https://financialdatasets.ai/

---

## 🧠 LLM Providers

### Supported (Choose ONE):

1. **OpenAI** (Recommended for API use)
   - GPT-4o (Latest) - Best overall quality
   - GPT-4o Mini - Fast & cheap
   - o1 (Reasoning) - Advanced reasoning
   - o1-mini - Faster reasoning

2. **Anthropic** (Best reasoning)
   - Claude Sonnet 4 (Latest) - Best reasoning available
   - Claude Sonnet 3.7 - Very good performance
   - Claude Opus 4 - Most powerful

3. **Ollama** (Free, Local, Private - RECOMMENDED)
   - **GPT-OSS 20B Cloud** - Your installed model (Recommended!)
   - GPT-OSS 20B - Alternative version
   - Llama 3.1 - Fast and capable
   - Qwen 3 30B - Large context window
   - Gemma 3 12B - Good for analysis
   - DeepSeek R1 8B - Reasoning focused
   - No API key or internet needed
   - 100% private
   - No API costs!

---

## ⚠️ Important Disclaimers

- **EDUCATIONAL ONLY** - Not for real trading
- **No financial advice** - Use at your own risk
- **Past performance ≠ future results**
- **Consult a financial advisor** for real investments

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Please keep PRs small and focused!**

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Simplified and optimized version of the original AI Hedge Fund project.

**Built with:**
- LangChain & LangGraph
- OpenAI / Anthropic / Ollama
- Financial Datasets API

---

## 📚 Learn More

- **Original Project:** https://github.com/virattt/ai-hedge-fund
- **Documentation:** Check the code comments and docstrings
- **Issues:** Report bugs on GitHub Issues

---

Made with ❤️ for educational purposes
