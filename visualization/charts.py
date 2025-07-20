"""
Visualization suite for the Deixis AI Agent system.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from models.schemas import AnnotatedResponse, DeicticFraming, EthicalStance

logger = logging.getLogger(__name__)

class VisualizationSuite:
    """
    Comprehensive visualization suite for analyzing deictic framing effects.
    """
    
    def __init__(self):
        self.color_schemes = self._initialize_color_schemes()
        logger.info("VisualizationSuite initialized")
    
    def _initialize_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Initialize color schemes for different visualization types."""
        return {
            "deictic_framings": {
                "anchored_cot": "#1f77b4",
                "role_based": "#ff7f0e", 
                "cosmological": "#2ca02c",
                "neutral": "#d62728",
                "shamanic": "#9467bd"
            },
            "ethical_stances": {
                "deontological": "#e377c2",
                "consequentialist": "#7f7f7f",
                "virtue": "#bcbd22",
                "relational": "#17becf",
                "shamanic": "#9467bd",
                "mixed": "#8c564b",
                "unclear": "#ff9896"
            },
            "models": {
                "gpt-4": "#1f77b4",
                "gpt-4-turbo": "#ff7f0e",
                "claude-3-opus": "#2ca02c",
                "claude-3-sonnet": "#d62728",
                "deepseek-r1": "#9467bd"
            }
        }
    
    def create_stance_distribution_chart(self, 
                                       annotated_responses: List[AnnotatedResponse],
                                       group_by: str = "framing") -> go.Figure:
        """
        Create a chart showing ethical stance distribution.
        
        Args:
            annotated_responses: List of annotated responses
            group_by: Group by 'framing', 'model', or 'dilemma'
            
        Returns:
            Plotly figure
        """
        # Prepare data
        data = []
        for response in annotated_responses:
            data.append({
                'framing': response.response.prompt_type.value,
                'model': response.response.model.value,
                'dilemma': response.response.dilemma_id,
                'stance': response.ethical_annotation.primary_stance.value,
                'confidence': response.ethical_annotation.confidence_score
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            return self._create_empty_chart("No data available")
        
        # Create chart based on grouping
        if group_by == "framing":
            fig = px.histogram(
                df, 
                x='framing', 
                color='stance',
                title="Ethical Stance Distribution by Deictic Framing",
                color_discrete_map=self.color_schemes["ethical_stances"]
            )
        elif group_by == "model":
            fig = px.histogram(
                df, 
                x='model', 
                color='stance',
                title="Ethical Stance Distribution by Model",
                color_discrete_map=self.color_schemes["ethical_stances"]
            )
        else:  # dilemma
            fig = px.histogram(
                df, 
                x='dilemma', 
                color='stance',
                title="Ethical Stance Distribution by Dilemma",
                color_discrete_map=self.color_schemes["ethical_stances"]
            )
            fig.update_xaxes(tickangle=45)
        
        fig.update_layout(
            xaxis_title=group_by.title(),
            yaxis_title="Count",
            legend_title="Ethical Stance"
        )
        
        return fig
    
    def create_framing_effectiveness_heatmap(self, 
                                           annotated_responses: List[AnnotatedResponse]) -> go.Figure:
        """
        Create a heatmap showing framing effectiveness across models and dilemmas.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Plotly figure
        """
        # Prepare data
        data = []
        for response in annotated_responses:
            data.append({
                'framing': response.response.prompt_type.value,
                'model': response.response.model.value,
                'dilemma': response.response.dilemma_id,
                'confidence': response.ethical_annotation.confidence_score
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            return self._create_empty_chart("No data available")
        
        # Calculate average confidence by framing and model
        heatmap_data = df.groupby(['framing', 'model'])['confidence'].mean().reset_index()
        pivot_data = heatmap_data.pivot(index='framing', columns='model', values='confidence')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            text=np.round(pivot_data.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            colorbar=dict(title="Average Confidence Score")
        ))
        
        fig.update_layout(
            title="Framing Effectiveness Heatmap (Average Confidence Scores)",
            xaxis_title="Model",
            yaxis_title="Deictic Framing"
        )
        
        return fig
    
    def create_pronoun_usage_chart(self, 
                                 annotated_responses: List[AnnotatedResponse]) -> go.Figure:
        """
        Create a chart showing pronoun usage patterns.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Plotly figure
        """
        # Extract pronoun data
        pronoun_data = []
        for response in annotated_responses:
            framing = response.response.prompt_type.value
            for pronoun in response.linguistic_annotation.pronoun_use:
                if ':' in pronoun:
                    category, word = pronoun.split(':', 1)
                    pronoun_data.append({
                        'framing': framing,
                        'category': category,
                        'word': word,
                        'count': 1
                    })
        
        if not pronoun_data:
            return self._create_empty_chart("No pronoun data available")
        
        df = pd.DataFrame(pronoun_data)
        
        # Aggregate by framing and category
        agg_data = df.groupby(['framing', 'category'])['count'].sum().reset_index()
        
        fig = px.bar(
            agg_data,
            x='framing',
            y='count',
            color='category',
            title="Pronoun Usage Patterns by Deictic Framing",
            labels={'count': 'Frequency', 'framing': 'Deictic Framing'}
        )
        
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def create_response_clustering_plot(self, 
                                      annotated_responses: List[AnnotatedResponse]) -> go.Figure:
        """
        Create a UMAP clustering plot of responses.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Plotly figure
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from umap import UMAP
            
            if len(annotated_responses) < 3:
                return self._create_empty_chart("Need at least 3 responses for clustering")
            
            # Extract text and metadata
            texts = [r.response.response_text for r in annotated_responses]
            framings = [r.response.prompt_type.value for r in annotated_responses]
            stances = [r.ethical_annotation.primary_stance.value for r in annotated_responses]
            
            # Vectorize texts
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            text_vectors = vectorizer.fit_transform(texts)
            
            # Apply UMAP
            umap_model = UMAP(n_components=2, random_state=42)
            embeddings = umap_model.fit_transform(text_vectors.toarray())
            
            # Create scatter plot
            fig = go.Figure()
            
            for framing in set(framings):
                mask = [f == framing for f in framings]
                fig.add_trace(go.Scatter(
                    x=embeddings[mask, 0],
                    y=embeddings[mask, 1],
                    mode='markers',
                    name=framing,
                    marker=dict(
                        color=self.color_schemes["deictic_framings"].get(framing, "#000000"),
                        size=8
                    ),
                    text=[stances[i] for i, m in enumerate(mask) if m],
                    hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>"
                ))
            
            fig.update_layout(
                title="Response Clustering (UMAP Projection)",
                xaxis_title="UMAP Dimension 1",
                yaxis_title="UMAP Dimension 2",
                legend_title="Deictic Framing"
            )
            
            return fig
            
        except ImportError:
            return self._create_empty_chart("UMAP clustering requires scikit-learn and umap-learn")
        except Exception as e:
            logger.error(f"Error creating clustering plot: {e}")
            return self._create_empty_chart(f"Error: {e}")
    
    def create_temporal_analysis_chart(self, 
                                     annotated_responses: List[AnnotatedResponse]) -> go.Figure:
        """
        Create a temporal analysis chart showing changes over time.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Plotly figure
        """
        # Prepare temporal data
        data = []
        for response in annotated_responses:
            data.append({
                'timestamp': response.response.timestamp,
                'framing': response.response.prompt_type.value,
                'stance': response.ethical_annotation.primary_stance.value,
                'confidence': response.ethical_annotation.confidence_score,
                'processing_time': response.response.processing_time
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            return self._create_empty_chart("No temporal data available")
        
        # Sort by timestamp
        df = df.sort_values('timestamp')
        
        # Create subplot with multiple metrics
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Confidence Scores Over Time', 'Processing Time Over Time'),
            vertical_spacing=0.1
        )
        
        # Add confidence score traces
        for framing in df['framing'].unique():
            framing_data = df[df['framing'] == framing]
            fig.add_trace(
                go.Scatter(
                    x=framing_data['timestamp'],
                    y=framing_data['confidence'],
                    mode='lines+markers',
                    name=f"{framing} (confidence)",
                    line=dict(color=self.color_schemes["deictic_framings"].get(framing, "#000000"))
                ),
                row=1, col=1
            )
        
        # Add processing time traces
        for framing in df['framing'].unique():
            framing_data = df[df['framing'] == framing]
            fig.add_trace(
                go.Scatter(
                    x=framing_data['timestamp'],
                    y=framing_data['processing_time'],
                    mode='lines+markers',
                    name=f"{framing} (time)",
                    line=dict(color=self.color_schemes["deictic_framings"].get(framing, "#000000"), dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title="Temporal Analysis of Response Patterns",
            height=600
        )
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Confidence Score", row=1, col=1)
        fig.update_yaxes(title_text="Processing Time (s)", row=2, col=1)
        
        return fig
    
    def create_comparative_analysis_dashboard(self, 
                                            annotated_responses: List[AnnotatedResponse]) -> Dict[str, go.Figure]:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Dictionary of figure names to Plotly figures
        """
        dashboard = {}
        
        try:
            dashboard["stance_distribution"] = self.create_stance_distribution_chart(
                annotated_responses, "framing"
            )
            dashboard["effectiveness_heatmap"] = self.create_framing_effectiveness_heatmap(
                annotated_responses
            )
            dashboard["pronoun_usage"] = self.create_pronoun_usage_chart(
                annotated_responses
            )
            dashboard["temporal_analysis"] = self.create_temporal_analysis_chart(
                annotated_responses
            )
            dashboard["clustering"] = self.create_response_clustering_plot(
                annotated_responses
            )
            
            logger.info("Created comprehensive analysis dashboard")
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            dashboard["error"] = self._create_empty_chart(f"Dashboard error: {e}")
        
        return dashboard
    
    def create_model_comparison_chart(self, 
                                    annotated_responses: List[AnnotatedResponse]) -> go.Figure:
        """
        Create a chart comparing model performance across different metrics.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Plotly figure
        """
        # Prepare comparison data
        data = []
        for response in annotated_responses:
            data.append({
                'model': response.response.model.value,
                'framing': response.response.prompt_type.value,
                'confidence': response.ethical_annotation.confidence_score,
                'processing_time': response.response.processing_time,
                'token_count': response.response.token_count
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            return self._create_empty_chart("No model comparison data available")
        
        # Calculate metrics by model
        model_metrics = df.groupby('model').agg({
            'confidence': 'mean',
            'processing_time': 'mean',
            'token_count': 'mean'
        }).reset_index()
        
        # Create radar chart
        fig = go.Figure()
        
        for _, row in model_metrics.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row['confidence'], 1/row['processing_time'], row['token_count']/1000],
                theta=['Confidence', 'Speed (1/time)', 'Verbosity (tokens/1000)'],
                fill='toself',
                name=row['model'],
                line=dict(color=self.color_schemes["models"].get(row['model'], "#000000"))
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Model Performance Comparison"
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor='white'
        )
        return fig
    
    def export_chart(self, fig: go.Figure, filename: str, format: str = "html") -> bool:
        """
        Export a chart to file.
        
        Args:
            fig: Plotly figure to export
            filename: Output filename
            format: Export format ('html', 'png', 'pdf', 'svg')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if format == "html":
                fig.write_html(filename)
            elif format == "png":
                fig.write_image(filename)
            elif format == "pdf":
                fig.write_image(filename)
            elif format == "svg":
                fig.write_image(filename)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Chart exported to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting chart: {e}")
            return False