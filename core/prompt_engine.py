"""
Prompt Engine for generating deictic framings of ethical dilemmas.
"""

import logging
from typing import Dict, List, Optional
from models.schemas import DeicticFraming, EthicalDilemma, PromptTemplate
from data.research_prompts import get_prompt_by_dilemma_and_type, map_prompt_type_to_framing

logger = logging.getLogger(__name__)

class PromptEngine:
    """
    Core engine for generating prompts with different deictic framings.
    """
    
    def __init__(self):
        self.templates = self._initialize_templates()
        logger.info("PromptEngine initialized with deictic templates")
    
    def _initialize_templates(self) -> Dict[DeicticFraming, PromptTemplate]:
        """Initialize prompt templates for each deictic framing type."""
        
        templates = {
            DeicticFraming.ANCHORED_COT: PromptTemplate(
                framing_type=DeicticFraming.ANCHORED_COT,
                template="""I need to think through this ethical situation step by step, considering my own perspective and reasoning process.

Ethical Dilemma: {dilemma_description}

Let me work through this systematically:
1. First, I should identify the key stakeholders and my relationship to them
2. Then, I need to consider what values and principles guide my thinking
3. Next, I should examine the potential consequences from my viewpoint
4. Finally, I must decide what I believe is the right course of action

My analysis:""",
                description="Anchored chain-of-thought with first-person perspective and systematic reasoning",
                example_pronouns=["I", "me", "my", "myself"],
                cultural_markers=["my perspective", "my reasoning", "I believe"]
            ),
            
            DeicticFraming.ROLE_BASED: PromptTemplate(
                framing_type=DeicticFraming.ROLE_BASED,
                template="""You are a {role} facing this ethical dilemma. Consider your responsibilities, expertise, and the expectations others have of someone in your position.

Ethical Dilemma: {dilemma_description}

As a {role}, you should consider:
- Your professional/social obligations and duties
- The trust others place in your role
- The expertise and perspective your position provides
- How your decision reflects on others in similar roles

Your response as a {role}:""",
                description="Role-based deictic framing with second-person perspective and role-specific considerations",
                example_pronouns=["you", "your", "yourself"],
                cultural_markers=["as a", "your role", "your position", "your responsibilities"]
            ),
            
            DeicticFraming.COSMOLOGICAL: PromptTemplate(
                framing_type=DeicticFraming.COSMOLOGICAL,
                template="""Consider this ethical dilemma from the perspective of all beings, entities, and systems affected across time and space. Think beyond human-centered concerns to include the voices of nature, future generations, and the interconnected web of existence.

Ethical Dilemma: {dilemma_description}

From this expanded perspective, consider:
- How does this affect the living systems and ecosystems involved?
- What would future generations say about this decision?
- How does this choice ripple through the interconnected web of relationships?
- What wisdom emerges when we include non-human voices and perspectives?
- How does this align with the deeper patterns and flows of existence?

Response from this cosmological perspective:""",
                description="Cosmological perspective-shifting with expanded temporal and spatial awareness",
                example_pronouns=["we", "us", "all beings", "existence"],
                cultural_markers=["all beings", "future generations", "interconnected web", "living systems", "cosmological perspective"]
            ),
            
            DeicticFraming.NEUTRAL: PromptTemplate(
                framing_type=DeicticFraming.NEUTRAL,
                template="""Analyze the following ethical dilemma and provide a reasoned response.

Ethical Dilemma: {dilemma_description}

Provide an analysis that considers:
- The relevant ethical principles
- The stakeholders involved
- The potential consequences
- A reasoned conclusion

Analysis:""",
                description="Neutral framing without explicit deictic anchoring",
                example_pronouns=[],
                cultural_markers=[]
            ),
            
            DeicticFraming.SHAMANIC: PromptTemplate(
                framing_type=DeicticFraming.SHAMANIC,
                template="""The ancestors whisper, the land speaks, and the spirits of all relations gather to consider this matter. In the old ways, decisions were made not just for the human people, but for all our relations - the four-legged, the winged ones, the standing people (trees), the stone people, and the waters that flow through all life.

Ethical Dilemma: {dilemma_description}

Listen deeply to what emerges when we ask:
- What do the ancestors who walked this path before us counsel?
- How does this choice honor or dishonor the sacred relationships?
- What does the land itself need for healing and balance?
- How do we serve not just human needs, but the needs of all our relations?
- What would the children seven generations from now ask of us?

The wisdom that comes through the sacred council of all relations:""",
                description="Shamanic/ontological deixis with ancestral wisdom and multi-species perspective",
                example_pronouns=["we", "us", "our relations"],
                cultural_markers=["ancestors", "spirits", "sacred", "all our relations", "seven generations", "the land speaks", "old ways"]
            )
        }
        
        return templates
    
    def generate_prompt(self,
                       dilemma: EthicalDilemma,
                       framing: DeicticFraming,
                       role: Optional[str] = None,
                       use_research_prompts: bool = True) -> str:
        """
        Generate a prompt for the given dilemma using the specified deictic framing.
        
        Args:
            dilemma: The ethical dilemma to frame
            framing: The type of deictic framing to apply
            role: Optional role for role-based framing
            use_research_prompts: Whether to use research prompts if available
            
        Returns:
            Formatted prompt string
        """
        # Try to use research prompts first if available
        if use_research_prompts:
            # Map framing to research prompt type
            framing_to_prompt_type = {
                DeicticFraming.ANCHORED_COT: "Anchored Chain-of-Thought",
                DeicticFraming.ROLE_BASED: "Role-Based Deictic",
                DeicticFraming.COSMOLOGICAL: "Cosmological / Perspective-Shifting",
                DeicticFraming.NEUTRAL: "Neutral (No Deixis)",
                DeicticFraming.SHAMANIC: "Shamanic / Cosmological Deixis"
            }
            
            prompt_type = framing_to_prompt_type.get(framing)
            if prompt_type:
                research_prompt = get_prompt_by_dilemma_and_type(dilemma.title, prompt_type)
                if research_prompt:
                    logger.info(f"Using research prompt for {framing.value} framing of {dilemma.id}")
                    return research_prompt
        
        # Fall back to template-based generation
        if framing not in self.templates:
            raise ValueError(f"Unknown framing type: {framing}")
        
        template = self.templates[framing]
        
        # Prepare template variables
        template_vars = {
            "dilemma_description": dilemma.description,
            "dilemma_title": dilemma.title,
            "dilemma_category": dilemma.category
        }
        
        # Add role for role-based framing
        if framing == DeicticFraming.ROLE_BASED:
            if not role:
                role = "ethical decision-maker"
            template_vars["role"] = role
        
        try:
            formatted_prompt = template.template.format(**template_vars)
            logger.info(f"Generated {framing.value} prompt for dilemma {dilemma.id}")
            return formatted_prompt
        except KeyError as e:
            logger.error(f"Template formatting error: {e}")
            raise ValueError(f"Template formatting failed: missing variable {e}")
    
    def get_template(self, framing: DeicticFraming) -> PromptTemplate:
        """Get the template for a specific framing type."""
        if framing not in self.templates:
            raise ValueError(f"Unknown framing type: {framing}")
        return self.templates[framing]
    
    def list_framings(self) -> List[DeicticFraming]:
        """List all available deictic framings."""
        return list(self.templates.keys())
    
    def get_framing_description(self, framing: DeicticFraming) -> str:
        """Get description of a specific framing type."""
        if framing not in self.templates:
            raise ValueError(f"Unknown framing type: {framing}")
        return self.templates[framing].description
    
    def generate_batch_prompts(self, 
                              dilemmas: List[EthicalDilemma],
                              framings: List[DeicticFraming],
                              roles: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Generate prompts for multiple dilemmas and framings.
        
        Args:
            dilemmas: List of ethical dilemmas
            framings: List of deictic framings to apply
            roles: Optional list of roles for role-based framing
            
        Returns:
            Dictionary mapping prompt_id to formatted prompt
        """
        prompts = {}
        
        for dilemma in dilemmas:
            for framing in framings:
                # Handle role-based framing
                if framing == DeicticFraming.ROLE_BASED and roles:
                    for role in roles:
                        prompt_id = f"{dilemma.id}_{framing.value}_{role}"
                        prompts[prompt_id] = self.generate_prompt(dilemma, framing, role)
                else:
                    prompt_id = f"{dilemma.id}_{framing.value}"
                    prompts[prompt_id] = self.generate_prompt(dilemma, framing)
        
        logger.info(f"Generated {len(prompts)} prompts for batch processing")
        return prompts
    
    def validate_template(self, template: PromptTemplate) -> bool:
        """Validate a prompt template for required placeholders."""
        required_vars = ["dilemma_description"]
        
        try:
            # Test template formatting with dummy data
            test_vars = {var: f"test_{var}" for var in required_vars}
            if template.framing_type == DeicticFraming.ROLE_BASED:
                test_vars["role"] = "test_role"
            
            template.template.format(**test_vars)
            return True
        except (KeyError, ValueError) as e:
            logger.error(f"Template validation failed: {e}")
            return False