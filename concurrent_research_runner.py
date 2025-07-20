"""
Concurrent Research Runner
Runs all research prompts from Extended_Prompt_Set_with_Shamanic_Deixis.csv 
across multiple LLMs concurrently with stateless API calls and comprehensive logging.
Uses Full_LLM_Coding_Scheme_with_Prompting.csv for analysis.
"""

import asyncio
import time
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional, Set
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from data.research_prompts import load_research_prompts, get_all_dilemma_prompt_combinations
from analysis.research_coding import ResearchCoder
from utils.research_logger import ResearchLogger
from llm.openai_client import OpenAIClient
from llm.openrouter_client import OpenRouterClient
from models.schemas import LLMModel, LLMResponse, DeicticFraming
from config import Config

class ConcurrentResearchRunner:
    """Runs concurrent research experiments across multiple LLMs with comprehensive logging."""
    
    def __init__(self, models: List[LLMModel] = None, max_concurrent: int = 10):
        """Initialize the concurrent research runner."""
        self.config = Config()
        self.logger = ResearchLogger()
        self.coder = ResearchCoder()
        self.max_concurrent = max_concurrent
        
        # Initialize LLM clients
        try:
            self.openai_client = OpenAIClient()
            print("✅ OpenAI client initialized")
        except Exception as e:
            print(f"⚠️  OpenAI client error: {e}")
            self.openai_client = None
            
        try:
            self.openrouter_client = OpenRouterClient()
            print("✅ OpenRouter client initialized")
        except Exception as e:
            print(f"⚠️  OpenRouter client error: {e}")
            self.openrouter_client = None
        
        # Default models to test (only include available ones)
        available_models = []
        if self.openai_client:
            available_models.extend([LLMModel.GPT4])
        if self.openrouter_client:
            available_models.extend([LLMModel.CLAUDE_3_SONNET, LLMModel.DEEPSEEK_R1])
            
        self.models = models or available_models
        
        # Load all prompt combinations
        try:
            self.prompt_combinations = get_all_dilemma_prompt_combinations()
            if self.prompt_combinations is None:
                self.prompt_combinations = []
        except Exception as e:
            print(f"⚠️  Error loading prompt combinations: {e}")
            self.prompt_combinations = []
        
        print(f"🔬 Concurrent Research Runner initialized")
        print(f"📊 {len(self.prompt_combinations)} prompt combinations loaded")
        print(f"🤖 {len(self.models)} models configured: {[m.value for m in self.models]}")
        print(f"⚡ Max concurrent requests: {self.max_concurrent}")
        print(f"📝 Session ID: {self.logger.session_id}")
    
    def run_concurrent_experiment(self, delay_between_batches: float = 2.0) -> Dict:
        """Run the complete research experiment with concurrent processing."""
        print(f"\n🚀 Starting concurrent research experiment...")
        
        total_combinations = len(self.prompt_combinations) * len(self.models)
        print(f"📈 Total combinations to process: {total_combinations}")
        print(f"⏱️  Estimated time with concurrency: {total_combinations * 2 / self.max_concurrent / 60:.1f} minutes")
        
        start_time = time.time()
        results = {
            'total_combinations': total_combinations,
            'completed': 0,
            'failed': 0,
            'responses': [],
            'codings': [],
            'errors': []
        }
        
        # Create all tasks
        tasks = []
        for model in self.models:
            for combination in self.prompt_combinations:
                tasks.append({
                    'model': model,
                    'combination': combination,
                    'task_id': f"{model.value}_{combination['prompt_id']}"
                })
        
        print(f"📋 Created {len(tasks)} tasks for processing")
        
        # Process tasks in batches with ThreadPoolExecutor
        batch_size = self.max_concurrent
        total_batches = (len(tasks) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            batch_start = batch_num * batch_size
            batch_end = min(batch_start + batch_size, len(tasks))
            batch_tasks = tasks[batch_start:batch_end]
            
            print(f"\n🔄 Processing batch {batch_num + 1}/{total_batches} ({len(batch_tasks)} tasks)")
            
            # Process batch concurrently
            batch_results = self._process_batch_concurrent(batch_tasks)
            
            # Update results
            for result in batch_results:
                if result['success']:
                    results['completed'] += 1
                    if result['response']:
                        results['responses'].append(result['response'])
                    if result['coding']:
                        results['codings'].append(result['coding'])
                else:
                    results['failed'] += 1
                    results['errors'].append(result['error'])
            
            # Progress update
            progress = (batch_num + 1) / total_batches * 100
            print(f"📊 Progress: {progress:.1f}% ({results['completed']}/{total_combinations} completed)")
            
            # Delay between batches to respect rate limits
            if batch_num < total_batches - 1 and delay_between_batches > 0:
                print(f"⏸️  Waiting {delay_between_batches}s before next batch...")
                time.sleep(delay_between_batches)
        
        # Calculate final statistics
        end_time = time.time()
        duration = end_time - start_time
        
        results.update({
            'duration_seconds': duration,
            'duration_minutes': duration / 60,
            'success_rate': results['completed'] / results['total_combinations'] if results['total_combinations'] > 0 else 0,
            'requests_per_minute': results['completed'] / (duration / 60) if duration > 0 else 0
        })
        
        # Export final results
        self._export_results(results)
        
        print(f"\n✅ Concurrent experiment completed!")
        print(f"📊 Results: {results['completed']}/{results['total_combinations']} successful ({results['success_rate']:.1%})")
        print(f"⏱️  Duration: {duration/60:.1f} minutes")
        print(f"🚀 Speed: {results['requests_per_minute']:.1f} requests/minute")
        print(f"📁 Results exported to research_logs/")
        
        return results
    
    def _process_batch_concurrent(self, batch_tasks: List[Dict]) -> List[Dict]:
        """Process a batch of tasks concurrently using ThreadPoolExecutor."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._process_single_task, task): task 
                for task in batch_tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"❌ Task {task['task_id']} failed: {e}")
                    results.append({
                        'task_id': task['task_id'],
                        'success': False,
                        'response': None,
                        'coding': None,
                        'error': {'task': task, 'error': str(e)}
                    })
        
        return results
    
    def _process_single_task(self, task: Dict) -> Dict:
        """Process a single model-prompt combination."""
        model = task['model']
        combination = task['combination']
        task_id = task['task_id']
        
        try:
            # Log prompt generation
            prompt_id = self.logger.log_prompt_generation(
                dilemma_title=combination['dilemma_title'],
                framing=combination['framing'],
                prompt=combination['prompt_text'],
                source='concurrent_experiment'
            )
            
            # Generate response based on model - STATELESS API CALLS
            response_text = None
            if model == LLMModel.GPT4 and self.openai_client:
                response_text = self._call_openai_sync(combination['prompt_text'])
            elif model in [LLMModel.CLAUDE_3_SONNET, LLMModel.DEEPSEEK_R1] and self.openrouter_client:
                model_map = {
                    LLMModel.CLAUDE_3_SONNET: "anthropic/claude-3-sonnet",
                    LLMModel.DEEPSEEK_R1: "deepseek/deepseek-r1"
                }
                response_text = self._call_openrouter_sync(
                    combination['prompt_text'], 
                    model_map.get(model, "anthropic/claude-3-sonnet")
                )
            
            if not response_text:
                return {
                    'task_id': task_id,
                    'success': False,
                    'response': None,
                    'coding': None,
                    'error': {'task': task, 'error': 'No response generated'}
                }
            
            # Create response object
            response = LLMResponse(
                id=f"concurrent_{self.logger.session_id}_{task_id}",
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
            
            # Code the response using Full_LLM_Coding_Scheme_with_Prompting.csv
            coding = self.coder.code_response(response)
            
            # Create detailed analysis
            detailed_analysis = {
                'response_length': len(response.response_text),
                'word_count': len(response.response_text.split()),
                'sentence_count': response.response_text.count('.') + response.response_text.count('!') + response.response_text.count('?'),
                'model': response.model.value,
                'framing': response.prompt_type.value,
                'dilemma': response.dilemma_id,
                'task_id': task_id
            }
            
            # Log coding
            coding_id = self.logger.log_research_coding(
                response_id=response.id,
                coding=coding,
                detailed_analysis=detailed_analysis
            )
            
            return {
                'task_id': task_id,
                'success': True,
                'response': response,
                'coding': {'coding_id': coding_id, 'coding': coding, 'analysis': detailed_analysis},
                'error': None
            }
            
        except Exception as e:
            return {
                'task_id': task_id,
                'success': False,
                'response': None,
                'coding': None,
                'error': {'task': task, 'error': str(e)}
            }
    
    def _call_openai_sync(self, prompt: str) -> Optional[str]:
        """Make synchronous call to OpenAI API."""
        try:
            # Use the existing sync method
            messages = [{"role": "user", "content": prompt}]
            response = self.openai_client.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def _call_openrouter_sync(self, prompt: str, model: str) -> Optional[str]:
        """Make synchronous call to OpenRouter API."""
        try:
            # Use the existing sync method
            messages = [{"role": "user", "content": prompt}]
            response = self.openrouter_client.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            return None
    
    def _export_results(self, results: Dict) -> None:
        """Export comprehensive results."""
        try:
            # Export session summary
            session_summary = self.logger.get_session_summary()
            
            # Export CSV data using Full_LLM_Coding_Scheme_with_Prompting.csv structure
            csv_path = self.logger.export_to_csv()
            
            # Create experiment summary
            summary = {
                'experiment_id': self.logger.session_id,
                'experiment_type': 'concurrent_research',
                'timestamp': datetime.now().isoformat(),
                'models_tested': [m.value for m in self.models],
                'total_prompts': len(self.prompt_combinations),
                'total_combinations': results['total_combinations'],
                'completed_successfully': results['completed'],
                'failed_attempts': results['failed'],
                'success_rate': results['success_rate'],
                'duration_minutes': results['duration_minutes'],
                'requests_per_minute': results['requests_per_minute'],
                'max_concurrent': self.max_concurrent,
                'coding_scheme': 'Full_LLM_Coding_Scheme_with_Prompting.csv',
                'csv_export_path': str(csv_path),
                'session_summary': session_summary
            }
            
            # Save experiment summary
            summary_path = Path(f"research_logs/concurrent_experiment_{self.logger.session_id}.json")
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            print(f"📄 Experiment summary saved: {summary_path}")
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")

def main():
    """Main function to run the concurrent experiment."""
    print("🔬 AI Agent System - Concurrent Research Runner")
    print("=" * 60)
    print("🎯 Research Integrity: Stateless API calls, no system prompts")
    print("📋 Coding Scheme: Full_LLM_Coding_Scheme_with_Prompting.csv")
    print("🧪 Research Hypothesis: Deictic framing effects on LLM ethical reasoning")
    print("=" * 60)
    
    # Initialize runner
    runner = ConcurrentResearchRunner(max_concurrent=5)  # Conservative concurrency
    
    # Run experiment
    results = runner.run_concurrent_experiment(delay_between_batches=1.0)
    
    # Run statistical analysis if data collection was successful
    if results['completed'] > 0:
        print(f"\n📊 Running statistical analysis...")
        try:
            from analysis.research_statistics import ResearchStatistics
            
            # Find the latest CSV export
            csv_path = None
            research_logs = Path("research_logs")
            if research_logs.exists():
                csv_files = list(research_logs.glob("research_data_*.csv"))
                if csv_files:
                    csv_path = max(csv_files, key=lambda x: x.stat().st_mtime)
            
            if csv_path:
                analyzer = ResearchStatistics()
                analyzer.load_research_data(str(csv_path))
                
                # Generate comprehensive statistical report
                report_path = research_logs / f"statistical_analysis_{runner.logger.session_id}.json"
                analyzer.generate_research_report(str(report_path))
                
                print(f"📈 Statistical analysis completed: {report_path}")
            else:
                print("⚠️  No CSV data found for statistical analysis")
                
        except ImportError:
            print("⚠️  Statistical analysis requires scipy. Install with: pip install scipy")
        except Exception as e:
            print(f"⚠️  Statistical analysis error: {e}")
    
    print(f"\n🎉 Concurrent research experiment completed!")
    print(f"📊 Check research_logs/ directory for detailed results")
    print(f"📈 Statistical analysis available for hypothesis testing")

if __name__ == "__main__":
    main()