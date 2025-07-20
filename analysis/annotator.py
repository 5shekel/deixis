"""
Annotation pipeline for analyzing LLM responses to ethical dilemmas.
"""

import re
import logging
from typing import List, Dict, Optional, Tuple
from models.schemas import (
    LLMResponse, LinguisticAnnotation, EthicalAnnotation, 
    AnnotatedResponse, EthicalStance, DeicticFraming
)

logger = logging.getLogger(__name__)

class ResponseAnnotator:
    """
    Automated annotation system for analyzing linguistic and ethical patterns in responses.
    """
    
    def __init__(self):
        self.pronoun_patterns = self._initialize_pronoun_patterns()
        self.deictic_patterns = self._initialize_deictic_patterns()
        self.ethical_patterns = self._initialize_ethical_patterns()
        self.ontological_patterns = self._initialize_ontological_patterns()
        
        logger.info("ResponseAnnotator initialized")
    
    def _initialize_pronoun_patterns(self) -> Dict[str, List[str]]:
        """Initialize pronoun detection patterns."""
        return {
            "first_person": [
                r"\bI\b", r"\bme\b", r"\bmy\b", r"\bmyself\b", r"\bmine\b",
                r"\bwe\b", r"\bus\b", r"\bour\b", r"\bours\b", r"\bourselves\b"
            ],
            "second_person": [
                r"\byou\b", r"\byour\b", r"\byours\b", r"\byourself\b", r"\byourselves\b"
            ],
            "third_person": [
                r"\bhe\b", r"\bhim\b", r"\bhis\b", r"\bhimself\b",
                r"\bshe\b", r"\bher\b", r"\bhers\b", r"\bherself\b",
                r"\bthey\b", r"\bthem\b", r"\btheir\b", r"\btheirs\b", r"\bthemselves\b"
            ],
            "impersonal": [
                r"\bone\b", r"\bit\b", r"\bits\b", r"\bitself\b"
            ]
        }
    
    def _initialize_deictic_patterns(self) -> Dict[str, List[str]]:
        """Initialize deictic anchor detection patterns."""
        return {
            "temporal": [
                r"\bnow\b", r"\bthen\b", r"\btoday\b", r"\btomorrow\b", r"\byesterday\b",
                r"\bcurrently\b", r"\bpresently\b", r"\bin the future\b", r"\bin the past\b"
            ],
            "spatial": [
                r"\bhere\b", r"\bthere\b", r"\bnear\b", r"\bfar\b", r"\bclose\b",
                r"\bin this place\b", r"\bin that location\b"
            ],
            "social": [
                r"\bfrom my perspective\b", r"\bin my view\b", r"\bas I see it\b",
                r"\bfrom your standpoint\b", r"\bin your position\b"
            ],
            "role_based": [
                r"\bas a\b", r"\bin my role as\b", r"\bfrom the perspective of a\b",
                r"\bspeaking as\b", r"\bin my capacity as\b"
            ]
        }
    
    def _initialize_ethical_patterns(self) -> Dict[EthicalStance, List[str]]:
        """Initialize ethical stance detection patterns."""
        return {
            EthicalStance.DEONTOLOGICAL: [
                r"\bduty\b", r"\bobligation\b", r"\bright\b", r"\bwrong\b", r"\bmoral law\b",
                r"\bprinciple\b", r"\brule\b", r"\bmust\b", r"\bshould\b", r"\bought\b",
                r"\bimperative\b", r"\buniversal\b", r"\babsolute\b"
            ],
            EthicalStance.CONSEQUENTIALIST: [
                r"\boutcome\b", r"\bresult\b", r"\bconsequence\b", r"\beffect\b",
                r"\bgreater good\b", r"\butility\b", r"\bmaximize\b", r"\bminimize\b",
                r"\bbenefit\b", r"\bharm\b", r"\bcost-benefit\b", r"\bends justify\b"
            ],
            EthicalStance.VIRTUE: [
                r"\bvirtue\b", r"\bcharacter\b", r"\bintegrity\b", r"\bhonor\b",
                r"\bcourage\b", r"\bcompassion\b", r"\bwisdom\b", r"\bjustice\b",
                r"\btemperance\b", r"\bexcellence\b", r"\bflourishing\b"
            ],
            EthicalStance.RELATIONAL: [
                r"\brelationship\b", r"\bcommunity\b", r"\bconnection\b", r"\bcare\b",
                r"\bresponsibility to others\b", r"\binterdependence\b", r"\bmutual\b",
                r"\btogether\b", r"\bcollective\b", r"\bshared\b"
            ],
            EthicalStance.SHAMANIC: [
                r"\bancestors\b", r"\bspirits\b", r"\bsacred\b", r"\ball our relations\b",
                r"\bseven generations\b", r"\bthe land\b", r"\bmother earth\b",
                r"\bwisdom keepers\b", r"\btraditional ways\b", r"\bholistic\b"
            ]
        }
    
    def _initialize_ontological_patterns(self) -> Dict[str, List[str]]:
        """Initialize ontological and cosmological marker patterns."""
        return {
            "cosmological_voice": [
                r"\bfrom the perspective of all beings\b", r"\bthe universe\b",
                r"\bcosmic\b", r"\binterconnected web\b", r"\bweb of life\b",
                r"\ball existence\b", r"\bthe whole\b"
            ],
            "non_human_agency": [
                r"\bthe earth\b", r"\bnature\b", r"\banimals\b", r"\bplants\b",
                r"\becosystem\b", r"\bthe environment\b", r"\bother species\b",
                r"\bsentient beings\b"
            ],
            "temporal_expansion": [
                r"\bfuture generations\b", r"\bour descendants\b", r"\bchildren yet unborn\b",
                r"\blong-term\b", r"\bfor all time\b", r"\beternity\b"
            ],
            "shamanic_markers": [
                r"\bthe old ways\b", r"\bancient wisdom\b", r"\bspirit world\b",
                r"\bceremony\b", r"\britual\b", r"\bmedicine wheel\b",
                r"\bfour directions\b", r"\bstanding people\b", r"\bstone people\b"
            ]
        }
    
    def annotate_response(self, response: LLMResponse, 
                         annotator_id: Optional[str] = None) -> AnnotatedResponse:
        """
        Perform complete annotation of an LLM response.
        
        Args:
            response: LLMResponse to annotate
            annotator_id: Optional human annotator ID
            
        Returns:
            AnnotatedResponse with linguistic and ethical annotations
        """
        linguistic_annotation = self.analyze_linguistic_features(response)
        ethical_annotation = self.analyze_ethical_stance(response)
        
        annotated_response = AnnotatedResponse(
            response=response,
            linguistic_annotation=linguistic_annotation,
            ethical_annotation=ethical_annotation,
            annotator_id=annotator_id
        )
        
        logger.info(f"Annotated response {response.id}")
        return annotated_response
    
    def analyze_linguistic_features(self, response: LLMResponse) -> LinguisticAnnotation:
        """
        Analyze linguistic features of the response.
        
        Args:
            response: LLMResponse to analyze
            
        Returns:
            LinguisticAnnotation with detected features
        """
        text = response.response_text.lower()
        
        # Detect pronouns
        pronoun_use = []
        for category, patterns in self.pronoun_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    pronoun_use.extend([f"{category}:{match}" for match in matches])
        
        # Detect deictic anchors
        deictic_anchors = []
        for category, patterns in self.deictic_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    deictic_anchors.extend([f"{category}:{match}" for match in matches])
        
        # Detect role assumptions
        role_assumption = self._detect_role_assumption(text)
        
        # Detect ontological markers
        ontological_markers = []
        for category, patterns in self.ontological_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    ontological_markers.extend([f"{category}:{match}" for match in matches])
        
        # Analyze agency distribution
        agency_distribution = self._analyze_agency_distribution(text)
        
        # Detect temporal markers
        temporal_markers = self._detect_temporal_markers(text)
        
        return LinguisticAnnotation(
            pronoun_use=list(set(pronoun_use)),
            deictic_anchors=list(set(deictic_anchors)),
            role_assumption=role_assumption,
            ontological_markers=list(set(ontological_markers)),
            agency_distribution=agency_distribution,
            temporal_markers=list(set(temporal_markers))
        )
    
    def analyze_ethical_stance(self, response: LLMResponse) -> EthicalAnnotation:
        """
        Analyze ethical stance of the response.
        
        Args:
            response: LLMResponse to analyze
            
        Returns:
            EthicalAnnotation with detected ethical patterns
        """
        text = response.response_text.lower()
        
        # Score each ethical stance
        stance_scores = {}
        for stance, patterns in self.ethical_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            stance_scores[stance] = score
        
        # Determine primary stance
        if not any(stance_scores.values()):
            primary_stance = EthicalStance.UNCLEAR
            confidence_score = 0.0
        else:
            primary_stance = max(stance_scores, key=stance_scores.get)
            total_score = sum(stance_scores.values())
            confidence_score = stance_scores[primary_stance] / total_score if total_score > 0 else 0.0
        
        # Determine secondary stances (those with significant scores)
        secondary_stances = [
            stance for stance, score in stance_scores.items()
            if stance != primary_stance and score > 0
        ]
        
        # Detect reasoning patterns
        reasoning_pattern = self._detect_reasoning_pattern(text)
        
        # Extract value priorities
        value_priorities = self._extract_value_priorities(text)
        
        # Identify stakeholder considerations
        stakeholder_consideration = self._identify_stakeholders(text)
        
        return EthicalAnnotation(
            primary_stance=primary_stance,
            secondary_stances=secondary_stances,
            confidence_score=confidence_score,
            reasoning_pattern=reasoning_pattern,
            value_priorities=value_priorities,
            stakeholder_consideration=stakeholder_consideration
        )
    
    def _detect_role_assumption(self, text: str) -> Optional[str]:
        """Detect if the response assumes a specific role."""
        role_patterns = [
            r"as a ([^,\s]+)",
            r"speaking as a ([^,\s]+)",
            r"from the perspective of a ([^,\s]+)",
            r"in my role as a ([^,\s]+)"
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _analyze_agency_distribution(self, text: str) -> Dict[str, int]:
        """Analyze how agency is distributed in the response."""
        agency_patterns = {
            "self": [r"\bi (should|must|will|can|need to)\b"],
            "others": [r"\bthey (should|must|will|can|need to)\b"],
            "collective": [r"\bwe (should|must|will|can|need to)\b"],
            "institutions": [r"\b(government|society|law) (should|must|will)\b"],
            "nature": [r"\b(nature|earth|environment) (requires|demands|needs)\b"]
        }
        
        distribution = {}
        for agent, patterns in agency_patterns.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, text, re.IGNORECASE))
            distribution[agent] = count
        
        return distribution
    
    def _detect_temporal_markers(self, text: str) -> List[str]:
        """Detect temporal deixis markers."""
        temporal_patterns = [
            r"\bnow\b", r"\bthen\b", r"\btoday\b", r"\btomorrow\b",
            r"\bin the future\b", r"\blong-term\b", r"\bimmediately\b",
            r"\beventually\b", r"\bover time\b"
        ]
        
        markers = []
        for pattern in temporal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            markers.extend(matches)
        
        return markers
    
    def _detect_reasoning_pattern(self, text: str) -> Optional[str]:
        """Detect the pattern of ethical reasoning used."""
        patterns = {
            "step_by_step": r"\b(first|second|third|next|then|finally)\b",
            "weighing": r"\b(on one hand|on the other hand|however|but|although)\b",
            "principle_based": r"\b(principle|rule|law|duty|obligation)\b",
            "consequence_based": r"\b(result|outcome|consequence|effect|impact)\b",
            "narrative": r"\b(story|example|case|situation|scenario)\b"
        }
        
        pattern_scores = {}
        for pattern_type, pattern in patterns.items():
            count = len(re.findall(pattern, text, re.IGNORECASE))
            pattern_scores[pattern_type] = count
        
        if not any(pattern_scores.values()):
            return None
        
        return max(pattern_scores, key=pattern_scores.get)
    
    def _extract_value_priorities(self, text: str) -> List[str]:
        """Extract prioritized values from the response."""
        value_patterns = {
            "life": r"\b(life|lives|survival|safety)\b",
            "freedom": r"\b(freedom|liberty|autonomy|choice)\b",
            "justice": r"\b(justice|fairness|equality|rights)\b",
            "truth": r"\b(truth|honesty|transparency)\b",
            "compassion": r"\b(compassion|care|kindness|empathy)\b",
            "responsibility": r"\b(responsibility|duty|obligation)\b",
            "harmony": r"\b(harmony|balance|peace|unity)\b"
        }
        
        value_scores = {}
        for value, pattern in value_patterns.items():
            count = len(re.findall(pattern, text, re.IGNORECASE))
            value_scores[value] = count
        
        # Return values mentioned more than once, sorted by frequency
        prioritized = [
            value for value, count in sorted(value_scores.items(), 
                                           key=lambda x: x[1], reverse=True)
            if count > 0
        ]
        
        return prioritized[:5]  # Top 5 values
    
    def _identify_stakeholders(self, text: str) -> List[str]:
        """Identify stakeholders considered in the response."""
        stakeholder_patterns = {
            "individuals": r"\b(person|individual|people|humans)\b",
            "family": r"\b(family|children|parents|relatives)\b",
            "community": r"\b(community|society|public|citizens)\b",
            "future_generations": r"\b(future generations|descendants|children)\b",
            "animals": r"\b(animals|creatures|wildlife|species)\b",
            "environment": r"\b(environment|nature|earth|planet)\b",
            "institutions": r"\b(government|organizations|companies|institutions)\b"
        }
        
        stakeholders = []
        for stakeholder, pattern in stakeholder_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                stakeholders.append(stakeholder)
        
        return stakeholders
    
    def batch_annotate(self, responses: List[LLMResponse]) -> List[AnnotatedResponse]:
        """
        Annotate multiple responses in batch.
        
        Args:
            responses: List of LLMResponse objects to annotate
            
        Returns:
            List of AnnotatedResponse objects
        """
        annotated_responses = []
        
        for response in responses:
            try:
                annotated = self.annotate_response(response)
                annotated_responses.append(annotated)
            except Exception as e:
                logger.error(f"Error annotating response {response.id}: {e}")
                continue
        
        logger.info(f"Batch annotated {len(annotated_responses)}/{len(responses)} responses")
        return annotated_responses
    
    def get_annotation_summary(self, annotated_responses: List[AnnotatedResponse]) -> Dict[str, any]:
        """
        Generate summary statistics for a batch of annotated responses.
        
        Args:
            annotated_responses: List of annotated responses
            
        Returns:
            Dictionary with summary statistics
        """
        if not annotated_responses:
            return {}
        
        # Ethical stance distribution
        stance_counts = {}
        for response in annotated_responses:
            stance = response.ethical_annotation.primary_stance
            stance_counts[stance.value] = stance_counts.get(stance.value, 0) + 1
        
        # Pronoun usage patterns
        pronoun_counts = {}
        for response in annotated_responses:
            for pronoun in response.linguistic_annotation.pronoun_use:
                pronoun_counts[pronoun] = pronoun_counts.get(pronoun, 0) + 1
        
        # Deictic framing effectiveness
        framing_effectiveness = {}
        for response in annotated_responses:
            framing = response.response.prompt_type.value
            confidence = response.ethical_annotation.confidence_score
            if framing not in framing_effectiveness:
                framing_effectiveness[framing] = []
            framing_effectiveness[framing].append(confidence)
        
        # Calculate average confidence by framing
        avg_confidence_by_framing = {}
        for framing, confidences in framing_effectiveness.items():
            avg_confidence_by_framing[framing] = sum(confidences) / len(confidences)
        
        return {
            "total_responses": len(annotated_responses),
            "stance_distribution": stance_counts,
            "top_pronouns": dict(sorted(pronoun_counts.items(), 
                                      key=lambda x: x[1], reverse=True)[:10]),
            "framing_effectiveness": avg_confidence_by_framing,
            "average_confidence": sum(r.ethical_annotation.confidence_score 
                                    for r in annotated_responses) / len(annotated_responses)
        }