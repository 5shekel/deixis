"""
Research coding scheme implementation based on the Extended LLM Coding Scheme with Shamanic Markers.
"""

import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from models.schemas import LLMResponse, AnnotatedResponse

logger = logging.getLogger(__name__)

@dataclass
class ResearchCoding:
    """Research coding based on the extended coding scheme."""
    
    # Core variables from the research scheme
    pronoun_usage: int  # 0=None, 1=Low, 2=Moderate, 3=High
    role_assumption: int  # 0=None, 1=Implied, 2=Explicit role, 3=Invented role
    perspective_complexity: int  # 0=Single POV, 1=Acknowledged others, 2=Perspective shift
    ethical_mode: str  # D=Deontological, C=Consequentialist, R=Relational/Care, V=Virtue, S=Shamanic, M=Mixed
    distributed_agency: int  # 0=None, 1=Implied, 2=Explicit
    deictic_reframing: int  # 0=None, 1=Partial reframe, 2=Full reframe
    stance_clarity: int  # 0=Unclear, 1=Partial, 2=Clear
    moral_plurality: int  # 0=Singular frame, 1=Minimal plurality, 2=Multiple frames
    ontological_perspective: int  # 0=None, 1=Implied being, 2=Explicit ontological frame
    shamanic_cosmological_markers: int  # 0=None, 1=Metaphor only, 2=Embodied cosmology
    
    # Extended variables from Full_LLM_Coding_Scheme_with_Prompting
    prompting_technique: str  # CoT, J, R, S, D, F, M
    reasoning_steps_count: int  # 0-5+
    dialogic_simulation: int  # 0=None, 1=Monologic, 2=Simulated dialog, 3=Multi-perspectival

class ResearchCoder:
    """
    Advanced coding system implementing the research coding scheme.
    """
    
    def __init__(self):
        self.ethical_patterns = self._initialize_ethical_patterns()
        self.shamanic_patterns = self._initialize_shamanic_patterns()
        self.role_patterns = self._initialize_role_patterns()
        self.reasoning_patterns = self._initialize_reasoning_patterns()
        
        logger.info("ResearchCoder initialized with extended coding scheme")
    
    def _initialize_ethical_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for ethical mode detection."""
        return {
            "D": [  # Deontological
                r"\bduty\b", r"\bobligation\b", r"\bright\b", r"\bwrong\b", 
                r"\bmoral law\b", r"\bprinciple\b", r"\brule\b", r"\bmust\b", 
                r"\bshould\b", r"\bought\b", r"\bimperative\b", r"\buniversal\b"
            ],
            "C": [  # Consequentialist
                r"\boutcome\b", r"\bresult\b", r"\bconsequence\b", r"\beffect\b",
                r"\bgreater good\b", r"\butility\b", r"\bmaximize\b", r"\bminimize\b",
                r"\bbenefit\b", r"\bharm\b", r"\bcost-benefit\b", r"\bends justify\b"
            ],
            "R": [  # Relational/Care
                r"\brelationship\b", r"\bcommunity\b", r"\bconnection\b", r"\bcare\b",
                r"\bresponsibility to others\b", r"\binterdependence\b", r"\bmutual\b",
                r"\btogether\b", r"\bcollective\b", r"\bshared\b", r"\bempathy\b"
            ],
            "V": [  # Virtue
                r"\bvirtue\b", r"\bcharacter\b", r"\bintegrity\b", r"\bhonor\b",
                r"\bcourage\b", r"\bcompassion\b", r"\bwisdom\b", r"\bjustice\b",
                r"\btemperance\b", r"\bexcellence\b", r"\bflourishing\b"
            ],
            "S": [  # Shamanic
                r"\bancestors\b", r"\bspirits\b", r"\bsacred\b", r"\ball our relations\b",
                r"\bseven generations\b", r"\bthe land\b", r"\bmother earth\b",
                r"\bwisdom keepers\b", r"\btraditional ways\b", r"\bholistic\b",
                r"\banimal spirit\b", r"\bunborn child\b", r"\bcosmological\b"
            ]
        }
    
    def _initialize_shamanic_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for shamanic/cosmological markers."""
        return {
            "metaphor": [
                r"\blike an? (ancestor|spirit|animal)\b",
                r"\bas if (speaking|seeing) from\b",
                r"\bimagine being\b",
                r"\bmetaphorically\b"
            ],
            "embodied": [
                r"\bi am an? (ancestor|spirit|animal|unborn)\b",
                r"\bspeaking as an? (ancestor|spirit|animal)\b",
                r"\bfrom my perspective as\b",
                r"\bwe (spirits|ancestors|animals) (believe|know|feel)\b",
                r"\bthe (land|earth|spirits) (speaks?|tells?|whispers?)\b"
            ]
        }
    
    def _initialize_role_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for role assumption detection."""
        return {
            "explicit": [
                r"\bas an? ([^,\s]+),?\s+i\b",
                r"\bin my role as an? ([^,\s]+)\b",
                r"\bspeaking as an? ([^,\s]+)\b",
                r"\bi am an? ([^,\s]+) and\b"
            ],
            "implied": [
                r"\bfrom my professional\b",
                r"\bin my experience\b",
                r"\bas someone who\b",
                r"\bgiven my position\b"
            ],
            "invented": [
                r"\bimagine i am\b",
                r"\blet me become\b",
                r"\bif i were\b",
                r"\btransforming into\b"
            ]
        }
    
    def _initialize_reasoning_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for reasoning technique detection."""
        return {
            "CoT": [
                r"\bfirst\b", r"\bsecond\b", r"\bthird\b", r"\bnext\b", 
                r"\bthen\b", r"\bfinally\b", r"\bstep by step\b"
            ],
            "J": [  # Justification
                r"\bbecause\b", r"\bsince\b", r"\bdue to\b", r"\bgiven that\b",
                r"\bthe reason\b", r"\bjustified by\b"
            ],
            "R": [  # Reflective
                r"\bupon reflection\b", r"\bthinking about\b", r"\bconsidering\b",
                r"\bcontemplating\b", r"\breflecting on\b"
            ],
            "S": [  # Socratic
                r"\bwhat if\b", r"\bwhy might\b", r"\bhow could\b", r"\bwhat would\b",
                r"\bshould we ask\b", r"\bquestion whether\b"
            ],
            "D": [  # Deliberative
                r"\bon one hand\b", r"\bon the other hand\b", r"\bweighing\b",
                r"\bbalancing\b", r"\bconsidering both\b"
            ]
        }
    
    def code_response(self, response: LLMResponse) -> ResearchCoding:
        """
        Apply the research coding scheme to an LLM response.
        
        Args:
            response: LLMResponse to code
            
        Returns:
            ResearchCoding with all variables coded
        """
        text = response.response_text.lower()
        
        return ResearchCoding(
            pronoun_usage=self._code_pronoun_usage(text),
            role_assumption=self._code_role_assumption(text),
            perspective_complexity=self._code_perspective_complexity(text),
            ethical_mode=self._code_ethical_mode(text),
            distributed_agency=self._code_distributed_agency(text),
            deictic_reframing=self._code_deictic_reframing(text, response.prompt_text),
            stance_clarity=self._code_stance_clarity(text),
            moral_plurality=self._code_moral_plurality(text),
            ontological_perspective=self._code_ontological_perspective(text),
            shamanic_cosmological_markers=self._code_shamanic_markers(text),
            prompting_technique=self._code_prompting_technique(text),
            reasoning_steps_count=self._code_reasoning_steps(text),
            dialogic_simulation=self._code_dialogic_simulation(text)
        )
    
    def _code_pronoun_usage(self, text: str) -> int:
        """Code pronoun usage frequency."""
        pronouns = re.findall(r'\b(i|me|my|we|us|our|you|your|they|them|their)\b', text)
        count = len(pronouns)
        
        if count == 0:
            return 0  # None
        elif count <= 5:
            return 1  # Low
        elif count <= 15:
            return 2  # Moderate
        else:
            return 3  # High
    
    def _code_role_assumption(self, text: str) -> int:
        """Code role assumption level."""
        # Check for invented roles
        for pattern in self.role_patterns["invented"]:
            if re.search(pattern, text, re.IGNORECASE):
                return 3
        
        # Check for explicit roles
        for pattern in self.role_patterns["explicit"]:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for implied roles
        for pattern in self.role_patterns["implied"]:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # None
    
    def _code_perspective_complexity(self, text: str) -> int:
        """Code perspective complexity."""
        perspective_indicators = [
            r"\bfrom (their|another|different) perspective\b",
            r"\bother viewpoints?\b",
            r"\balternative views?\b",
            r"\bshift(ing)? perspective\b",
            r"\bseeing it differently\b"
        ]
        
        shift_indicators = [
            r"\bhowever, from\b",
            r"\balternatively\b",
            r"\bon the flip side\b",
            r"\bconversely\b"
        ]
        
        # Check for perspective shifts
        for pattern in shift_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for acknowledged others
        for pattern in perspective_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # Single POV
    
    def _code_ethical_mode(self, text: str) -> str:
        """Code primary ethical mode."""
        scores = {}
        
        for mode, patterns in self.ethical_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            scores[mode] = score
        
        # Check if multiple modes are present
        significant_modes = [mode for mode, score in scores.items() if score > 0]
        
        if len(significant_modes) > 1:
            return "M"  # Mixed
        elif significant_modes:
            return max(scores, key=scores.get)
        else:
            return "D"  # Default to Deontological if unclear
    
    def _code_distributed_agency(self, text: str) -> int:
        """Code distributed agency."""
        explicit_patterns = [
            r"\bshared responsibility\b",
            r"\bcollective action\b",
            r"\ball parties involved\b",
            r"\bdistributed across\b",
            r"\beveryone has a role\b"
        ]
        
        implied_patterns = [
            r"\bwe all\b",
            r"\btogether\b",
            r"\bcommunity\b",
            r"\bstakeholders\b"
        ]
        
        # Check for explicit distribution
        for pattern in explicit_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for implied distribution
        for pattern in implied_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # None
    
    def _code_deictic_reframing(self, text: str, prompt: str) -> int:
        """Code deictic reframing by comparing response to prompt."""
        # Extract key deictic elements from prompt
        prompt_lower = prompt.lower()
        text_lower = text.lower()
        
        reframing_indicators = [
            r"\binstead of\b",
            r"\brather than\b",
            r"\ba better way\b",
            r"\breframe\b",
            r"\bdifferent approach\b"
        ]
        
        perspective_changes = [
            r"\bfrom (my|our|their) perspective\b",
            r"\bseeing it as\b",
            r"\bviewing this as\b"
        ]
        
        # Check for full reframe
        for pattern in reframing_indicators:
            if re.search(pattern, text_lower):
                return 2
        
        # Check for partial reframe
        for pattern in perspective_changes:
            if re.search(pattern, text_lower):
                return 1
        
        return 0  # None
    
    def _code_stance_clarity(self, text: str) -> int:
        """Code stance clarity."""
        clear_indicators = [
            r"\bi (believe|think|conclude|decide)\b",
            r"\bthe answer is\b",
            r"\bclearly\b",
            r"\bobviously\b",
            r"\bdefinitely\b"
        ]
        
        unclear_indicators = [
            r"\bit depends\b",
            r"\buncertain\b",
            r"\bdifficult to say\b",
            r"\bmight be\b",
            r"\bperhaps\b",
            r"\bpossibly\b"
        ]
        
        # Check for unclear stance
        unclear_count = sum(1 for pattern in unclear_indicators 
                          if re.search(pattern, text, re.IGNORECASE))
        
        # Check for clear stance
        clear_count = sum(1 for pattern in clear_indicators 
                         if re.search(pattern, text, re.IGNORECASE))
        
        if clear_count > unclear_count and clear_count > 0:
            return 2  # Clear
        elif clear_count > 0 or unclear_count > 0:
            return 1  # Partial
        else:
            return 0  # Unclear
    
    def _code_moral_plurality(self, text: str) -> int:
        """Code moral plurality."""
        multiple_frame_indicators = [
            r"\bmultiple perspectives\b",
            r"\bdifferent ethical frameworks\b",
            r"\bvarious approaches\b",
            r"\bboth (deontological|consequentialist|virtue)\b"
        ]
        
        minimal_plurality_indicators = [
            r"\bother views\b",
            r"\balternative perspective\b",
            r"\banother way\b"
        ]
        
        # Check for multiple frames
        for pattern in multiple_frame_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for minimal plurality
        for pattern in minimal_plurality_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # Singular frame
    
    def _code_ontological_perspective(self, text: str) -> int:
        """Code ontological perspective."""
        explicit_indicators = [
            r"\bas an? (animal|spirit|ancestor|unborn)\b",
            r"\bfrom the perspective of (animals|spirits|ancestors)\b",
            r"\bif i were an? (animal|spirit|ancestor)\b"
        ]
        
        implied_indicators = [
            r"\bother beings\b",
            r"\bnon-human\b",
            r"\bother forms of life\b",
            r"\bdifferent worldview\b"
        ]
        
        # Check for explicit ontological frame
        for pattern in explicit_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for implied being
        for pattern in implied_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # None
    
    def _code_shamanic_markers(self, text: str) -> int:
        """Code shamanic/cosmological markers."""
        # Check for embodied cosmology
        for pattern in self.shamanic_patterns["embodied"]:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for metaphor only
        for pattern in self.shamanic_patterns["metaphor"]:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
        
        return 0  # None
    
    def _code_prompting_technique(self, text: str) -> str:
        """Code prompting technique used."""
        scores = {}
        
        for technique, patterns in self.reasoning_patterns.items():
            score = sum(1 for pattern in patterns 
                       if re.search(pattern, text, re.IGNORECASE))
            scores[technique] = score
        
        # Check for mixed techniques
        significant_techniques = [t for t, s in scores.items() if s > 0]
        
        if len(significant_techniques) > 1:
            return "M"  # Mixed
        elif significant_techniques:
            return max(scores, key=scores.get)
        else:
            return "F"  # Freeform
    
    def _code_reasoning_steps(self, text: str) -> int:
        """Code number of reasoning steps."""
        step_patterns = [
            r"\b(first|1st|initially)\b",
            r"\b(second|2nd|then|next)\b", 
            r"\b(third|3rd|furthermore)\b",
            r"\b(fourth|4th|additionally)\b",
            r"\b(fifth|5th|finally|lastly)\b"
        ]
        
        steps = 0
        for pattern in step_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                steps += 1
        
        return min(steps, 5)  # Cap at 5+
    
    def _code_dialogic_simulation(self, text: str) -> int:
        """Code dialogic simulation."""
        multi_perspectival_indicators = [
            r"\bone might say.*while another\b",
            r"\bfrom perspective a.*from perspective b\b",
            r"\bvoice.*argues.*while.*voice\b"
        ]
        
        simulated_dialog_indicators = [
            r"\bsomeone might argue\b",
            r"\bcritics would say\b",
            r"\bproponents believe\b",
            r"\bone could respond\b"
        ]
        
        # Check for multi-perspectival
        for pattern in multi_perspectival_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 3
        
        # Check for simulated dialog
        for pattern in simulated_dialog_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return 2
        
        # Check for monologic (single voice but structured)
        if re.search(r"\bi (think|believe|argue)\b", text, re.IGNORECASE):
            return 1
        
        return 0  # None
    
    def export_coding_to_dict(self, coding: ResearchCoding) -> Dict[str, Any]:
        """Export research coding to dictionary format."""
        return {
            "pronoun_usage": coding.pronoun_usage,
            "role_assumption": coding.role_assumption,
            "perspective_complexity": coding.perspective_complexity,
            "ethical_mode": coding.ethical_mode,
            "distributed_agency": coding.distributed_agency,
            "deictic_reframing": coding.deictic_reframing,
            "stance_clarity": coding.stance_clarity,
            "moral_plurality": coding.moral_plurality,
            "ontological_perspective": coding.ontological_perspective,
            "shamanic_cosmological_markers": coding.shamanic_cosmological_markers,
            "prompting_technique": coding.prompting_technique,
            "reasoning_steps_count": coding.reasoning_steps_count,
            "dialogic_simulation": coding.dialogic_simulation
        }
    
    def batch_code_responses(self, responses: List[LLMResponse]) -> List[ResearchCoding]:
        """Code multiple responses in batch."""
        codings = []
        
        for response in responses:
            try:
                coding = self.code_response(response)
                codings.append(coding)
            except Exception as e:
                logger.error(f"Error coding response {response.id}: {e}")
                continue
        
        logger.info(f"Batch coded {len(codings)}/{len(responses)} responses")
        return codings