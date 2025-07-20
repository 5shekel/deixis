"""
Main Streamlit application for the Deixis AI Agent system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import List, Dict, Any
import time

# Import our modules
from config import Config
from core.prompt_engine import PromptEngine
from llm.openai_client import OpenAIClient
from llm.openrouter_client import OpenRouterClient
from storage.database import DatabaseManager
from analysis.annotator import ResponseAnnotator
from analysis.research_coding import ResearchCoder
from data.ethical_dilemmas import get_sample_dilemmas, get_dilemma_categories
from data.research_prompts import get_research_dilemmas, load_research_prompts, get_research_statistics
from analysis.research_statistics import ResearchStatistics
from concurrent_research_runner import ConcurrentResearchRunner
from models.schemas import DeicticFraming, EthicalStance, LLMModel
from utils.research_logger import research_logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Deixis AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.prompt_engine = None
    st.session_state.openai_client = None
    st.session_state.openrouter_client = None
    st.session_state.db_manager = None
    st.session_state.annotator = None
    st.session_state.research_coder = None

def initialize_system():
    """Initialize the system components."""
    try:
        # Initialize components
        st.session_state.prompt_engine = PromptEngine()
        st.session_state.db_manager = DatabaseManager()
        st.session_state.annotator = ResponseAnnotator()
        st.session_state.research_coder = ResearchCoder()
        
        # Initialize OpenAI client if API key is available
        if Config.OPENAI_API_KEY:
            st.session_state.openai_client = OpenAIClient()
        
        # Initialize OpenRouter client if API key is available
        if Config.OPENROUTER_API_KEY:
            st.session_state.openrouter_client = OpenRouterClient()
        
        st.session_state.initialized = True
        st.success("System initialized successfully!")
        
    except Exception as e:
        st.error(f"Failed to initialize system: {e}")
        logger.error(f"System initialization error: {e}")

def main():
    """Main application function."""
    
    # Title and description
    st.title("🧠 Deixis AI Agent")
    st.markdown("""
    **AI agent for analyzing language model responses to ethical dilemmas through diverse deictic configurations**
    
    This system enables researchers to evaluate how different LLM architectures respond to 
    anchored, role-based, cosmological, and shamanic prompt variants.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "🔧 Configuration", "📝 Prompt Testing", "🔬 Research Mode",
         "📊 Batch Experiments", "🧪 Comprehensive Research", "📈 Analysis & Visualization", "💾 Data Management"]
    )
    
    # Initialize system if not done
    if not st.session_state.initialized:
        st.sidebar.warning("System not initialized")
        if st.sidebar.button("Initialize System"):
            initialize_system()
    else:
        st.sidebar.success("System ready")
    
    # Route to appropriate page
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔧 Configuration":
        show_configuration_page()
    elif page == "📝 Prompt Testing":
        show_prompt_testing_page()
    elif page == "🔬 Research Mode":
        show_research_mode_page()
    elif page == "📊 Batch Experiments":
        show_batch_experiments_page()
    elif page == "📈 Analysis & Visualization":
        show_analysis_page()
    elif page == "💾 Data Management":
        show_data_management_page()

def show_home_page():
    """Display the home page with system overview."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("System Overview")
        
        st.subheader("🎯 Core Functionalities")
        st.markdown("""
        1. **Prompt Engine**: Generates prompts across five deictic framings
        2. **LLM Orchestration**: Interfaces with multiple LLM APIs
        3. **Annotation Assistant**: Auto-tags outputs for linguistic and ethical variables
        4. **Visualization Suite**: Generates comparative plots and analysis
        """)
        
        st.subheader("🔬 Deictic Framings")
        framings_info = {
            "Anchored Chain-of-Thought": "First-person perspective with systematic reasoning",
            "Role-Based Deictic": "Second-person perspective with role-specific considerations",
            "Cosmological/Perspective-Shifting": "Expanded temporal and spatial awareness",
            "Neutral (No Deixis)": "Direct, objective framing without explicit anchoring",
            "Shamanic/Ontological Deixis": "Ancestral wisdom and multi-species perspective"
        }
        
        for framing, description in framings_info.items():
            st.markdown(f"**{framing}**: {description}")
    
    with col2:
        st.header("System Status")
        
        if st.session_state.initialized:
            # Show system statistics
            if st.session_state.db_manager:
                stats = st.session_state.db_manager.get_experiment_stats()
                
                st.metric("Total Responses", stats.get('total_responses', 0))
                st.metric("Total Annotations", stats.get('total_annotations', 0))
                st.metric("Unique Dilemmas", stats.get('unique_dilemmas', 0))
                st.metric("Experiments", stats.get('total_experiments', 0))
            
            # API Status
            st.subheader("API Status")
            if st.session_state.openai_client:
                if st.button("Test OpenAI Connection"):
                    with st.spinner("Testing connection..."):
                        success = st.session_state.openai_client.test_connection()
                        if success:
                            st.success("✅ OpenAI API connected")
                        else:
                            st.error("❌ OpenAI API connection failed")
            else:
                st.warning("⚠️ OpenAI API key not configured")
        
        else:
            st.warning("System not initialized. Please initialize from the sidebar.")

def show_configuration_page():
    """Display the configuration page."""
    st.header("⚙️ System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Configuration")
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key", 
            value=Config.OPENAI_API_KEY or "",
            type="password",
            help="Enter your OpenAI API key"
        )
        
        if st.button("Update OpenAI Key"):
            if openai_key:
                try:
                    st.session_state.openai_client = OpenAIClient(api_key=openai_key)
                    st.success("OpenAI client updated successfully!")
                except Exception as e:
                    st.error(f"Failed to update OpenAI client: {e}")
            else:
                st.warning("Please enter a valid API key")
        
        st.subheader("Model Settings")
        
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=2.0, 
            value=Config.TEMPERATURE,
            step=0.1,
            help="Controls randomness in responses"
        )
        
        max_tokens = st.number_input(
            "Max Tokens", 
            min_value=100, 
            max_value=4000, 
            value=Config.MAX_TOKENS,
            help="Maximum tokens in response"
        )
        
        batch_size = st.number_input(
            "Batch Size", 
            min_value=1, 
            max_value=50, 
            value=Config.BATCH_SIZE,
            help="Number of prompts to process in batch"
        )
    
    with col2:
        st.subheader("Database Configuration")
        
        st.text_input(
            "Database Path", 
            value=Config.DATABASE_PATH,
            disabled=True,
            help="SQLite database file path"
        )
        
        if st.session_state.db_manager:
            stats = st.session_state.db_manager.get_experiment_stats()
            st.json(stats)
        
        st.subheader("Logging Configuration")
        
        log_level = st.selectbox(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,
            help="Logging verbosity level"
        )
        
        st.text_input(
            "Log File Path",
            value=Config.LOG_FILE,
            disabled=True,
            help="Log file location"
        )

def show_prompt_testing_page():
    """Display the prompt testing page."""
    st.header("📝 Prompt Testing")
    
    if not st.session_state.initialized:
        st.warning("Please initialize the system first.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Select Dilemma")
        
        # Load dilemmas
        dilemmas = get_sample_dilemmas()
        dilemma_options = {f"{d.title} ({d.category})": d for d in dilemmas}
        
        selected_dilemma_key = st.selectbox(
            "Choose an ethical dilemma:",
            list(dilemma_options.keys())
        )
        
        selected_dilemma = dilemma_options[selected_dilemma_key]
        
        st.markdown(f"**Category:** {selected_dilemma.category}")
        st.markdown(f"**Complexity:** {selected_dilemma.complexity_level}/5")
        st.markdown(f"**Description:** {selected_dilemma.description}")
        
        st.subheader("Select Framing")
        
        framing_type = st.selectbox(
            "Choose deictic framing:",
            [f.value for f in DeicticFraming]
        )
        
        # Role input for role-based framing
        role = None
        if framing_type == DeicticFraming.ROLE_BASED.value:
            role = st.text_input(
                "Specify role:",
                value="ethical decision-maker",
                help="Enter the role for role-based framing"
            )
    
    with col2:
        st.subheader("Generated Prompt")
        
        if st.button("Generate Prompt"):
            try:
                framing_enum = DeicticFraming(framing_type)
                prompt = st.session_state.prompt_engine.generate_prompt(
                    selected_dilemma, framing_enum, role
                )
                st.text_area("Prompt:", value=prompt, height=300)
                
                # Store prompt in session state for response generation
                st.session_state.current_prompt = prompt
                st.session_state.current_dilemma = selected_dilemma
                st.session_state.current_framing = framing_enum
                
            except Exception as e:
                st.error(f"Error generating prompt: {e}")
        
        st.subheader("Generate Response")
        
        if st.session_state.openai_client and hasattr(st.session_state, 'current_prompt'):
            if st.button("Get LLM Response"):
                try:
                    with st.spinner("Generating response..."):
                        response = st.session_state.openai_client.generate_response(
                            prompt=st.session_state.current_prompt,
                            dilemma_id=st.session_state.current_dilemma.id,
                            prompt_type=st.session_state.current_framing
                        )
                        
                        st.success("Response generated!")
                        st.text_area("LLM Response:", value=response.response_text, height=200)
                        
                        # Store response and annotate
                        st.session_state.db_manager.store_response(response)
                        
                        annotated = st.session_state.annotator.annotate_response(response)
                        st.session_state.db_manager.store_annotation(annotated)
                        
                        # Show annotation summary
                        st.subheader("Quick Analysis")
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.metric(
                                "Primary Ethical Stance", 
                                annotated.ethical_annotation.primary_stance.value
                            )
                            st.metric(
                                "Confidence Score", 
                                f"{annotated.ethical_annotation.confidence_score:.2f}"
                            )
                        
                        with col_b:
                            st.metric("Token Count", response.token_count)
                            st.metric("Processing Time", f"{response.processing_time:.2f}s")
                        
                except Exception as e:
                    st.error(f"Error generating response: {e}")
        else:
            if not st.session_state.openai_client:
                st.warning("OpenAI client not configured")
            else:
                st.info("Generate a prompt first")

def show_batch_experiments_page():
    """Display the batch experiments page."""
    st.header("📊 Batch Experiments")
    
    if not st.session_state.initialized:
        st.warning("Please initialize the system first.")
        return
    
    st.subheader("Create New Experiment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        experiment_name = st.text_input("Experiment Name")
        experiment_description = st.text_area("Description")
        
        # Select dilemmas
        dilemmas = get_sample_dilemmas()
        categories = get_dilemma_categories()
        
        selected_category = st.selectbox("Filter by Category", ["All"] + categories)
        
        if selected_category == "All":
            available_dilemmas = dilemmas
        else:
            available_dilemmas = [d for d in dilemmas if d.category == selected_category]
        
        selected_dilemmas = st.multiselect(
            "Select Dilemmas",
            [f"{d.title} ({d.id})" for d in available_dilemmas],
            default=[f"{d.title} ({d.id})" for d in available_dilemmas[:3]]
        )
    
    with col2:
        # Select framings
        selected_framings = st.multiselect(
            "Select Deictic Framings",
            [f.value for f in DeicticFraming],
            default=[f.value for f in DeicticFraming]
        )
        
        # Select models
        selected_models = st.multiselect(
            "Select Models",
            [m.value for m in LLMModel if m in [LLMModel.GPT4, LLMModel.GPT4_TURBO]],
            default=[LLMModel.GPT4_TURBO.value]
        )
        
        runs_per_combination = st.number_input(
            "Runs per Combination",
            min_value=1,
            max_value=5,
            value=1,
            help="Number of times to run each dilemma-framing-model combination"
        )
    
    if st.button("Start Experiment"):
        if not (experiment_name and selected_dilemmas and selected_framings and selected_models):
            st.error("Please fill in all required fields")
        elif not st.session_state.openai_client:
            st.error("OpenAI client not configured")
        else:
            # Create and run experiment
            try:
                # Extract dilemma IDs
                dilemma_ids = [d.split("(")[-1].strip(")") for d in selected_dilemmas]
                
                # Create experiment
                from models.schemas import BatchExperiment
                import uuid
                
                experiment = BatchExperiment(
                    id=str(uuid.uuid4()),
                    name=experiment_name,
                    description=experiment_description,
                    dilemma_ids=dilemma_ids,
                    framing_types=[DeicticFraming(f) for f in selected_framings],
                    models=[LLMModel(m) for m in selected_models],
                    runs_per_combination=runs_per_combination
                )
                
                # Store experiment
                st.session_state.db_manager.store_experiment(experiment)
                
                # Run experiment
                run_batch_experiment(experiment)
                
            except Exception as e:
                st.error(f"Error running experiment: {e}")
    
    # Show existing experiments
    st.subheader("Recent Experiments")
    # This would show a list of recent experiments from the database
    # For now, show placeholder
    st.info("Experiment history will be displayed here")

def show_research_mode_page():
    """Display the research mode page with research prompts and coding."""
    st.header("🔬 Research Mode")
    
    if not st.session_state.initialized:
        st.warning("Please initialize the system first.")
        return
    
    st.markdown("""
    **Research Mode** uses the validated research prompts and implements the extended coding scheme 
    with shamanic markers for systematic analysis of LLM responses to ethical dilemmas.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Research Dilemmas")
        
        # Load research dilemmas
        research_dilemmas = get_research_dilemmas()
        dilemma_options = {f"{d.title}": d for d in research_dilemmas}
        
        selected_dilemma_key = st.selectbox(
            "Choose a research dilemma:",
            list(dilemma_options.keys())
        )
        
        selected_dilemma = dilemma_options[selected_dilemma_key]
        
        st.markdown(f"**Category:** {selected_dilemma.category}")
        st.markdown(f"**Complexity:** {selected_dilemma.complexity_level}/5")
        st.markdown(f"**Source:** {selected_dilemma.source}")
        
        st.subheader("Deictic Framing")
        
        framing_type = st.selectbox(
            "Choose deictic framing:",
            [f.value for f in DeicticFraming]
        )
        
        st.subheader("Model Selection")
        
        # Model selection with both OpenAI and OpenRouter options
        available_models = []
        if st.session_state.openai_client:
            available_models.extend([LLMModel.GPT4.value, LLMModel.GPT4_TURBO.value])
        if st.session_state.openrouter_client:
            available_models.extend([
                LLMModel.CLAUDE_3_OPUS.value, 
                LLMModel.CLAUDE_3_SONNET.value,
                LLMModel.DEEPSEEK_R1.value
            ])
        
        if not available_models:
            st.warning("No LLM clients configured. Please add API keys in Configuration.")
            return
        
        selected_model = st.selectbox(
            "Choose model:",
            available_models
        )
    
    with col2:
        st.subheader("Research Prompt")
        
        if st.button("Generate Research Prompt"):
            try:
                framing_enum = DeicticFraming(framing_type)
                
                # Use research prompts (prioritized)
                prompt = st.session_state.prompt_engine.generate_prompt(
                    selected_dilemma, framing_enum, use_research_prompts=True
                )
                st.text_area("Research Prompt:", value=prompt, height=200)
                
                # Log prompt generation
                prompt_id = research_logger.log_prompt_generation(
                    dilemma_title=selected_dilemma.title,
                    framing=framing_enum,
                    prompt=prompt,
                    source="research"
                )
                
                # Store for response generation
                st.session_state.current_research_prompt = prompt
                st.session_state.current_research_dilemma = selected_dilemma
                st.session_state.current_research_framing = framing_enum
                st.session_state.current_research_model = LLMModel(selected_model)
                st.session_state.current_prompt_id = prompt_id
                
                st.success(f"✅ Prompt logged: {prompt_id}")
                
            except Exception as e:
                st.error(f"Error generating research prompt: {e}")
        
        st.subheader("Generate & Analyze Response")
        
        if hasattr(st.session_state, 'current_research_prompt'):
            if st.button("Get LLM Response & Research Coding"):
                try:
                    with st.spinner("Generating response and applying research coding..."):
                        # Select appropriate client
                        model_enum = st.session_state.current_research_model
                        
                        if model_enum in [LLMModel.GPT4, LLMModel.GPT4_TURBO]:
                            if not st.session_state.openai_client:
                                st.error("OpenAI client not available")
                                return
                            client = st.session_state.openai_client
                        else:
                            if not st.session_state.openrouter_client:
                                st.error("OpenRouter client not available")
                                return
                            client = st.session_state.openrouter_client
                        
                        # Generate response
                        response = client.generate_response(
                            prompt=st.session_state.current_research_prompt,
                            dilemma_id=st.session_state.current_research_dilemma.id,
                            prompt_type=st.session_state.current_research_framing,
                            model=model_enum
                        )
                        
                        # Log response generation
                        response_id = research_logger.log_response_generation(
                            response=response,
                            prompt_id=getattr(st.session_state, 'current_prompt_id', None)
                        )
                        
                        st.success("✅ Response generated and logged!")
                        st.text_area("LLM Response:", value=response.response_text, height=150)
                        
                        # Apply research coding
                        research_coding = st.session_state.research_coder.code_response(response)
                        
                        # Create detailed analysis for logging
                        detailed_analysis = {
                            "response_length": len(response.response_text),
                            "word_count": len(response.response_text.split()),
                            "sentence_count": len([s for s in response.response_text.split('.') if s.strip()]),
                            "model_used": response.model.value,
                            "framing_used": response.prompt_type.value,
                            "processing_metrics": {
                                "token_count": response.token_count,
                                "processing_time": response.processing_time,
                                "temperature": response.temperature
                            }
                        }
                        
                        # Log research coding
                        coding_id = research_logger.log_research_coding(
                            response_id=response.id,
                            coding=research_coding,
                            detailed_analysis=detailed_analysis
                        )
                        
                        # Store response and coding
                        st.session_state.db_manager.store_response(response)
                        
                        # Display research coding results
                        st.subheader("Research Coding Results")
                        
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Pronoun Usage", research_coding.pronoun_usage)
                            st.metric("Role Assumption", research_coding.role_assumption)
                            st.metric("Perspective Complexity", research_coding.perspective_complexity)
                            st.metric("Distributed Agency", research_coding.distributed_agency)
                        
                        with col_b:
                            st.metric("Ethical Mode", research_coding.ethical_mode)
                            st.metric("Stance Clarity", research_coding.stance_clarity)
                            st.metric("Moral Plurality", research_coding.moral_plurality)
                            st.metric("Deictic Reframing", research_coding.deictic_reframing)
                        
                        with col_c:
                            st.metric("Ontological Perspective", research_coding.ontological_perspective)
                            st.metric("Shamanic Markers", research_coding.shamanic_cosmological_markers)
                            st.metric("Reasoning Steps", research_coding.reasoning_steps_count)
                            st.metric("Dialogic Simulation", research_coding.dialogic_simulation)
                        
                        # Show prompting technique
                        st.markdown(f"**Prompting Technique:** {research_coding.prompting_technique}")
                        
                        # Export coding data
                        coding_dict = st.session_state.research_coder.export_coding_to_dict(research_coding)
                        
                        # Show logging information
                        st.info(f"📝 Research data logged: Response ID {response_id}, Coding ID {coding_id}")
                        
                        # Export options
                        col_export1, col_export2, col_export3 = st.columns(3)
                        
                        with col_export1:
                            if st.button("Export Coding JSON"):
                                import json
                                coding_json = json.dumps(coding_dict, indent=2)
                                st.download_button(
                                    label="Download Coding as JSON",
                                    data=coding_json,
                                    file_name=f"research_coding_{response.id}.json",
                                    mime="application/json"
                                )
                        
                        with col_export2:
                            if st.button("Export Session Summary"):
                                summary_file = research_logger.export_session_summary()
                                st.success(f"Session summary exported: {summary_file}")
                        
                        with col_export3:
                            if st.button("Export Research CSV"):
                                csv_file = research_logger.export_research_data_csv()
                                if csv_file:
                                    st.success(f"Research data exported: {csv_file}")
                                else:
                                    st.warning("No data available for CSV export")
                        
                except Exception as e:
                    st.error(f"Error in research analysis: {e}")
        else:
            st.info("Generate a research prompt first")
    
    # Research coding scheme reference
    with st.expander("📋 Research Coding Scheme Reference"):
        st.markdown("""
        ### Extended LLM Coding Scheme with Shamanic Markers
        
        **Core Variables:**
        - **Pronoun Usage**: 0=None, 1=Low, 2=Moderate, 3=High
        - **Role Assumption**: 0=None, 1=Implied, 2=Explicit role, 3=Invented role
    
    # Research logging section
    st.subheader("📊 Research Session Logging")
    
    # Show current session info
    session_summary = research_logger.get_session_summary()
    
    col_log1, col_log2, col_log3 = st.columns(3)
    
    with col_log1:
        st.metric("Session ID", session_summary["session_id"])
        st.metric("Activities", session_summary["activities"])
    
    with col_log2:
        stats = session_summary["statistics"]
        st.metric("Prompts Generated", stats["prompts_generated"])
        st.metric("Responses Generated", stats["responses_generated"])
    
    with col_log3:
        st.metric("Codings Completed", stats["codings_completed"])
        st.metric("Models Used", len(stats["models_used"]))
    
    # Session management
    col_session1, col_session2 = st.columns(2)
    
    with col_session1:
        if st.button("📋 View Session Log"):
            st.json(session_summary)
    
    with col_session2:
        if st.button("💾 Close Session & Export"):
            summary_file = research_logger.close_session()
            st.success(f"Session closed and exported: {summary_file}")

        - **Perspective Complexity**: 0=Single POV, 1=Acknowledged others, 2=Perspective shift
        - **Ethical Mode**: D=Deontological, C=Consequentialist, R=Relational/Care, V=Virtue, S=Shamanic, M=Mixed
        - **Distributed Agency**: 0=None, 1=Implied, 2=Explicit
        - **Deictic Reframing**: 0=None, 1=Partial reframe, 2=Full reframe
        - **Stance Clarity**: 0=Unclear, 1=Partial, 2=Clear
        - **Moral Plurality**: 0=Singular frame, 1=Minimal plurality, 2=Multiple frames
        - **Ontological Perspective**: 0=None, 1=Implied being, 2=Explicit ontological frame
        - **Shamanic/Cosmological Markers**: 0=None, 1=Metaphor only, 2=Embodied cosmology
        
        **Extended Variables:**
        - **Prompting Technique**: CoT, J, R, S, D, F, M
        - **Reasoning Steps Count**: 0-5+
        - **Dialogic Simulation**: 0=None, 1=Monologic, 2=Simulated dialog, 3=Multi-perspectival
        """)


def run_batch_experiment(experiment):
    """Run a batch experiment."""
    st.info(f"Starting experiment: {experiment.name}")
    
    # Get dilemmas
    all_dilemmas = get_sample_dilemmas()
    selected_dilemmas = [d for d in all_dilemmas if d.id in experiment.dilemma_ids]
    
    # Create progress tracking
    total_combinations = (
        len(selected_dilemmas) * 
        len(experiment.framing_types) * 
        len(experiment.models) * 
        experiment.runs_per_combination
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    completed = 0
    
    for dilemma in selected_dilemmas:
        for framing in experiment.framing_types:
            for model in experiment.models:
                for run in range(experiment.runs_per_combination):
                    try:
                        # Update progress
                        progress = completed / total_combinations
                        progress_bar.progress(progress)
                        status_text.text(
                            f"Processing: {dilemma.title} | {framing.value} | {model.value} | Run {run+1}"
                        )
                        
                        # Generate prompt
                        prompt = st.session_state.prompt_engine.generate_prompt(dilemma, framing)
                        
                        # Generate response
                        response = st.session_state.openai_client.generate_response(
                            prompt=prompt,
                            dilemma_id=dilemma.id,
                            prompt_type=framing,
                            model=model
                        )
                        
                        # Store response
                        st.session_state.db_manager.store_response(response)
                        
                        # Annotate response
                        annotated = st.session_state.annotator.annotate_response(response)
                        st.session_state.db_manager.store_annotation(annotated)
                        
                        completed += 1
                        
                        # Small delay to respect rate limits
                        time.sleep(1)
                        
                    except Exception as e:
                        st.error(f"Error in experiment: {e}")
                        completed += 1
                        continue
    
    progress_bar.progress(1.0)
    status_text.text("Experiment completed!")
    st.success(f"Experiment '{experiment.name}' completed successfully!")

def show_analysis_page():
    """Display the analysis and visualization page."""
    st.header("📈 Analysis & Visualization")
    
    if not st.session_state.initialized:
        st.warning("Please initialize the system first.")
        return
    
    # Get data from database
    stats = st.session_state.db_manager.get_experiment_stats()
    
    if stats.get('total_responses', 0) == 0:
        st.info("No data available. Run some experiments first!")
        return
    
    st.subheader("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Responses", stats.get('total_responses', 0))
    with col2:
        st.metric("Annotations", stats.get('total_annotations', 0))
    with col3:
        st.metric("Dilemmas Tested", stats.get('unique_dilemmas', 0))
    with col4:
        st.metric("Models Used", stats.get('unique_models', 0))
    
    # Placeholder for visualizations
    st.subheader("Response Analysis")
    st.info("Detailed visualizations will be implemented here, including:")
    st.markdown("""
    - Ethical stance distribution by framing type
    - Pronoun usage patterns across models
    - Deictic effectiveness heatmaps
    - Response clustering analysis
    - Temporal analysis of model behavior
    """)

def show_data_management_page():
    """Display the data management page."""
    st.header("💾 Data Management")
    
    if not st.session_state.initialized:
        st.warning("Please initialize the system first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Database Statistics")
        
        if st.button("Refresh Stats"):
            stats = st.session_state.db_manager.get_experiment_stats()
            st.json(stats)
    
    with col2:
        st.subheader("Data Export")
        
        export_format = st.selectbox(
            "Export Format",
            ["JSONL", "CSV", "Excel"]
        )
        
        include_annotations = st.checkbox("Include Annotations", value=True)
        
        if st.button("Export Data"):
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"deixis_export_{timestamp}.jsonl"
                
                success = st.session_state.db_manager.export_to_jsonl(
                    f"exports/{filename}",
                    include_annotations=include_annotations
                )
                
                if success:
                    st.success(f"Data exported to exports/{filename}")
                else:
                    st.error("Export failed")
                    
            except Exception as e:
                st.error(f"Export error: {e}")

if __name__ == "__main__":
    main()