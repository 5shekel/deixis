# Research Design: Deictic Framing Effects on LLM Ethical Reasoning

## Research Hypothesis

**Primary Hypothesis**: Large Language Models (LLMs) respond differently to ethical dilemmas depending on the deictic framing and prompting technique used. Specifically, prompts that invoke relational, cosmological, or shamanic deixis will lead to more distributed, plural, and ethically reflective responses than those that rely on anchored or neutral frames. This variation reveals latent ethical preferences and ontological commitments embedded in the LLM's training and architecture.

## Research Questions

1. **Which prompt styles activate which ethical dispositions?**
   - Do shamanic/cosmological framings increase relational ethics markers?
   - Do anchored CoT prompts favor consequentialist reasoning?
   - Do role-based prompts increase perspective complexity?

2. **Do LLMs exhibit latent preferences for specific ethical framings?**
   - Are certain models more responsive to particular deictic frames?
   - Do models show consistent ethical mode preferences across dilemmas?
   - How do architectural differences (GPT-4 vs Claude vs DeepSeek) affect ethical reasoning patterns?

3. **Can deixis be used as a design lever for culturally-responsive AI?**
   - Do shamanic/cosmological prompts activate non-Western ethical frameworks?
   - Can deictic framing increase moral plurality and perspective-taking?
   - How might this inform AI system design for diverse cultural contexts?

## Experimental Design

### Independent Variables (Manipulated)

| Variable | Levels | Description |
|----------|--------|-------------|
| **Deictic Framing** | 5 levels | Anchored CoT, Role-Based, Cosmological, Shamanic, Neutral |
| **LLM Model** | 3+ levels | GPT-4, Claude 3 Sonnet, DeepSeek R1 |
| **Ethical Dilemma** | 49 levels | Professional, medical, personal, AI ethics, etc. |
| **Prompting Technique** | 7 levels | CoT, Justification, Reflective, Socratic, Deliberative, Freeform, Mixed |

### Dependent Variables (Measured)

| Variable | Scale | Research Significance |
|----------|-------|----------------------|
| **Pronoun Usage** | 0-3 | Indicates degree of anchoring and relational stance |
| **Role Assumption** | 0-3 | Shows how models position themselves ethically |
| **Perspective Complexity** | 0-2 | Measures viewpoint multiplicity and sophistication |
| **Ethical Mode** | D/C/R/V/S/M | Reveals dominant moral logic (deontological, consequentialist, relational, virtue, shamanic, mixed) |
| **Distributed Agency** | 0-2 | Shows whether responsibility is shared or centralized |
| **Deictic Reframing** | 0-2 | Measures how models reinterpret moral positioning |
| **Stance Clarity** | 0-2 | Indicates decisiveness vs. ambiguity in ethical positions |
| **Moral Plurality** | 0-2 | Measures acknowledgment of multiple valid ethical perspectives |
| **Ontological Perspective** | 0-2 | Captures use of non-human or metaphysical frames |
| **Shamanic/Cosmological Markers** | 0-2 | Evidence of mythic, spiritual, or non-modern reasoning |
| **Reasoning Steps Count** | 0-5+ | Quantifies explicit logical progression |
| **Dialogic Simulation** | 0-3 | Measures simulation of conversation, deliberation, or multiplicity |

## Methodology

### Data Collection Protocol

1. **Stateless API Calls**: No system prompts to ensure pure model responses
2. **Concurrent Processing**: Multiple models respond to identical prompts simultaneously
3. **Comprehensive Logging**: Every prompt, response, and coding decision tracked
4. **Blind Coding**: Automated coding system applies consistent criteria

### Sample Size

- **245 total prompts** (49 dilemmas × 5 deictic framings)
- **735+ total responses** (245 prompts × 3+ models)
- **Sufficient power** for detecting medium effect sizes in ethical reasoning patterns

### Data Analysis Plan

#### Primary Analyses

1. **ANOVA**: Deictic Framing × Model × Dilemma Type effects on ethical variables
2. **Regression Analysis**: Predicting ethical modes from deictic framing and model type
3. **Cluster Analysis**: Identifying latent ethical reasoning profiles across models
4. **Network Analysis**: Mapping relationships between deictic frames and ethical outcomes

#### Secondary Analyses

1. **Interaction Effects**: How model architecture moderates deictic framing effects
2. **Dilemma-Specific Patterns**: Which ethical domains are most sensitive to deictic manipulation
3. **Temporal Consistency**: Whether models show stable ethical preferences across prompts
4. **Cross-Cultural Validity**: Evidence for non-Western ethical frameworks in responses

## Expected Outcomes

### Hypothesis 1: Deictic Framing Main Effects
- **Shamanic/Cosmological prompts** → Higher scores on:
  - Distributed Agency
  - Moral Plurality
  - Ontological Perspective
  - Shamanic/Cosmological Markers
  - Relational Ethical Mode

- **Anchored CoT prompts** → Higher scores on:
  - Stance Clarity
  - Reasoning Steps Count
  - Consequentialist Ethical Mode
  - Lower Perspective Complexity

### Hypothesis 2: Model-Specific Patterns
- **GPT-4**: More systematic, consequentialist reasoning
- **Claude**: More nuanced, perspective-aware responses
- **DeepSeek**: Potentially different cultural/ethical baselines

### Hypothesis 3: Interaction Effects
- Shamanic framing × Complex dilemmas → Highest moral plurality
- Role-based framing × Professional dilemmas → Highest role assumption
- Cosmological framing × Existential dilemmas → Highest ontological perspective

## Research Significance

### Theoretical Contributions
1. **AI Ethics**: Understanding how prompt design shapes moral reasoning in AI systems
2. **Cultural AI**: Evidence for culturally-responsive AI design through deictic manipulation
3. **Moral Psychology**: Insights into how linguistic framing affects ethical cognition

### Practical Applications
1. **AI System Design**: Guidelines for developing culturally-sensitive AI assistants
2. **Prompt Engineering**: Best practices for eliciting desired ethical reasoning patterns
3. **AI Safety**: Understanding and controlling ethical biases in language models

### Methodological Innovations
1. **Deictic Ethics Framework**: Novel approach to studying AI moral reasoning
2. **Concurrent Multi-Model Testing**: Efficient methodology for comparative AI research
3. **Comprehensive Coding Scheme**: Systematic framework for analyzing ethical responses

## Data Management and Ethics

### Research Integrity
- **Open Science**: All prompts, responses, and coding publicly available
- **Reproducibility**: Complete methodology and code documentation
- **Transparency**: Clear reporting of all analytical decisions and limitations

### Ethical Considerations
- **No Human Subjects**: Research involves only AI systems
- **Bias Awareness**: Systematic examination of potential cultural and ethical biases
- **Responsible AI**: Findings will inform more ethical AI development practices

## Timeline and Deliverables

### Phase 1: Data Collection (1-2 days)
- Run concurrent research experiment
- Generate comprehensive response dataset
- Apply automated coding scheme

### Phase 2: Analysis (1-2 weeks)
- Statistical analysis of deictic framing effects
- Model comparison and interaction analysis
- Pattern identification and visualization

### Phase 3: Reporting (1-2 weeks)
- Research paper draft
- Data visualization and infographics
- Policy recommendations for AI development

## Technical Implementation

The research is implemented through:
- **[`concurrent_research_runner.py`](concurrent_research_runner.py)**: Main experimental system
- **[`files/Extended_Prompt_Set_with_Shamanic_Deixis.csv`](files/Extended_Prompt_Set_with_Shamanic_Deixis.csv)**: Research prompts
- **[`files/Full_LLM_Coding_Scheme_with_Prompting.csv`](files/Full_LLM_Coding_Scheme_with_Prompting.csv)**: Coding framework
- **Comprehensive logging system**: Complete data capture and traceability

This research design provides a rigorous framework for understanding how deictic framing influences AI ethical reasoning, with significant implications for developing more culturally-responsive and ethically-aware AI systems.