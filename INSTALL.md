# Installation Guide - Deixis AI Agent

## Quick Setup with Virtual Environment

### 1. Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show venv path)
where python
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

### 2. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# Required: OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Test Installation

```bash
# Run system tests
python test_system.py

# Should show: 🎉 All tests passed! System is ready for use.
```

### 5. Start Application

```bash
# Launch Streamlit app
streamlit run app.py

# Open browser to: http://localhost:8501
```

## Detailed Setup Instructions

### Prerequisites

- **Python 3.9+** (recommended: Python 3.10 or 3.11)
- **OpenAI API Key** (required for LLM integration)
- **Git** (for cloning repository)

### Verify Python Version

```bash
python --version
# Should show: Python 3.9.x or higher
```

### Install System Dependencies

**Windows:**
```bash
# No additional system dependencies required
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python if needed
brew install python
```

**Ubuntu/Debian:**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install additional dependencies for some packages
sudo apt install build-essential
```

### Virtual Environment Best Practices

1. **Always use a virtual environment** to avoid conflicts
2. **Activate before installing** any packages
3. **Deactivate when done** working on the project

```bash
# Deactivate virtual environment when done
deactivate
```

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for future expansion)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Database Configuration
DATABASE_PATH=data/responses.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/deixis_agent.log

# Model Configuration
MAX_TOKENS=2000
TEMPERATURE=0.7
BATCH_SIZE=10
```

### Troubleshooting

#### Common Issues

**1. Python version too old:**
```bash
# Check version
python --version

# If < 3.9, install newer Python version
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: Use pyenv or compile from source
```

**2. Virtual environment activation fails:**
```bash
# Windows: Try different activation script
venv\Scripts\activate.bat
# or
venv\Scripts\Activate.ps1

# macOS/Linux: Check shell
echo $SHELL
# Use appropriate activation script
```

**3. Package installation fails:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages one by one to identify issues
pip install streamlit
pip install openai
# etc.
```

**4. OpenAI API errors:**
```bash
# Verify API key is set
python -c "import os; print('API Key set:', bool(os.getenv('OPENAI_API_KEY')))"

# Test API connection
python -c "
from llm.openai_client import OpenAIClient
client = OpenAIClient()
print('Connection test:', client.test_connection())
"
```

**5. Database permission errors:**
```bash
# Ensure data directory exists and is writable
mkdir -p data logs exports templates
chmod 755 data logs exports templates
```

#### Performance Optimization

**For better performance:**

1. **Use SSD storage** for database operations
2. **Increase batch size** for bulk processing (if API limits allow)
3. **Use faster Python** (PyPy for CPU-intensive tasks)
4. **Enable GPU** for UMAP clustering (if available)

```bash
# Install GPU-accelerated packages (optional)
pip install cupy-cuda11x  # For NVIDIA GPUs
pip install umap-learn[plot]  # Enhanced UMAP
```

### Development Setup

**For contributors:**

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run code formatting
black .
flake8 .
mypy .

# Run tests
pytest tests/
```

### Docker Setup (Alternative)

**If you prefer Docker:**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t deixis-ai-agent .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key deixis-ai-agent
```

### Verification Checklist

After installation, verify these components work:

- [ ] Virtual environment activated
- [ ] All packages installed without errors
- [ ] Environment variables configured
- [ ] System tests pass (6/6)
- [ ] Streamlit app launches
- [ ] OpenAI API connection successful
- [ ] Database operations working
- [ ] Prompt generation functional
- [ ] Annotation pipeline operational

### Getting Help

If you encounter issues:

1. **Check the logs** in `logs/deixis_agent.log`
2. **Run system tests** to identify specific problems
3. **Verify environment** variables are set correctly
4. **Check API quotas** and rate limits
5. **Review error messages** for specific guidance

### Next Steps

Once installed successfully:

1. **Configure your OpenAI API key**
2. **Run the system tests** to verify everything works
3. **Launch the Streamlit app** and explore the interface
4. **Try the prompt testing** feature with sample dilemmas
5. **Create your first batch experiment**
6. **Explore the visualization** features

🎉 **You're ready to start analyzing ethical dilemmas through deictic framings!**