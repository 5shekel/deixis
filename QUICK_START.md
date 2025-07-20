# Quick Start Guide - AI Agent System for Deictic Ethics Research

## System Overview

This AI agent system is configured to run your 245 research prompts from `Extended_Prompt_Set_with_Shamanic_Deixis.csv` across multiple LLM models with comprehensive logging and analysis.

**🔬 RESEARCH INTEGRITY**: The system uses **stateless API calls with NO system prompts** to ensure pure model responses without bias. This allows you to study how models naturally enact their training on ethical dilemmas.

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage Options

### Option 1: Comprehensive Research Interface (Recommended)
```bash
streamlit run streamlit_research_app.py
```
- **Complete research dashboard** with all 245 prompts integrated
- **Run concurrent experiments** directly from the interface
- **Statistical analysis** with hypothesis testing
- **Data visualization** and exploration tools
- **Research design documentation** built-in

### Option 1b: Basic Streamlit Interface
```bash
streamlit run app.py
```
- Navigate to Research Mode
- Test individual prompts interactively
- View real-time research coding

### Option 2: Concurrent Research Runner (Recommended for Full Research)
```bash
python concurrent_research_runner.py
```
- **Concurrent processing**: Multiple models respond simultaneously
- **Stateless API calls**: Pure research integrity, no system prompts
- **Full coding scheme**: Uses `Full_LLM_Coding_Scheme_with_Prompting.csv`
- **Efficient**: Processes all 245 prompts across multiple models quickly
- **Comprehensive logging**: Complete session tracking and analysis

### Option 3: Legacy Batch Processing
```bash
python batch_research_runner.py
```
- Sequential processing (slower but more conservative)
- Tests multiple LLM models (GPT-4, Claude 3, DeepSeek R1)
- Generates comprehensive logs for analysis

### Option 4: Test System First
```bash
python test_integration.py
```
- Verifies all components are working
- Shows sample prompts and statistics
- Confirms research data loading

## Your Research Data

### Prompts Loaded
- **245 prompts** from your CSV file
- **49 ethical dilemmas** 
- **5 deictic framings** per dilemma:
  - Anchored Chain-of-Thought
  - Role-Based Deictic
  - Cosmological / Perspective-Shifting
  - Neutral (No Deixis)
  - Shamanic / Cosmological Deixis

### Research Coding
Each response is coded with 13 variables:
- Pronoun usage, role assumption, perspective complexity
- Ethical mode, distributed agency, deictic reframing
- Stance clarity, moral plurality, ontological perspective
- Shamanic/cosmological markers, prompting technique
- Reasoning steps count, dialogic simulation

## Output Files

After running batch processing, check `research_logs/` directory:
- `research_data_[timestamp].csv` - All responses with coding variables
- `sessions/session_[timestamp].json` - Complete session metadata
- `experiment_summary_[timestamp].json` - Experiment overview
- Individual response and coding files

## Troubleshooting

### Missing API Keys
- Make sure `.env` file contains valid API keys
- OpenAI API key is required for GPT-4
- OpenRouter API key is optional (for Claude 3, DeepSeek R1)

### Import Errors
- Run `pip install -r requirements.txt` to install all dependencies
- For async batch processing, install: `pip install aiohttp`

### File Not Found
- Ensure `files/Extended_Prompt_Set_with_Shamanic_Deixis.csv` exists
- Check that the CSV file has the correct column headers

## Next Steps

1. Test the system with `python test_integration.py`
2. Try the web interface with `streamlit run app.py`
3. Run full batch processing with `python batch_research_runner.py`
4. Analyze results in `research_logs/` directory

Your research prompts are now fully integrated and ready for systematic analysis across multiple LLM architectures!