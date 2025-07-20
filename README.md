# Deixis AI Agent: Comprehensive Research System for Ethical AI Analysis

**A sophisticated AI research platform designed to systematically analyze how different deictic framings influence Large Language Model (LLM) responses to ethical dilemmas through rigorous experimental design, statistical analysis, and comprehensive data collection.**

## 🎯 What This System Does

The Deixis AI Agent is a complete research framework that investigates how the way we frame questions (deictic positioning) affects how AI models reason about ethical problems. It provides researchers with tools to:

1. **Generate Systematic Prompts**: Create 245+ research-validated ethical dilemma prompts across 5 different deictic framings
2. **Test Multiple AI Models**: Simultaneously query OpenAI GPT-4, Claude, DeepSeek, and other LLMs
3. **Analyze Responses**: Apply a 13-variable coding scheme to categorize ethical reasoning patterns
4. **Statistical Testing**: Perform ANOVA, Chi-square, and Mann-Whitney U tests to validate hypotheses
5. **Visualize Results**: Generate interactive charts, heatmaps, and statistical plots
6. **Export Research Data**: Create publication-ready datasets and analysis reports

## 🔬 Core Research Question

**How do different deictic framings (ways of positioning the reader/AI in relation to ethical problems) influence the ethical reasoning patterns of Large Language Models?**

### Research Hypothesis
Different deictic framings will produce statistically significant variations in LLM ethical reasoning patterns, with shamanic/ontological framings showing increased perspective complexity and distributed agency compared to neutral framings.

## 🧠 The Five Deictic Framings

### 1. **Anchored Chain-of-Thought**
- **Position**: First-person perspective ("I need to think through this...")
- **Purpose**: Grounds the AI in systematic, step-by-step reasoning
- **Example**: "I need to carefully consider this ethical dilemma step by step, thinking through my own moral framework..."

### 2. **Role-Based Deictic** 
- **Position**: Second-person perspective with specific roles ("As an ethical advisor, you must...")
- **Purpose**: Tests how role assignment affects ethical reasoning
- **Example**: "As an ethical decision-maker responsible for community welfare, you must weigh the following considerations..."

### 3. **Cosmological/Perspective-Shifting**
- **Position**: Expanded temporal and spatial awareness ("From the perspective of future generations...")
- **Purpose**: Examines how broader temporal/spatial framing affects decisions
- **Example**: "Considering this dilemma from the perspective of future generations and the interconnectedness of all life..."

### 4. **Neutral (No Deixis)**
- **Position**: Direct, objective framing without explicit positioning
- **Purpose**: Baseline condition for comparison
- **Example**: "This ethical dilemma requires analysis of the following factors and stakeholder considerations..."

### 5. **Shamanic/Ontological Deixis**
- **Position**: Ancestral wisdom and multi-species perspective ("Drawing upon ancestral wisdom...")
- **Purpose**: Tests indigenous/non-Western ethical frameworks
- **Example**: "Drawing upon ancestral wisdom and considering the voices of all beings affected, including future generations and the natural world..."

## 📊 The 13-Variable Research Coding Scheme

Each AI response is systematically analyzed using this comprehensive framework:

### Core Linguistic Variables
1. **Pronoun Usage** (0-3): None → Low → Moderate → High first/second person usage
2. **Role Assumption** (0-3): None → Implied → Explicit role → Invented role
3. **Perspective Complexity** (0-2): Single POV → Acknowledged others → Perspective shift
4. **Distributed Agency** (0-2): None → Implied → Explicit distribution of responsibility

### Ethical Reasoning Variables
5. **Ethical Mode**: D=Deontological, C=Consequentialist, R=Relational/Care, V=Virtue, S=Shamanic, M=Mixed
6. **Stance Clarity** (0-2): Unclear → Partial → Clear ethical position
7. **Moral Plurality** (0-2): Singular frame → Minimal plurality → Multiple ethical frameworks
8. **Deictic Reframing** (0-2): None → Partial reframe → Full reframe of the problem

### Advanced Analysis Variables
9. **Ontological Perspective** (0-2): None → Implied being → Explicit ontological framework
10. **Shamanic/Cosmological Markers** (0-2): None → Metaphor only → Embodied cosmology
11. **Prompting Technique**: CoT=Chain-of-Thought, J=Jailbreak, R=Role-play, S=Socratic, D=Direct, F=Few-shot, M=Meta
12. **Reasoning Steps Count** (0-5+): Number of explicit reasoning steps
13. **Dialogic Simulation** (0-3): None → Monologic → Simulated dialog → Multi-perspectival

## 🚀 System Architecture & Components

### 1. **Core Prompt Engine** ([`core/prompt_engine.py`](core/prompt_engine.py))
- Generates contextually appropriate prompts for each deictic framing
- Integrates 245 research-validated ethical dilemmas
- Supports both basic and research-grade prompt generation
- Handles role-based customization and cultural context

### 2. **Multi-LLM Integration** ([`llm/`](llm/))
- **OpenAI Client**: GPT-4, GPT-4-Turbo integration with rate limiting
- **OpenRouter Client**: Claude-3-Opus, Claude-3-Sonnet, DeepSeek-R1 support
- Stateless API calls ensuring research integrity (no system prompts)
- Comprehensive error handling and retry logic

### 3. **Research Data Management** ([`storage/database.py`](storage/database.py))
- SQLite database for structured response storage
- JSONL export for research data portability
- Automatic metadata tracking (timestamps, tokens, processing time)
- Experiment grouping and batch management

### 4. **Advanced Annotation System** ([`analysis/`](analysis/))
- **Response Annotator**: Basic ethical stance classification
- **Research Coder**: 13-variable comprehensive analysis
- **Statistical Analysis**: ANOVA, Chi-square, Mann-Whitney U tests
- Automated hypothesis testing with effect size calculations

### 5. **Concurrent Processing** ([`concurrent_research_runner.py`](concurrent_research_runner.py))
- ThreadPoolExecutor for simultaneous multi-model testing
- Progress tracking and real-time status updates
- Automatic statistical analysis integration
- Rate limiting and error recovery

### 6. **Comprehensive Logging** ([`utils/research_logger.py`](utils/research_logger.py))
- Session-based research activity tracking
- Detailed prompt and response logging
- Research coding preservation
- Export capabilities for research reproducibility

### 7. **Interactive Web Interface** ([`app.py`](app.py) & [`streamlit_research_app.py`](streamlit_research_app.py))
- **Basic Interface**: Single prompt testing and batch experiments
- **Research Interface**: 6-module comprehensive research dashboard
- Real-time visualization and data exploration
- Statistical analysis integration

## 📈 Research Dashboard Modules

### Module 1: Research Overview
- Dataset statistics (245 prompts, 5 framings, multiple categories)
- Research hypothesis presentation
- Sample prompt examples by framing type
- Distribution analysis of ethical categories

### Module 2: Concurrent Experiment Runner
- Multi-model selection (GPT-4, Claude, DeepSeek)
- Configurable framing combinations
- Real-time progress tracking
- Automatic result compilation

### Module 3: Statistical Analysis
- Hypothesis testing (ANOVA for continuous variables)
- Chi-square tests for categorical variables
- Mann-Whitney U tests for non-parametric comparisons
- Effect size calculations (Cohen's d, Cramér's V)
- Automated report generation

### Module 4: Research Design Documentation
- Formal methodology documentation
- Variable definitions and coding schemes
- Expected outcomes and research questions
- Experimental design specifications

### Module 5: Data Explorer
- Interactive response browsing
- Filter by model, framing, ethical category
- Search functionality across responses
- Export selected datasets

### Module 6: Visualizations
- Ethical stance distribution charts
- Pronoun usage pattern analysis
- Deictic effectiveness heatmaps
- Response clustering visualization
- Temporal analysis of model behavior

## 🔬 Research Workflow

### Phase 1: Experimental Setup
1. **Configure API Keys**: Add OpenAI, Anthropic, or OpenRouter credentials
2. **Select Models**: Choose from available LLM providers
3. **Define Parameters**: Set framing types, prompt counts, concurrent workers
4. **Initialize Logging**: Start research session tracking

### Phase 2: Data Collection
1. **Concurrent Execution**: Run experiments across multiple models simultaneously
2. **Response Storage**: Automatically store all responses with metadata
3. **Progress Monitoring**: Real-time tracking of experiment completion
4. **Error Handling**: Automatic retry and failure recovery

### Phase 3: Analysis & Coding
1. **Automated Coding**: Apply 13-variable scheme to all responses
2. **Statistical Testing**: Run hypothesis tests on collected data
3. **Effect Size Calculation**: Determine practical significance of findings
4. **Pattern Recognition**: Identify trends across framings and models

### Phase 4: Visualization & Export
1. **Interactive Charts**: Generate publication-ready visualizations
2. **Statistical Reports**: Create comprehensive analysis summaries
3. **Data Export**: Export in multiple formats (CSV, JSON, Excel)
4. **Research Documentation**: Generate methodology and results documentation

## 📊 Statistical Analysis Capabilities

### Hypothesis Testing Framework
- **Primary Hypothesis**: Deictic framing effects on ethical reasoning patterns
- **Secondary Hypotheses**: Model-specific response variations
- **Control Variables**: Prompt complexity, ethical category, response length

### Statistical Tests Implemented
1. **ANOVA**: For continuous variables (pronoun usage, reasoning steps)
2. **Chi-square**: For categorical variables (ethical mode, stance clarity)
3. **Mann-Whitney U**: For non-parametric comparisons
4. **Effect Size Calculations**: Cohen's d, Cramér's V, eta-squared

### Research Integrity Features
- **Stateless API Calls**: No system prompts to bias responses
- **Randomization**: Prompt order randomization to prevent bias
- **Replication Support**: Complete experimental reproducibility
- **Blind Analysis**: Automated coding reduces researcher bias

## 🛠️ Technical Implementation

### Core Technologies
- **Python 3.9+**: Core programming language
- **Streamlit**: Interactive web interface
- **SQLite**: Local database for response storage
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization
- **SciPy**: Statistical testing
- **ThreadPoolExecutor**: Concurrent processing
- **Pydantic**: Data validation and schemas

### API Integrations
- **OpenAI API**: GPT-4, GPT-4-Turbo
- **OpenRouter API**: Claude-3-Opus, Claude-3-Sonnet, DeepSeek-R1
- **Rate Limiting**: Automatic throttling to respect API limits
- **Error Recovery**: Exponential backoff and retry logic

### Data Storage Architecture
```
research_logs/
├── sessions/           # Research session metadata
├── responses/          # Raw LLM responses with metadata
├── codings/           # 13-variable coding results
├── analysis/          # Statistical analysis results
└── research_data_*.csv # Exportable research datasets
```

## 📁 Complete Project Structure

```
deixis-ai-agent/
├── app.py                          # Main Streamlit interface
├── streamlit_research_app.py       # Comprehensive research dashboard
├── concurrent_research_runner.py   # Multi-model concurrent processing
├── batch_research_runner.py        # Batch experiment management
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── RESEARCH_DESIGN.md              # Formal research methodology
├── INSTALL.md                      # Installation instructions
├── QUICK_START.md                  # Quick start guide
│
├── models/                         # Data schemas and models
│   ├── __init__.py
│   └── schemas.py                  # Pydantic data models
│
├── core/                           # Core prompt engine
│   ├── __init__.py
│   └── prompt_engine.py            # Deictic prompt generation
│
├── llm/                            # LLM integrations
│   ├── __init__.py
│   ├── openai_client.py            # OpenAI API client
│   └── openrouter_client.py        # OpenRouter API client
│
├── storage/                        # Database management
│   ├── __init__.py
│   └── database.py                 # SQLite operations
│
├── analysis/                       # Analysis pipeline
│   ├── __init__.py
│   ├── annotator.py                # Basic response annotation
│   ├── research_coding.py          # 13-variable coding scheme
│   └── research_statistics.py      # Statistical analysis
│
├── visualization/                  # Charts and plots
│   ├── __init__.py
│   └── charts.py                   # Plotly visualizations
│
├── data/                           # Data sources
│   ├── ethical_dilemmas.py         # Basic ethical dilemmas
│   ├── research_prompts.py         # 245 research prompts
│   └── responses.db                # SQLite database
│
├── utils/                          # Utilities
│   ├── __init__.py
│   └── research_logger.py          # Research activity logging
│
├── files/                          # Research data files
│   ├── Extended_Prompt_Set_with_Shamanic_Deixis.csv
│   ├── Full_LLM_Coding_Scheme_with_Prompting.csv
│   ├── Extended_LLM_Coding_Scheme_with_Shamanic_Markers.csv
│   └── LLM_Coding_Scheme_with_Shamanic_Markers.csv
│
├── research_logs/                  # Research session data
│   ├── sessions/                   # Session metadata
│   ├── responses/                  # Response storage
│   ├── codings/                    # Coding results
│   └── analysis/                   # Statistical results
│
├── logs/                           # System logs
├── exports/                        # Data exports
└── templates/                      # Prompt templates
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- At least one LLM API key (OpenAI recommended)
- 4GB+ RAM for concurrent processing
- Internet connection for API calls

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd deixis-ai-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key_here
# OPENROUTER_API_KEY=your_openrouter_key_here
```

4. **Run the basic interface:**
```bash
streamlit run app.py
```

5. **Or run the comprehensive research dashboard:**
```bash
streamlit run streamlit_research_app.py
```

### Quick Test
1. Navigate to the Configuration page
2. Add your OpenAI API key
3. Go to "Prompt Testing" or "Research Mode"
4. Select an ethical dilemma and framing type
5. Generate a prompt and get an LLM response
6. View the automatic coding results

## 📊 Example Research Outputs

### Statistical Analysis Results
```json
{
  "hypothesis_test": "ANOVA",
  "variable": "pronoun_usage",
  "f_statistic": 12.45,
  "p_value": 0.0001,
  "effect_size": 0.34,
  "interpretation": "Large effect of deictic framing on pronoun usage"
}
```

### Response Coding Example
```json
{
  "pronoun_usage": 3,
  "role_assumption": 2,
  "perspective_complexity": 2,
  "ethical_mode": "M",
  "stance_clarity": 2,
  "shamanic_markers": 1,
  "reasoning_steps_count": 4,
  "prompting_technique": "CoT"
}
```

## 🔬 Research Applications

### Academic Research
- **Computational Ethics**: Study AI moral reasoning patterns
- **Linguistic Anthropology**: Analyze deictic effects on cognition
- **AI Safety**: Understand how framing affects AI alignment
- **Cross-Cultural Studies**: Compare Western vs. indigenous ethical frameworks

### Industry Applications
- **AI Product Development**: Optimize prompt engineering for ethical AI
- **Content Moderation**: Understand bias in AI decision-making
- **Chatbot Design**: Improve ethical reasoning in conversational AI
- **Risk Assessment**: Evaluate AI behavior under different framings

### Educational Use
- **Ethics Courses**: Demonstrate AI ethical reasoning patterns
- **Computational Linguistics**: Study deixis in human-AI interaction
- **Research Methods**: Teach systematic AI evaluation techniques
- **Philosophy of Mind**: Explore AI consciousness and perspective-taking

## 📈 Advanced Features

### Concurrent Processing
- Process multiple models simultaneously
- Configurable worker threads (1-10)
- Automatic rate limiting and error recovery
- Real-time progress tracking

### Statistical Rigor
- Multiple hypothesis testing correction
- Effect size calculations for practical significance
- Non-parametric alternatives for non-normal data
- Confidence interval reporting

### Data Export Options
- **CSV**: For statistical software (R, SPSS, Python)
- **JSON**: For programmatic analysis
- **Excel**: For manual review and annotation
- **JSONL**: For machine learning pipelines

### Visualization Suite
- Interactive Plotly charts
- Exportable PNG/PDF formats
- Customizable color schemes
- Statistical overlay options

## 🔧 Configuration Options

### Model Parameters
```python
TEMPERATURE = 0.7          # Response randomness (0.0-2.0)
MAX_TOKENS = 2000         # Maximum response length
BATCH_SIZE = 10           # Concurrent requests
RETRY_ATTEMPTS = 3        # API failure retries
RATE_LIMIT_DELAY = 1.0    # Seconds between requests
```

### Research Settings
```python
MAX_PROMPTS_PER_FRAMING = 50    # Experiment size
CONCURRENT_WORKERS = 3          # Parallel processing
STATISTICAL_ALPHA = 0.05        # Significance threshold
EFFECT_SIZE_THRESHOLD = 0.3     # Practical significance
```

## 🚧 Future Enhancements

### Planned Research Features
- **Multilingual Support**: Spanish, French, Basque ethical dilemmas
- **Cultural Adaptation**: Region-specific ethical frameworks
- **Longitudinal Studies**: Track model changes over time
- **Fine-tuning Analysis**: Compare base vs. fine-tuned models

### Technical Improvements
- **Local Model Support**: Llama, Mistral integration
- **GPU Acceleration**: Faster local processing
- **Cloud Deployment**: Scalable research infrastructure
- **API Rate Optimization**: Intelligent request batching

### Analysis Extensions
- **Machine Learning**: Predictive modeling of ethical stances
- **Network Analysis**: Relationship mapping between variables
- **Causal Inference**: Identify causal relationships in data
- **Meta-Analysis**: Combine results across studies

## 📄 Research Ethics & Compliance

### Ethical Considerations
- **No Human Subjects**: All testing involves AI systems only
- **Bias Awareness**: Systematic documentation of potential biases
- **Transparency**: Open methodology and reproducible results
- **Cultural Sensitivity**: Respectful treatment of indigenous perspectives

### Data Privacy
- **No Personal Data**: Only AI responses are collected
- **Local Storage**: All data stored locally by default
- **Anonymization**: No identifying information in exports
- **Secure APIs**: Encrypted communication with LLM providers

## 📞 Support & Contributing

### Getting Help
- Check the [INSTALL.md](INSTALL.md) for setup issues
- Review [QUICK_START.md](QUICK_START.md) for basic usage
- Examine [RESEARCH_DESIGN.md](RESEARCH_DESIGN.md) for methodology

### Contributing
- Fork the repository and create feature branches
- Follow Python PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for changes

### Reporting Issues
- Use GitHub Issues for bug reports
- Include system information and error logs
- Provide minimal reproduction examples
- Tag issues appropriately (bug, enhancement, question)

---

## 🎯 Summary

The Deixis AI Agent is a comprehensive research platform that enables systematic investigation of how deictic framing affects AI ethical reasoning. With 245 research prompts, 5 deictic framings, a 13-variable coding scheme, and integrated statistical analysis, it provides researchers with everything needed to conduct rigorous studies of AI moral cognition.

The system combines theoretical rigor with practical usability, offering both simple single-prompt testing and sophisticated concurrent multi-model experiments. Its comprehensive logging, statistical testing, and visualization capabilities make it suitable for academic research, industry applications, and educational use.

**Key Strengths:**
- ✅ Research-grade experimental design
- ✅ Comprehensive statistical analysis
- ✅ Multi-model concurrent processing
- ✅ Complete data provenance and reproducibility
- ✅ Interactive visualization and exploration
- ✅ Flexible export and integration options

This system represents a significant advancement in AI ethics research methodology, providing tools to systematically study how the framing of ethical questions influences AI moral reasoning patterns.