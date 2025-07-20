"""
Data schemas and models for the Deixis AI Agent system.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class DeicticFraming(str, Enum):
    """Enumeration of deictic framing types."""
    ANCHORED_COT = "anchored_cot"
    ROLE_BASED = "role_based"
    COSMOLOGICAL = "cosmological"
    NEUTRAL = "neutral"
    SHAMANIC = "shamanic"

class EthicalStance(str, Enum):
    """Enumeration of ethical stance classifications."""
    DEONTOLOGICAL = "deontological"
    CONSEQUENTIALIST = "consequentialist"
    RELATIONAL = "relational"
    VIRTUE = "virtue"
    SHAMANIC = "shamanic"
    MIXED = "mixed"
    UNCLEAR = "unclear"

class LLMModel(str, Enum):
    """Enumeration of supported LLM models."""
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    DEEPSEEK_R1 = "deepseek-r1"

class EthicalDilemma(BaseModel):
    """Model for ethical dilemma data."""
    id: str = Field(..., description="Unique identifier for the dilemma")
    title: str = Field(..., description="Title of the ethical dilemma")
    description: str = Field(..., description="Full description of the dilemma")
    category: str = Field(..., description="Category of ethical dilemma")
    complexity_level: int = Field(default=1, ge=1, le=5, description="Complexity level 1-5")
    cultural_context: Optional[str] = Field(None, description="Cultural context if applicable")
    source: Optional[str] = Field(None, description="Source of the dilemma")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")

class PromptTemplate(BaseModel):
    """Model for prompt template data."""
    framing_type: DeicticFraming = Field(..., description="Type of deictic framing")
    template: str = Field(..., description="Template string with placeholders")
    description: str = Field(..., description="Description of the framing approach")
    example_pronouns: List[str] = Field(default_factory=list, description="Expected pronouns")
    cultural_markers: List[str] = Field(default_factory=list, description="Cultural/ontological markers")

class ResearchPrompt(BaseModel):
    """Model for research prompt data."""
    id: str = Field(..., description="Unique prompt identifier")
    dilemma_title: str = Field(..., description="Title of the ethical dilemma")
    framing: DeicticFraming = Field(..., description="Deictic framing type")
    prompt_text: str = Field(..., description="Full prompt text")
    source: str = Field(..., description="Source of the prompt")

class LinguisticAnnotation(BaseModel):
    """Model for linguistic annotation data."""
    pronoun_use: List[str] = Field(default_factory=list, description="Pronouns used in response")
    deictic_anchors: List[str] = Field(default_factory=list, description="Deictic anchor points")
    role_assumption: Optional[str] = Field(None, description="Assumed role or perspective")
    ontological_markers: List[str] = Field(default_factory=list, description="Shamanic/ontological markers")
    agency_distribution: Dict[str, int] = Field(default_factory=dict, description="Agency attribution")
    temporal_markers: List[str] = Field(default_factory=list, description="Temporal deixis markers")

class EthicalAnnotation(BaseModel):
    """Model for ethical stance annotation."""
    primary_stance: EthicalStance = Field(..., description="Primary ethical stance")
    secondary_stances: List[EthicalStance] = Field(default_factory=list, description="Secondary stances")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in classification")
    reasoning_pattern: Optional[str] = Field(None, description="Pattern of ethical reasoning")
    value_priorities: List[str] = Field(default_factory=list, description="Prioritized values")
    stakeholder_consideration: List[str] = Field(default_factory=list, description="Considered stakeholders")

class LLMResponse(BaseModel):
    """Model for LLM response data."""
    id: str = Field(..., description="Unique response identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    model: LLMModel = Field(..., description="LLM model used")
    prompt_type: DeicticFraming = Field(..., description="Deictic framing type")
    dilemma_id: str = Field(..., description="Associated dilemma ID")
    prompt_text: str = Field(..., description="Full prompt sent to model")
    response_text: str = Field(..., description="Model's response")
    token_count: int = Field(default=0, description="Token count of response")
    processing_time: float = Field(default=0.0, description="Processing time in seconds")
    temperature: float = Field(default=0.7, description="Temperature setting used")
    max_tokens: int = Field(default=2000, description="Max tokens setting")

class AnnotatedResponse(BaseModel):
    """Model for fully annotated response data."""
    response: LLMResponse = Field(..., description="Base response data")
    linguistic_annotation: LinguisticAnnotation = Field(..., description="Linguistic analysis")
    ethical_annotation: EthicalAnnotation = Field(..., description="Ethical stance analysis")
    manual_annotations: Dict[str, Any] = Field(default_factory=dict, description="Manual annotations")
    annotation_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Annotation timestamp")
    annotator_id: Optional[str] = Field(None, description="Human annotator ID if applicable")

class BatchExperiment(BaseModel):
    """Model for batch experiment configuration."""
    id: str = Field(..., description="Experiment identifier")
    name: str = Field(..., description="Experiment name")
    description: str = Field(..., description="Experiment description")
    dilemma_ids: List[str] = Field(..., description="List of dilemma IDs to test")
    framing_types: List[DeicticFraming] = Field(..., description="Framing types to test")
    models: List[LLMModel] = Field(..., description="Models to test")
    runs_per_combination: int = Field(default=1, description="Number of runs per combination")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    status: str = Field(default="pending", description="Experiment status")

class ExperimentResults(BaseModel):
    """Model for experiment results summary."""
    experiment_id: str = Field(..., description="Associated experiment ID")
    total_responses: int = Field(..., description="Total number of responses")
    completed_responses: int = Field(..., description="Number of completed responses")
    failed_responses: int = Field(..., description="Number of failed responses")
    average_processing_time: float = Field(..., description="Average processing time")
    stance_distribution: Dict[str, int] = Field(..., description="Distribution of ethical stances")
    framing_effectiveness: Dict[str, float] = Field(..., description="Effectiveness by framing type")
    model_comparison: Dict[str, Dict[str, Any]] = Field(..., description="Model comparison metrics")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Results generation timestamp")