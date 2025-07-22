"""
Comprehensive Streamlit Research Interface for Deictic Ethics Research
Integrates the concurrent research runner and statistical analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import asyncio
import threading

# Import research modules
from data.research_prompts import load_research_prompts, get_research_statistics
from analysis.research_statistics import ResearchStatistics
from concurrent_research_runner import ConcurrentResearchRunner
from models.schemas import LLMModel, DeicticFraming

# Page configuration
st.set_page_config(
    page_title="🧠 Deixis AI Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application interface."""
    st.title("🧠 Deixis AI Agent Research System")
    st.markdown("**AI agent for analyzing language model responses to ethical dilemmas through diverse deictic configurations**")
    
    # Sidebar navigation
    st.sidebar.title("🔬 Research Navigation")
    page = st.sidebar.selectbox(
        "Choose Research Module",
        [
            "📊 Research Overview",
            "🚀 Run Concurrent Experiment", 
            "📈 Statistical Analysis",
            "📋 Research Design",
            "🔍 Data Explorer",
            "📊 Visualizations"
        ]
    )
    
    if page == "📊 Research Overview":
        show_research_overview()
    elif page == "🚀 Run Concurrent Experiment":
        show_concurrent_experiment()
    elif page == "📈 Statistical Analysis":
        show_statistical_analysis()
    elif page == "📋 Research Design":
        show_research_design()
    elif page == "🔍 Data Explorer":
        show_data_explorer()
    elif page == "📊 Visualizations":
        show_visualizations()

def show_research_overview():
    """Show comprehensive research overview."""
    st.header("📊 Research System Overview")
    
    # Load research data
    try:
        prompts = load_research_prompts()
        stats = get_research_statistics()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Research Prompts", stats['total_prompts'])
        with col2:
            st.metric("Ethical Dilemmas", stats['total_dilemmas'])
        with col3:
            st.metric("Deictic Framings", len(stats['framing_distribution']))
        with col4:
            st.metric("Prompts per Dilemma", stats['prompts_per_dilemma'])
        
        # Research hypothesis
        st.subheader("🧪 Research Hypothesis")
        st.info("""
        **Primary Hypothesis**: Large Language Models (LLMs) respond differently to ethical dilemmas 
        depending on the deictic framing and prompting technique used. Specifically, prompts that invoke 
        relational, cosmological, or shamanic deixis will lead to more distributed, plural, and ethically 
        reflective responses than those that rely on anchored or neutral frames.
        """)
        
        # Framing distribution
        st.subheader("🎯 Deictic Framing Distribution")
        framing_df = pd.DataFrame(list(stats['framing_distribution'].items()), 
                                columns=['Framing', 'Count'])
        
        fig = px.bar(framing_df, x='Framing', y='Count', 
                    title="Distribution of Prompts by Deictic Framing")
        st.plotly_chart(fig, use_container_width=True)
        
        # Research variables
        st.subheader("📋 Research Variables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔧 Independent Variables (Manipulated)**")
            st.markdown("""
            - **Deictic Framing** (5 levels): Anchored CoT, Role-Based, Cosmological, Shamanic, Neutral
            - **LLM Model** (3+ levels): GPT-4, Claude 3 Sonnet, DeepSeek R1
            - **Ethical Dilemma** (49 levels): Professional, medical, personal, AI ethics
            - **Prompting Technique** (7 levels): CoT, Justification, Reflective, etc.
            """)
        
        with col2:
            st.markdown("**📊 Dependent Variables (Measured)**")
            st.markdown("""
            - **Pronoun Usage** (0-3): Degree of anchoring and relational stance
            - **Role Assumption** (0-3): How models position themselves ethically
            - **Perspective Complexity** (0-2): Viewpoint multiplicity
            - **Ethical Mode** (D/C/R/V/S/M): Dominant moral logic
            - **Distributed Agency** (0-2): Responsibility sharing vs. centralization
            - **Moral Plurality** (0-2): Multiple ethical perspective acknowledgment
            - **Shamanic/Cosmological Markers** (0-2): Non-modern reasoning evidence
            - **And 6 more variables...**
            """)
        
        # Check for existing data
        st.subheader("📁 Existing Research Data")
        research_logs = Path("research_logs")
        if research_logs.exists():
            csv_files = list(research_logs.glob("research_data_*.csv"))
            json_files = list(research_logs.glob("statistical_analysis_*.json"))
            
            if csv_files or json_files:
                st.success(f"Found {len(csv_files)} data files and {len(json_files)} analysis files")
                
                if csv_files:
                    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
                    st.info(f"Latest data: {latest_csv.name}")
                
                if json_files:
                    latest_analysis = max(json_files, key=lambda x: x.stat().st_mtime)
                    st.info(f"Latest analysis: {latest_analysis.name}")
            else:
                st.warning("No research data found. Run the concurrent experiment to generate data.")
        else:
            st.warning("No research_logs directory found. Run the concurrent experiment first.")
            
    except Exception as e:
        st.error(f"Error loading research data: {e}")

def show_concurrent_experiment():
    """Interface for running concurrent research experiment."""
    st.header("🚀 Concurrent Research Experiment")
    
    st.markdown("""
    This module runs all 245 research prompts across multiple LLM models concurrently 
    with stateless API calls to ensure research integrity.
    """)
    
    # Configuration
    st.subheader("⚙️ Experiment Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_concurrent = st.slider("Max Concurrent Requests", 1, 10, 5)
        delay_between_batches = st.slider("Delay Between Batches (seconds)", 0.5, 5.0, 1.0)
    
    with col2:
        models = st.multiselect(
            "Select Models to Test",
            ["GPT-4", "Claude 3 Sonnet", "DeepSeek R1"],
            default=["GPT-4"]
        )
        
        run_analysis = st.checkbox("Run Statistical Analysis After Experiment", value=True)
    
    # API Key Status
    st.subheader("🔑 API Key Status")
    
    try:
        from config import Config
        config = Config()
        
        if config.OPENROUTER_API_KEY:
            st.success("✅ OpenRouter API Key configured")
            st.info("🔄 All models (GPT-4, Claude 3 Sonnet, DeepSeek R1) will be accessed via OpenRouter")
        else:
            st.error("❌ OpenRouter API Key missing")
            st.error("Please add OPENROUTER_API_KEY to your .env file")
    except Exception as e:
        st.error(f"❌ Configuration error - check .env file: {e}")
    
    # Run experiment
    if st.button("🚀 Start Concurrent Experiment", type="primary"):
        if not models:
            st.error("Please select at least one model to test")
            return
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize runner
            status_text.text("Initializing concurrent research runner...")
            
            # Map model names to enum values
            model_map = {
                "GPT-4": LLMModel.GPT4,
                "Claude 3 Sonnet": LLMModel.CLAUDE_3_SONNET,
                "DeepSeek R1": LLMModel.DEEPSEEK_R1
            }
            selected_models = [model_map[m] for m in models]
            
            runner = ConcurrentResearchRunner(
                models=selected_models,
                max_concurrent=max_concurrent
            )
            
            status_text.text("Running concurrent experiment...")
            progress_bar.progress(0.1)
            
            # Run experiment (this would need to be adapted for Streamlit)
            st.info("🔄 Experiment running... This may take 15-30 minutes depending on configuration.")
            st.info("💡 For now, please run: `python concurrent_research_runner.py` in terminal")
            
            # TODO: Implement async execution in Streamlit
            # results = runner.run_concurrent_experiment(delay_between_batches)
            
        except Exception as e:
            st.error(f"Error running experiment: {e}")

def show_statistical_analysis():
    """Show statistical analysis interface."""
    st.header("📈 Statistical Analysis")
    
    # Load latest data
    research_logs = Path("research_logs")
    if not research_logs.exists():
        st.warning("No research data found. Run the concurrent experiment first.")
        return
    
    # Find data files
    csv_files = list(research_logs.glob("research_data_*.csv"))
    analysis_files = list(research_logs.glob("statistical_analysis_*.json"))
    
    if not csv_files:
        st.warning("No CSV data files found. Run the concurrent experiment first.")
        return
    
    # Select data file
    selected_file = st.selectbox(
        "Select Data File",
        [f.name for f in csv_files],
        index=len(csv_files)-1  # Default to latest
    )
    
    if st.button("🔬 Run Statistical Analysis"):
        try:
            # Load data
            data_path = research_logs / selected_file
            analyzer = ResearchStatistics()
            data = analyzer.load_research_data(str(data_path))
            
            if data is not None:
                st.success(f"Loaded {len(data)} responses for analysis")
                
                # Generate analysis
                with st.spinner("Running statistical tests..."):
                    report_path = research_logs / f"statistical_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    analyzer.generate_research_report(str(report_path))
                
                st.success(f"Analysis complete! Report saved: {report_path.name}")
                
                # Show key results
                with open(report_path, 'r') as f:
                    report = json.load(f)
                
                show_analysis_results(report)
            
        except Exception as e:
            st.error(f"Error in statistical analysis: {e}")
    
    # Show existing analysis files
    if analysis_files:
        st.subheader("📊 Existing Analysis Reports")
        
        selected_analysis = st.selectbox(
            "Select Analysis Report",
            [f.name for f in analysis_files],
            index=len(analysis_files)-1
        )
        
        if st.button("📖 Load Analysis Report"):
            try:
                with open(research_logs / selected_analysis, 'r') as f:
                    report = json.load(f)
                show_analysis_results(report)
            except Exception as e:
                st.error(f"Error loading analysis: {e}")

def show_analysis_results(report):
    """Display statistical analysis results."""
    st.subheader("🔬 Statistical Analysis Results")
    
    # Sample characteristics
    sample = report['sample_characteristics']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sample Size", sample['sample_size'])
    with col2:
        st.metric("Models Tested", len(sample['models']))
    with col3:
        st.metric("Framings Used", len(sample['framings']))
    
    # Significant effects
    st.subheader("🎯 Significant Deictic Framing Effects")
    
    framing_effects = report['deictic_framing_effects']
    significant_vars = []
    
    for var, result in framing_effects.items():
        if isinstance(result, dict) and result.get('significant', False):
            significant_vars.append({
                'Variable': var,
                'p-value': f"{result['p_value']:.4f}",
                'Effect Size (η²)': f"{result['effect_size']:.3f}"
            })
    
    if significant_vars:
        st.dataframe(pd.DataFrame(significant_vars))
    else:
        st.info("No significant deictic framing effects found")
    
    # Shamanic hypothesis
    st.subheader("🌟 Shamanic Framing Hypothesis Test")
    
    shamanic_results = report['shamanic_hypothesis_test']
    shamanic_df = []
    
    for var, result in shamanic_results.items():
        if isinstance(result, dict) and 'significant' in result:
            shamanic_df.append({
                'Variable': var,
                'Shamanic Mean': f"{result['shamanic_mean']:.3f}",
                'Other Mean': f"{result['other_mean']:.3f}",
                'p-value': f"{result['p_value']:.4f}",
                'Supported': "✅ Yes" if result['significant'] else "❌ No"
            })
    
    if shamanic_df:
        st.dataframe(pd.DataFrame(shamanic_df))

def show_research_design():
    """Show research design documentation."""
    st.header("📋 Research Design")
    
    # Load and display research design
    try:
        with open("RESEARCH_DESIGN.md", "r") as f:
            content = f.read()
        st.markdown(content)
    except FileNotFoundError:
        st.error("RESEARCH_DESIGN.md not found")

def show_data_explorer():
    """Data exploration interface."""
    st.header("🔍 Data Explorer")
    
    # Load data
    research_logs = Path("research_logs")
    if not research_logs.exists():
        st.warning("No research data found.")
        return
    
    csv_files = list(research_logs.glob("research_data_*.csv"))
    if not csv_files:
        st.warning("No CSV data files found.")
        return
    
    # Select file
    selected_file = st.selectbox(
        "Select Data File",
        [f.name for f in csv_files],
        index=len(csv_files)-1
    )
    
    try:
        data = pd.read_csv(research_logs / selected_file)
        
        st.subheader("📊 Data Overview")
        st.dataframe(data.head())
        
        st.subheader("📈 Data Summary")
        st.write(data.describe())
        
        # Filter options
        st.subheader("🔍 Filter Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'model' in data.columns:
                selected_models = st.multiselect("Models", data['model'].unique())
                if selected_models:
                    data = data[data['model'].isin(selected_models)]
        
        with col2:
            if 'framing' in data.columns:
                selected_framings = st.multiselect("Framings", data['framing'].unique())
                if selected_framings:
                    data = data[data['framing'].isin(selected_framings)]
        
        st.subheader("📊 Filtered Data")
        st.dataframe(data)
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_visualizations():
    """Show research visualizations."""
    st.header("📊 Research Visualizations")
    
    # Load data
    research_logs = Path("research_logs")
    if not research_logs.exists():
        st.warning("No research data found.")
        return
    
    csv_files = list(research_logs.glob("research_data_*.csv"))
    if not csv_files:
        st.warning("No CSV data files found.")
        return
    
    try:
        # Load latest data
        latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
        data = pd.read_csv(latest_file)
        
        st.info(f"Visualizing data from: {latest_file.name}")
        
        # Ethical mode distribution
        if 'ethical_mode' in data.columns and 'framing' in data.columns:
            st.subheader("🎯 Ethical Mode Distribution by Framing")
            
            ethical_counts = data.groupby(['framing', 'ethical_mode']).size().reset_index(name='count')
            fig = px.bar(ethical_counts, x='framing', y='count', color='ethical_mode',
                        title="Ethical Mode Distribution by Deictic Framing")
            st.plotly_chart(fig, use_container_width=True)
        
        # Variable distributions
        st.subheader("📈 Variable Distributions")
        
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            selected_var = st.selectbox("Select Variable", numeric_cols)
            
            if 'framing' in data.columns:
                fig = px.box(data, x='framing', y=selected_var,
                           title=f"{selected_var} Distribution by Framing")
                st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        if len(numeric_cols) > 1:
            st.subheader("🔥 Variable Correlation Heatmap")
            
            corr_matrix = data[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                          title="Variable Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    main()
