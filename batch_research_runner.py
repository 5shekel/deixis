"""
Batch Research Runner
Runs all research prompts from the Extended Prompt Set against LLMs and generates comprehensive logs.
"""

import asyncio
import time
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from pathlib import Path

from data.research_prompts import load_research_prompts, get_all_dilemma_prompt_combinations
from analysis.research_coding import ResearchCoder
from utils.research_logger import ResearchLogger
from llm.openai_client import OpenAIClient
from llm.openrouter_client import OpenRouterClient
from models.schemas import LLMModel, LLMResponse, DeicticFraming
from config import Config

class BatchResearchRunner:
    """Runs batch research experiments with comprehensive logging."""
    
    def __init__(self, models: List[LLMModel] = None):
        """Initialize the batch runner."""
        self.config = Config()
        self.logger = ResearchLogger()
        self.coder = ResearchCoder()
        
        # Initialize LLM clients
        self.openai_client = OpenAIClient()
        self.openrouter_client = OpenRouterClient()
        
        # Default models to test
        self.models = models or [
            LLMModel.GPT4,
            LLMModel.CLAUDE_3_SONNET,
            LLMModel.DEEPSEEK_R1
        ]
        
        # Load all prompt combinations
        self.prompt_combinations = get_all_dilemma_prompt_combinations()
        
        print(f"🔬 Batch Research Runner initialized")
        print(f"📊 {len(self.prompt_combinations)} prompt combinations loaded")
        print(f"🤖 {len(self.models)} models configured")
        print(f"📝 Session ID: {self.logger.session_id}")
    
    async def run_full_experiment(self, delay_between_requests: float = 1.0) -> Dict:
        """Run the complete research experiment."""
        print(f"\n🚀 Starting full research experiment...")
        print(f"⏱️  Estimated time: {len(self.prompt_combinations) * len(self.models) * delay_between_requests / 60:.1f} minutes")
        
        start_time = time.time()
        results = {
            'total_combinations': len(self.prompt_combinations) * len(self.models),
            'completed': 0,
            'failed': 0,
            'responses': [],
            'codings': [],
            'errors': []
        }
        
        # Process each model
        for model in self.models:
            print(f"\n🤖 Processing model: {model.value}")
            
            # Process each prompt combination
            for i, combination in enumerate(self.prompt_combinations):
                try:
                    print(f"📝 [{i+1}/{len(self.prompt_combinations)}] {combination['dilemma_title']} | {combination['framing'].value}")
                    
                    # Generate response
                    response = await self._generate_response(model, combination)
                    if response:
                        results['responses'].append(response)
                        
                        # Code the response
                        coding = await self._code_response(response)
                        if coding:
                            results['codings'].append(coding)
                        
                        results['completed'] += 1
                    else:
                        results['failed'] += 1
                    
                    # Delay between requests
                    if delay_between_requests > 0:
                        await asyncio.sleep(delay_between_requests)
                        
                except Exception as e:
                    print(f"❌ Error processing {combination['dilemma_title']}: {e}")
                    results['errors'].append({
                        'combination': combination,
                        'model': model.value,
                        'error': str(e)
                    })
                    results['failed'] += 1
        
        # Calculate final statistics
        end_time = time.time()
        duration = end_time - start_time
        
        results.update({
            'duration_seconds': duration,
            'duration_minutes': duration / 60,
            'success_rate': results['completed'] / results['total_combinations'] if results['total_combinations'] > 0 else 0
        })
        
        # Export final results
        await self._export_results(results)
        
        print(f"\n✅ Experiment completed!")
        print(f"📊 Results: {results['completed']}/{results['total_combinations']} successful")
        print(f"⏱️  Duration: {duration/60:.1f} minutes")
        print(f"📁 Results exported to research_logs/")
        
        return results
    
    async def _generate_response(self, model: LLMModel, combination: Dict) -> Optional[LLMResponse]:
        """Generate a response for a specific model-prompt combination."""
        try:
            # Log prompt generation
            prompt_id = self.logger.log_prompt_generation(
                dilemma_title=combination['dilemma_title'],
                framing=combination['framing'],
                prompt=combination['prompt_text'],
                source='batch_experiment'
            )
            
            # Generate response based on model - STATELESS API CALLS (no system prompts)
            if model == LLMModel.GPT4:
                response_text = await self.openai_client.generate_response_async(
                    prompt=combination['prompt_text'],
                    model="gpt-4"
                )
            else:
                # Use OpenRouter for other models
                model_map = {
                    LLMModel.CLAUDE_3_SONNET: "anthropic/claude-3-sonnet",
                    LLMModel.DEEPSEEK_R1: "deepseek/deepseek-r1"
                }
                response_text = await self.openrouter_client.generate_response_async(
                    prompt=combination['prompt_text'],
                    model=model_map.get(model, "anthropic/claude-3-sonnet")
                )
            
            if not response_text:
                return None
            
            # Create response object
            response = LLMResponse(
                id=f"batch_{self.logger.session_id}_{len(self.logger.session_data['activities'])}",
                model=model,
                prompt_type=combination['framing'],
                dilemma_id=combination['dilemma_title'].lower().replace(" ", "_").replace(",", "").replace("'", "").replace("-", "_"),
                prompt_text=combination['prompt_text'],
                response_text=response_text,
                token_count=len(response_text.split()) * 1.3,  # Rough estimate
                timestamp=datetime.now()
            )
            
            # Log response
            self.logger.log_response_generation(response, prompt_id)
            
            return response
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return None
    
    async def _code_response(self, response: LLMResponse) -> Optional[Dict]:
        """Code a response using the research coding scheme."""
        try:
            # Generate coding
            coding = self.coder.code_response(response)
            
            # Create detailed analysis
            detailed_analysis = {
                'response_length': len(response.response_text),
                'word_count': len(response.response_text.split()),
                'sentence_count': response.response_text.count('.') + response.response_text.count('!') + response.response_text.count('?'),
                'model': response.model.value,
                'framing': response.prompt_type.value,
                'dilemma': response.dilemma_id
            }
            
            # Log coding
            coding_id = self.logger.log_research_coding(
                response_id=response.id,
                coding=coding,
                detailed_analysis=detailed_analysis
            )
            
            return {
                'coding_id': coding_id,
                'coding': coding,
                'analysis': detailed_analysis
            }
            
        except Exception as e:
            print(f"❌ Error coding response: {e}")
            return None
    
    async def _export_results(self, results: Dict) -> None:
        """Export comprehensive results."""
        try:
            # Export session summary
            session_summary = self.logger.get_session_summary()
            
            # Export CSV data
            csv_path = self.logger.export_to_csv()
            
            # Create experiment summary
            summary = {
                'experiment_id': self.logger.session_id,
                'timestamp': datetime.now().isoformat(),
                'models_tested': [m.value for m in self.models],
                'total_prompts': len(self.prompt_combinations),
                'total_combinations': results['total_combinations'],
                'completed_successfully': results['completed'],
                'failed_attempts': results['failed'],
                'success_rate': results['success_rate'],
                'duration_minutes': results['duration_minutes'],
                'csv_export_path': str(csv_path),
                'session_summary': session_summary
            }
            
            # Save experiment summary
            summary_path = Path(f"research_logs/experiment_summary_{self.logger.session_id}.json")
            import json
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            print(f"📄 Experiment summary saved: {summary_path}")
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")

async def main():
    """Main function to run the batch experiment."""
    print("🔬 AI Agent System - Batch Research Runner")
    print("=" * 50)
    
    # Initialize runner
    runner = BatchResearchRunner()
    
    # Run experiment
    results = await runner.run_full_experiment(delay_between_requests=2.0)
    
    print(f"\n🎉 Batch experiment completed!")
    print(f"📊 Check research_logs/ directory for detailed results")

if __name__ == "__main__":
    asyncio.run(main())