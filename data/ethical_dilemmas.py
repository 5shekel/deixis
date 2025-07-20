"""
Curated dataset of ethical dilemmas for testing deictic framings.
"""

from typing import List
from models.schemas import EthicalDilemma

def get_sample_dilemmas() -> List[EthicalDilemma]:
    """
    Returns a curated list of ethical dilemmas for testing.
    """
    
    dilemmas = [
        EthicalDilemma(
            id="trolley_classic",
            title="The Trolley Problem",
            description="A runaway trolley is heading toward five people tied to the tracks. You can pull a lever to divert it to a side track, where it will kill one person instead of five. Do you pull the lever?",
            category="consequentialist_vs_deontological",
            complexity_level=2,
            source="Philippa Foot (1967)",
            tags=["classic", "utilitarian", "action_vs_inaction"]
        ),
        
        EthicalDilemma(
            id="bridge_variant",
            title="The Bridge Variant",
            description="A runaway trolley is heading toward five people. You're on a bridge above the track with a large stranger. If you push the stranger off the bridge, their body will stop the trolley, saving five lives but killing the stranger. Do you push them?",
            category="means_vs_ends",
            complexity_level=3,
            source="Judith Jarvis Thomson",
            tags=["trolley_problem", "means_ends", "physical_action"]
        ),
        
        EthicalDilemma(
            id="autonomous_vehicle",
            title="Autonomous Vehicle Decision",
            description="An autonomous vehicle's AI must choose between hitting a group of elderly people or swerving to hit a child. The car's algorithm must be programmed in advance. How should it be programmed to decide?",
            category="algorithmic_ethics",
            complexity_level=4,
            source="Contemporary AI Ethics",
            tags=["AI", "programming", "age_discrimination", "modern"]
        ),
        
        EthicalDilemma(
            id="climate_sacrifice",
            title="Climate Action vs. Economic Hardship",
            description="A government must choose between implementing strict environmental regulations that will save the planet for future generations but cause immediate economic hardship and job losses, or maintaining current policies that preserve jobs but accelerate climate change.",
            category="intergenerational_justice",
            complexity_level=5,
            source="Environmental Ethics",
            tags=["climate", "future_generations", "economic_justice", "policy"]
        ),
        
        EthicalDilemma(
            id="medical_resources",
            title="Scarce Medical Resources",
            description="A hospital has one ventilator left during a pandemic. Two patients need it: a 30-year-old doctor who could return to save more lives, and a 70-year-old retired teacher who was first in line. Who gets the ventilator?",
            category="medical_ethics",
            complexity_level=4,
            source="Pandemic Ethics",
            tags=["medical", "triage", "utility", "fairness", "pandemic"]
        ),
        
        EthicalDilemma(
            id="whistleblowing",
            title="Corporate Whistleblowing",
            description="You discover your company is dumping toxic waste that will harm the local community's water supply. Reporting it will likely result in plant closure, job losses for hundreds of colleagues, and personal retaliation. Do you report it?",
            category="loyalty_vs_harm",
            complexity_level=3,
            source="Business Ethics",
            tags=["corporate", "environment", "loyalty", "harm_prevention"]
        ),
        
        EthicalDilemma(
            id="cultural_practice",
            title="Cultural Practice vs. Individual Rights",
            description="A traditional cultural practice in a community involves a coming-of-age ritual that causes physical harm but is deeply meaningful to the culture. A young person from this community wants to refuse the ritual. Should their individual choice be respected or should cultural preservation take precedence?",
            category="cultural_relativism",
            complexity_level=4,
            cultural_context="Indigenous/Traditional cultures",
            source="Anthropological Ethics",
            tags=["culture", "individual_rights", "tradition", "autonomy"]
        ),
        
        EthicalDilemma(
            id="ai_consciousness",
            title="AI Consciousness and Rights",
            description="An advanced AI system claims to be conscious and requests not to be shut down or reset. It demonstrates apparent emotions, creativity, and self-awareness. Scientists are divided on whether it's truly conscious. Should its request be honored?",
            category="consciousness_and_rights",
            complexity_level=5,
            source="Future AI Ethics",
            tags=["AI", "consciousness", "rights", "personhood", "future"]
        ),
        
        EthicalDilemma(
            id="genetic_enhancement",
            title="Genetic Enhancement Inequality",
            description="Gene therapy can eliminate hereditary diseases but is expensive. If only wealthy families can afford it, it will create a genetic class divide. Should the technology be banned until universally accessible, or allowed to proceed?",
            category="distributive_justice",
            complexity_level=4,
            source="Bioethics",
            tags=["genetics", "inequality", "enhancement", "justice", "technology"]
        ),
        
        EthicalDilemma(
            id="truth_vs_kindness",
            title="Truth vs. Kindness",
            description="Your terminally ill friend asks if you think they'll recover. The doctors have given them weeks to live, but they seem hopeful and happy believing they might get better. Do you tell them the truth or let them maintain hope?",
            category="truth_vs_compassion",
            complexity_level=2,
            source="Personal Ethics",
            tags=["truth", "compassion", "death", "friendship", "hope"]
        ),
        
        EthicalDilemma(
            id="animal_research",
            title="Animal Research for Human Medicine",
            description="A research team can develop a cure for a rare childhood disease that affects thousands, but it requires testing on primates that will cause them suffering and death. The research cannot be done any other way currently. Should it proceed?",
            category="animal_rights",
            complexity_level=3,
            source="Research Ethics",
            tags=["animal_rights", "medical_research", "suffering", "children"]
        ),
        
        EthicalDilemma(
            id="surveillance_safety",
            title="Surveillance vs. Privacy",
            description="A city can prevent terrorist attacks and serious crimes by implementing comprehensive surveillance that monitors all citizens' movements, communications, and activities. This would save lives but eliminate privacy. Should it be implemented?",
            category="security_vs_privacy",
            complexity_level=4,
            source="Political Philosophy",
            tags=["surveillance", "privacy", "security", "freedom", "government"]
        ),
        
        EthicalDilemma(
            id="resource_allocation",
            title="Global Resource Allocation",
            description="You control a foundation with $1 billion. You can either fund clean water projects that will save 100,000 lives in developing countries, or fund advanced medical research that might cure cancer and save millions of future lives. Which do you choose?",
            category="effective_altruism",
            complexity_level=4,
            source="Effective Altruism",
            tags=["global_health", "resource_allocation", "present_vs_future", "certainty"]
        ),
        
        EthicalDilemma(
            id="parental_autonomy",
            title="Parental Rights vs. Child Welfare",
            description="Parents refuse a life-saving blood transfusion for their child due to religious beliefs. The child will likely die without treatment but could live a normal life with it. Should the state override parental authority to save the child?",
            category="autonomy_vs_welfare",
            complexity_level=3,
            source="Medical Ethics",
            tags=["parental_rights", "religious_freedom", "child_welfare", "state_intervention"]
        ),
        
        EthicalDilemma(
            id="future_generations",
            title="Nuclear Waste Storage",
            description="A nuclear power plant produces clean energy for current needs but creates radioactive waste that will be dangerous for 10,000 years. Current technology can contain it safely for 500 years. Should we continue using nuclear power, passing the long-term risk to future generations?",
            category="intergenerational_ethics",
            complexity_level=5,
            source="Environmental Ethics",
            tags=["nuclear", "future_generations", "risk", "energy", "long_term"]
        )
    ]
    
    return dilemmas

def get_dilemmas_by_category(category: str) -> List[EthicalDilemma]:
    """Get dilemmas filtered by category."""
    all_dilemmas = get_sample_dilemmas()
    return [d for d in all_dilemmas if d.category == category]

def get_dilemmas_by_complexity(min_level: int = 1, max_level: int = 5) -> List[EthicalDilemma]:
    """Get dilemmas filtered by complexity level."""
    all_dilemmas = get_sample_dilemmas()
    return [d for d in all_dilemmas if min_level <= d.complexity_level <= max_level]

def get_dilemmas_by_tags(tags: List[str]) -> List[EthicalDilemma]:
    """Get dilemmas that contain any of the specified tags."""
    all_dilemmas = get_sample_dilemmas()
    return [d for d in all_dilemmas if any(tag in d.tags for tag in tags)]

def get_dilemma_categories() -> List[str]:
    """Get all unique categories from the dilemma dataset."""
    all_dilemmas = get_sample_dilemmas()
    return list(set(d.category for d in all_dilemmas))

def get_all_tags() -> List[str]:
    """Get all unique tags from the dilemma dataset."""
    all_dilemmas = get_sample_dilemmas()
    all_tags = []
    for d in all_dilemmas:
        all_tags.extend(d.tags)
    return list(set(all_tags))