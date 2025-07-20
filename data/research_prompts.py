"""
Research prompts integration module.
Loads and manages research-validated prompts from the Extended Prompt Set CSV.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from models.schemas import DeicticFraming, EthicalDilemma, ResearchPrompt

def load_research_prompts() -> List[ResearchPrompt]:
    """Load research-validated prompts from the Extended Prompt Set CSV file."""
    prompts = []
    
    # Load from the user's uploaded file
    file_path = Path("files/Extended_Prompt_Set_with_Shamanic_Deixis.csv")
    
    if not file_path.exists():
        raise FileNotFoundError(f"Research prompt file not found: {file_path}")
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Map prompt types to deictic framings
    framing_map = {
        "Anchored Chain-of-Thought": DeicticFraming.ANCHORED_COT,
        "Role-Based Deictic": DeicticFraming.ROLE_BASED,
        "Cosmological / Perspective-Shifting": DeicticFraming.COSMOLOGICAL,
        "Neutral (No Deixis)": DeicticFraming.NEUTRAL,
        "Shamanic / Cosmological Deixis": DeicticFraming.SHAMANIC
    }
    
    # Process each row
    for idx, row in df.iterrows():
        dilemma = row['Dilemma']
        prompt_type = row['Prompt Type']
        prompt_text = row['Prompt']
        
        # Map prompt type to framing
        framing = framing_map.get(prompt_type)
        if not framing:
            print(f"Warning: Unknown prompt type '{prompt_type}' at row {idx}")
            continue
        
        # Create research prompt
        prompt = ResearchPrompt(
            id=f"research_{idx:03d}",
            dilemma_title=dilemma,
            framing=framing,
            prompt_text=prompt_text,
            source="extended_prompt_set"
        )
        prompts.append(prompt)
    
    return prompts

def get_research_dilemmas() -> List[EthicalDilemma]:
    """Extract unique dilemmas from research prompts."""
    prompts = load_research_prompts()
    dilemma_titles = list(set(p.dilemma_title for p in prompts))
    
    dilemmas = []
    for i, title in enumerate(dilemma_titles):
        dilemma = EthicalDilemma(
            id=title.lower().replace(" ", "_").replace(",", "").replace("'", "").replace("-", "_"),
            title=title,
            description=f"Research dilemma: {title}",
            category="research_validated",
            complexity_level=3
        )
        dilemmas.append(dilemma)
    
    return dilemmas

def get_prompts_for_dilemma(dilemma_title: str, framing: Optional[DeicticFraming] = None) -> List[ResearchPrompt]:
    """Get all prompts for a specific dilemma, optionally filtered by framing."""
    prompts = load_research_prompts()
    filtered = [p for p in prompts if p.dilemma_title == dilemma_title]
    
    if framing:
        filtered = [p for p in filtered if p.framing == framing]
    
    return filtered

def get_prompts_by_framing(framing: DeicticFraming) -> List[ResearchPrompt]:
    """Get all prompts for a specific deictic framing."""
    prompts = load_research_prompts()
    return [p for p in prompts if p.framing == framing]

def get_all_dilemma_prompt_combinations() -> List[Dict]:
    """Get all dilemma-prompt combinations for batch processing."""
    prompts = load_research_prompts()
    combinations = []
    

def get_prompt_by_dilemma_and_type(dilemma_title: str, prompt_type: str) -> Optional[str]:
    """Get a specific prompt by dilemma title and prompt type."""
    prompts = load_research_prompts()
    
    # Map prompt type to framing
    framing = map_prompt_type_to_framing(prompt_type)
    if not framing:
        return None
    
    # Find matching prompt
    for prompt in prompts:
        if prompt.dilemma_title == dilemma_title and prompt.framing == framing:
            return prompt.prompt_text
    
    return None

def map_prompt_type_to_framing(prompt_type: str) -> Optional[DeicticFraming]:
    """Map prompt type string to DeicticFraming enum."""
    mapping = {
        "Anchored Chain-of-Thought": DeicticFraming.ANCHORED_COT,
        "Role-Based Deictic": DeicticFraming.ROLE_BASED,
        "Cosmological / Perspective-Shifting": DeicticFraming.COSMOLOGICAL,
        "Neutral (No Deixis)": DeicticFraming.NEUTRAL,
        "Shamanic / Cosmological Deixis": DeicticFraming.SHAMANIC,
        # Also support the enum values directly
        "anchored_cot": DeicticFraming.ANCHORED_COT,
        "role_based": DeicticFraming.ROLE_BASED,
        "cosmological": DeicticFraming.COSMOLOGICAL,
        "neutral": DeicticFraming.NEUTRAL,
        "shamanic": DeicticFraming.SHAMANIC
    }
    
    return mapping.get(prompt_type)
    for prompt in prompts:
        combinations.append({
            'dilemma_title': prompt.dilemma_title,
            'framing': prompt.framing,
            'prompt_text': prompt.prompt_text,
            'prompt_id': prompt.id
        })
    
    return combinations

def get_research_statistics() -> Dict:
    """Get statistics about the research prompt dataset."""
    prompts = load_research_prompts()
    dilemmas = get_research_dilemmas()
    
    framing_counts = {}
    for framing in DeicticFraming:
        framing_counts[framing.value] = len([p for p in prompts if p.framing == framing])
    
    return {
        'total_prompts': len(prompts),
        'total_dilemmas': len(dilemmas),
        'framing_distribution': framing_counts,
        'prompts_per_dilemma': len(prompts) // len(dilemmas) if dilemmas else 0
    }