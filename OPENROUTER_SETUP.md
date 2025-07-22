# OpenRouter Setup Guide

## Overview

Your research system has been configured to use **OpenRouter exclusively** for all LLM models, including GPT-4, Claude 3 Sonnet, and DeepSeek R1. This simplifies the setup by requiring only one API key.

## Quick Setup

### 1. Get OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up or log in
3. Navigate to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-...`)

### 2. Configure Environment

1. **Check if .env file exists:**
   ```bash
   ls -la .env
   ```

2. **If .env doesn't exist, create it:**
   ```bash
   cp .env.example .env
   ```

3. **Edit .env file and add your OpenRouter key:**
   ```
   OPENROUTER_API_KEY=sk-or-your-key-here
   ```

### 3. Test Your Setup

Run the test script to verify everything works:

```bash
python test_openrouter_setup.py
```

This will test:
- ✅ Environment configuration
- ✅ OpenRouter client connection
- ✅ Access to all 3 models (GPT-4, Claude 3 Sonnet, DeepSeek R1)
- ✅ Research data loading (245 prompts)
- ✅ Concurrent runner initialization

## Running Your Research

### Option 1: Command Line (Recommended)

Run the full concurrent experiment:

```bash
python concurrent_research_runner.py
```

This will:
- Process all 245 research prompts
- Test across GPT-4, Claude 3 Sonnet, and DeepSeek R1
- Use concurrent processing (5 requests at a time)
- Generate coded responses with 13 research variables
- Export results to `research_logs/research_data_[timestamp].csv`
- Run statistical analysis automatically

**Expected time:** 15-30 minutes for all 735 combinations (245 prompts × 3 models)

### Option 2: Streamlit Interface

Launch the web interface:

```bash
streamlit run streamlit_research_app.py
```

Navigate to "🚀 Run Concurrent Experiment" to configure and run experiments.

## What You'll Get

### Research Data
- **CSV file** with all responses and coding variables
- **JSON files** with statistical analysis results
- **Session logs** with detailed experiment metadata

### Key Research Variables (13 total)
1. **Pronoun Usage** (0-3): Anchoring and relational stance
2. **Role Assumption** (0-3): Ethical positioning
3. **Perspective Complexity** (0-2): Viewpoint multiplicity
4. **Ethical Mode** (D/C/R/V/S/M): Dominant moral logic
5. **Distributed Agency** (0-2): Responsibility sharing
6. **Moral Plurality** (0-2): Multiple ethical perspectives
7. **Shamanic/Cosmological Markers** (0-2): Non-modern reasoning
8. And 6 more variables...

### Statistical Analysis
- **ANOVA tests** for deictic framing effects
- **Hypothesis testing** for shamanic framing
- **Effect sizes** and significance levels
- **Model comparisons** across GPT-4, Claude, DeepSeek

## Models & Pricing

All models accessed via OpenRouter:

| Model | OpenRouter ID | Approx. Cost per 1K tokens |
|-------|---------------|---------------------------|
| GPT-4 | `openai/gpt-4` | $0.03 input / $0.06 output |
| Claude 3 Sonnet | `anthropic/claude-3-sonnet` | $0.003 input / $0.015 output |
| DeepSeek R1 | `deepseek/deepseek-r1` | $0.0014 input / $0.0028 output |

**Estimated total cost for full experiment:** $15-25 USD

## Troubleshooting

### Common Issues

1. **"OpenRouter API Key missing"**
   - Check your .env file exists and contains `OPENROUTER_API_KEY=sk-or-...`
   - Restart your terminal/IDE after editing .env

2. **"No response generated"**
   - Check your OpenRouter account has sufficient credits
   - Verify internet connection
   - Try reducing `max_concurrent` from 5 to 2

3. **"No research data found"**
   - This is normal before running your first experiment
   - Run `python concurrent_research_runner.py` to generate data

4. **Import errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're in the correct directory

### Rate Limits

OpenRouter has generous rate limits, but if you encounter issues:
- Reduce `max_concurrent` from 5 to 2-3
- Increase `delay_between_batches` from 1.0 to 2.0 seconds

## Research Integrity Features

✅ **Stateless API calls** - No system prompts that could bias responses  
✅ **Concurrent processing** - Efficient data collection  
✅ **Comprehensive logging** - Full session tracking  
✅ **Automated coding** - 13 research variables per response  
✅ **Statistical analysis** - Hypothesis testing built-in  

## Next Steps

1. **Test setup:** `python test_openrouter_setup.py`
2. **Run experiment:** `python concurrent_research_runner.py`
3. **View results:** `streamlit run streamlit_research_app.py`
4. **Analyze data:** Check `research_logs/` directory

Your 245 research prompts across 5 deictic framings are ready to test how different prompting approaches affect LLM ethical reasoning!
