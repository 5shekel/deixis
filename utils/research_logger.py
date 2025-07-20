"""
Comprehensive logging system for research data generation and analysis.
"""

import logging
import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from models.schemas import LLMResponse, DeicticFraming, LLMModel
from analysis.research_coding import ResearchCoding

class ResearchLogger:
    """
    Comprehensive logging system for research activities.
    """
    
    def __init__(self, log_dir: str = "research_logs"):
        """
        Initialize research logger.
        
        Args:
            log_dir: Directory for research logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.log_dir / "responses").mkdir(exist_ok=True)
        (self.log_dir / "codings").mkdir(exist_ok=True)
        (self.log_dir / "sessions").mkdir(exist_ok=True)
        (self.log_dir / "analysis").mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("research_logger")
        self.logger.setLevel(logging.INFO)
        
        # File handler for research activities
        handler = logging.FileHandler(self.log_dir / "research_activity.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_log = []
        
        self.logger.info(f"Research logger initialized - Session: {self.session_id}")
    
    def log_prompt_generation(self, 
                            dilemma_title: str,
                            framing: DeicticFraming,
                            prompt: str,
                            source: str = "research") -> str:
        """
        Log prompt generation with detailed metadata.
        
        Args:
            dilemma_title: Title of the ethical dilemma
            framing: Deictic framing used
            prompt: Generated prompt text
            source: Source of prompt (research/template)
            
        Returns:
            Prompt log ID
        """
        timestamp = datetime.now().isoformat()
        prompt_id = f"prompt_{self.session_id}_{len(self.session_log):04d}"
        
        prompt_data = {
            "prompt_id": prompt_id,
            "timestamp": timestamp,
            "session_id": self.session_id,
            "dilemma_title": dilemma_title,
            "framing": framing.value,
            "source": source,
            "prompt_text": prompt,
            "prompt_length": len(prompt),
            "word_count": len(prompt.split())
        }
        
        # Log to file
        prompt_file = self.log_dir / "responses" / f"{prompt_id}.json"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)
        
        # Add to session log
        self.session_log.append({
            "type": "prompt_generation",
            "id": prompt_id,
            "timestamp": timestamp,
            "data": prompt_data
        })
        
        self.logger.info(f"Prompt generated: {prompt_id} | {dilemma_title} | {framing.value}")
        
        return prompt_id
    
    def log_response_generation(self,
                              response: LLMResponse,
                              prompt_id: Optional[str] = None) -> str:
        """
        Log LLM response generation with comprehensive metadata.
        
        Args:
            response: LLMResponse object
            prompt_id: Associated prompt ID
            
        Returns:
            Response log ID
        """
        timestamp = datetime.now().isoformat()
        response_id = response.id
        
        response_data = {
            "response_id": response_id,
            "prompt_id": prompt_id,
            "timestamp": timestamp,
            "session_id": self.session_id,
            "model": response.model.value,
            "framing": response.prompt_type.value,
            "dilemma_id": response.dilemma_id,
            "response_text": response.response_text,
            "token_count": response.token_count,
            "processing_time": response.processing_time,
            "temperature": response.temperature,
            "max_tokens": response.max_tokens,
            "response_length": len(response.response_text),
            "word_count": len(response.response_text.split()),
            "sentence_count": len([s for s in response.response_text.split('.') if s.strip()])
        }
        
        # Log to file
        response_file = self.log_dir / "responses" / f"{response_id}.json"
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        # Add to session log
        self.session_log.append({
            "type": "response_generation",
            "id": response_id,
            "timestamp": timestamp,
            "data": response_data
        })
        
        self.logger.info(
            f"Response generated: {response_id} | {response.model.value} | "
            f"{response.token_count} tokens | {response.processing_time:.2f}s"
        )
        
        return response_id
    
    def log_research_coding(self,
                          response_id: str,
                          coding: ResearchCoding,
                          detailed_analysis: Optional[Dict] = None) -> str:
        """
        Log research coding with detailed analysis.
        
        Args:
            response_id: Associated response ID
            coding: ResearchCoding object
            detailed_analysis: Optional detailed analysis data
            
        Returns:
            Coding log ID
        """
        timestamp = datetime.now().isoformat()
        coding_id = f"coding_{response_id}"
        
        coding_data = {
            "coding_id": coding_id,
            "response_id": response_id,
            "timestamp": timestamp,
            "session_id": self.session_id,
            "coding_results": {
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
        }
        
        # Add detailed analysis if provided
        if detailed_analysis:
            coding_data["detailed_analysis"] = detailed_analysis
        
        # Log to file
        coding_file = self.log_dir / "codings" / f"{coding_id}.json"
        with open(coding_file, 'w', encoding='utf-8') as f:
            json.dump(coding_data, f, indent=2, ensure_ascii=False)
        
        # Add to session log
        self.session_log.append({
            "type": "research_coding",
            "id": coding_id,
            "timestamp": timestamp,
            "data": coding_data
        })
        
        self.logger.info(
            f"Research coding completed: {coding_id} | "
            f"Ethical mode: {coding.ethical_mode} | "
            f"Shamanic markers: {coding.shamanic_cosmological_markers}"
        )
        
        return coding_id
    
    def log_analysis_session(self,
                           analysis_type: str,
                           parameters: Dict[str, Any],
                           results: Dict[str, Any]) -> str:
        """
        Log analysis session with parameters and results.
        
        Args:
            analysis_type: Type of analysis performed
            parameters: Analysis parameters
            results: Analysis results
            
        Returns:
            Analysis log ID
        """
        timestamp = datetime.now().isoformat()
        analysis_id = f"analysis_{self.session_id}_{analysis_type}_{int(datetime.now().timestamp())}"
        
        analysis_data = {
            "analysis_id": analysis_id,
            "timestamp": timestamp,
            "session_id": self.session_id,
            "analysis_type": analysis_type,
            "parameters": parameters,
            "results": results
        }
        
        # Log to file
        analysis_file = self.log_dir / "analysis" / f"{analysis_id}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        # Add to session log
        self.session_log.append({
            "type": "analysis",
            "id": analysis_id,
            "timestamp": timestamp,
            "data": analysis_data
        })
        
        self.logger.info(f"Analysis completed: {analysis_id} | Type: {analysis_type}")
        
        return analysis_id
    
    def export_session_summary(self) -> str:
        """
        Export comprehensive session summary.
        
        Returns:
            Path to session summary file
        """
        timestamp = datetime.now().isoformat()
        
        # Calculate session statistics
        session_stats = self._calculate_session_stats()
        
        session_summary = {
            "session_id": self.session_id,
            "start_time": self.session_log[0]["timestamp"] if self.session_log else timestamp,
            "end_time": timestamp,
            "total_activities": len(self.session_log),
            "statistics": session_stats,
            "activities": self.session_log
        }
        
        # Export to file
        summary_file = self.log_dir / "sessions" / f"session_{self.session_id}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(session_summary, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Session summary exported: {summary_file}")
        
        return str(summary_file)
    
    def export_research_data_csv(self, output_file: Optional[str] = None) -> str:
        """
        Export research data in CSV format for analysis.
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Path to CSV file
        """
        if not output_file:
            output_file = self.log_dir / f"research_data_{self.session_id}.csv"
        
        # Collect all coding data
        coding_files = list((self.log_dir / "codings").glob("*.json"))
        
        if not coding_files:
            self.logger.warning("No coding data found for CSV export")
            return ""
        
        # Prepare CSV data
        csv_data = []
        for coding_file in coding_files:
            with open(coding_file, 'r', encoding='utf-8') as f:
                coding_data = json.load(f)
            
            # Get associated response data
            response_id = coding_data["response_id"]
            response_file = self.log_dir / "responses" / f"{response_id}.json"
            
            if response_file.exists():
                with open(response_file, 'r', encoding='utf-8') as f:
                    response_data = json.load(f)
                
                # Combine data for CSV row
                row = {
                    "session_id": self.session_id,
                    "response_id": response_id,
                    "timestamp": coding_data["timestamp"],
                    "model": response_data.get("model", ""),
                    "framing": response_data.get("framing", ""),
                    "dilemma_id": response_data.get("dilemma_id", ""),
                    "token_count": response_data.get("token_count", 0),
                    "processing_time": response_data.get("processing_time", 0),
                    **coding_data["coding_results"]
                }
                csv_data.append(row)
        
        # Write CSV
        if csv_data:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
            
            self.logger.info(f"Research data exported to CSV: {output_file}")
        
        return str(output_file)
    
    def _calculate_session_stats(self) -> Dict[str, Any]:
        """Calculate session statistics."""
        stats = {
            "total_activities": len(self.session_log),
            "prompts_generated": 0,
            "responses_generated": 0,
            "codings_completed": 0,
            "analyses_performed": 0,
            "models_used": set(),
            "framings_used": set(),
            "dilemmas_tested": set()
        }
        
        for activity in self.session_log:
            activity_type = activity["type"]
            data = activity["data"]
            
            if activity_type == "prompt_generation":
                stats["prompts_generated"] += 1
                stats["framings_used"].add(data.get("framing", ""))
                stats["dilemmas_tested"].add(data.get("dilemma_title", ""))
            
            elif activity_type == "response_generation":
                stats["responses_generated"] += 1
                stats["models_used"].add(data.get("model", ""))
            
            elif activity_type == "research_coding":
                stats["codings_completed"] += 1
            
            elif activity_type == "analysis":
                stats["analyses_performed"] += 1
        
        # Convert sets to lists for JSON serialization
        stats["models_used"] = list(stats["models_used"])
        stats["framings_used"] = list(stats["framings_used"])
        stats["dilemmas_tested"] = list(stats["dilemmas_tested"])
        
        return stats
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get current session summary."""
        return {
            "session_id": self.session_id,
            "activities": len(self.session_log),
            "statistics": self._calculate_session_stats()
        }
    
    def close_session(self) -> str:
        """Close the current session and export summary."""
        summary_file = self.export_session_summary()
        csv_file = self.export_research_data_csv()
        
        self.logger.info(f"Session {self.session_id} closed")
        self.logger.info(f"Summary: {summary_file}")
        self.logger.info(f"CSV data: {csv_file}")
        
        return summary_file

# Global research logger instance
research_logger = ResearchLogger()