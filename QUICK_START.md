# 🚀 QUICK START GUIDE

## Run With Your Local Ollama Models (RECOMMENDED)

Your system has these Ollama models installed:
- **gpt-oss:20b-cloud** ⭐ (Best choice - recommended!)
- gpt-oss:20b
- llama3.1:latest
- qwen3:30b
- gemma3:12b
- deepseek-r1:8b

### **Fastest Way to Start:**

```bash
# Conservative strategy with local GPT-OSS 20B
poetry run python src/main.py --tickers AAPL --strategy conservative --ollama

# Growth strategy with local model
poetry run python src/main.py --tickers TSLA --strategy growth --ollama

# Balanced strategy
poetry run python src/main.py --tickers MSFT --strategy balanced --ollama
```

### **Why Use Ollama (Local)?**
- ✅ **FREE** - No API costs ever
- ✅ **FAST** - Your 20B model is already downloaded
- ✅ **PRIVATE** - Data never leaves your machine
- ✅ **OFFLINE** - Works without internet
- ✅ **UNLIMITED** - No rate limits or quotas

---

## If You Want to Use Cloud APIs Instead

### **1. OpenAI (Good but costs money)**
```bash
# Add to .env file:
OPENAI_API_KEY=sk-your-key-here

# Run:
poetry run python src/main.py --tickers AAPL --strategy conservative
```

### **2. Anthropic Claude (Best reasoning but costs money)**
```bash
# Add to .env file:
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Run:
poetry run python src/main.py --tickers AAPL --strategy conservative
```

---

## 📊 Strategy Cheat Sheet

### **Conservative (Value Investing)**
Best for: Long-term stable stocks
```bash
poetry run python src/main.py --tickers AAPL,JNJ,PG --strategy conservative --ollama
```
Uses: Warren Buffett, Fundamentals, Valuation analysts

### **Growth (High Growth)**
Best for: Tech stocks, growth companies
```bash
poetry run python src/main.py --tickers TSLA,NVDA,AMD --strategy growth --ollama
```
Uses: Peter Lynch, Technical, Sentiment analysts

### **Balanced (Mix)**
Best for: General purpose analysis
```bash
poetry run python src/main.py --tickers MSFT,GOOGL,AMZN --strategy balanced --ollama
```
Uses: Buffett, Lynch, Technical, Valuation analysts

### **All Analysts (Comprehensive)**
Best for: When you want maximum analysis
```bash
poetry run python src/main.py --tickers AAPL --strategy all --ollama
```
Uses: All 6 analysts (slower but thorough)

---

## 🎯 Common Use Cases

### **Quick Check on Single Stock**
```bash
poetry run python src/main.py --tickers AAPL --strategy conservative --ollama
```

### **Compare Multiple Stocks**
```bash
poetry run python src/main.py --tickers AAPL,MSFT,GOOGL --strategy balanced --ollama
```

### **See Detailed Reasoning**
```bash
poetry run python src/main.py --tickers AAPL --strategy conservative --ollama --show-reasoning
```

### **Custom Date Range**
```bash
poetry run python src/main.py --tickers AAPL --start-date 2024-01-01 --end-date 2024-06-01 --ollama
```

### **Backtest a Strategy**
```bash
poetry run python src/backtester.py --tickers AAPL,MSFT --start-date 2024-01-01 --ollama
```

---

## ⚡ Performance Comparison

| Model | Speed | Cost | Quality | Privacy |
|-------|-------|------|---------|---------|
| **GPT-OSS 20B (Local)** | ⚡⚡⚡ Fast | 💰 FREE | ⭐⭐⭐⭐ Good | 🔒 100% |
| GPT-4o (OpenAI) | ⚡⚡ Medium | 💰💰 $0.10/run | ⭐⭐⭐⭐⭐ Best | ☁️ Cloud |
| Claude Sonnet 4 (Anthropic) | ⚡⚡ Medium | 💰💰 $0.15/run | ⭐⭐⭐⭐⭐ Best | ☁️ Cloud |

**Recommendation:** Start with `--ollama` (free, fast, private). Only use cloud APIs if you need the absolute best quality.

---

## 🔧 Troubleshooting

### **Ollama not working?**
```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### **Model not found?**
```bash
# Pull the recommended model
ollama pull gpt-oss:20b-cloud
```

### **Want to see all options?**
```bash
poetry run python src/main.py --help
```

---

## 💡 Pro Tips

1. **Start with Conservative strategy** - It's faster (only 3 analysts) and good for most stocks
2. **Use --ollama flag** - Your local GPT-OSS 20B is already great
3. **Save API costs** - Run unlimited analyses for free with Ollama
4. **Batch analysis** - Analyze multiple stocks in one command: `--tickers AAPL,MSFT,GOOGL`
5. **Use --show-reasoning** - Learn what each analyst is thinking

---

## 📚 Learn More

- Full documentation: [README.md](README.md)
- What changed: [SIMPLIFICATION_SUMMARY.md](SIMPLIFICATION_SUMMARY.md)
- Test it works: `poetry run pytest tests/ -v`

---

**Ready to start!** 🎉

Try this now:
```bash
poetry run python src/main.py --tickers AAPL --strategy conservative --ollama
```
