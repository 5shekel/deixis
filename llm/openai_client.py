"""
OpenAI GPT-4 integration module for the Deixis AI Agent system.
"""

import logging
import time
from typing import Optional, Dict, Any
from openai import OpenAI
from models.schemas import LLMResponse, LLMModel, DeicticFraming
from config import Config

logger = logging.getLogger(__name__)

class OpenAIClient:
    """
    Client for interacting with OpenAI's GPT-4 API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, will use Config.OPENAI_API_KEY
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.default_model = LLMModel.GPT4_TURBO
        self.default_temperature = Config.TEMPERATURE
        self.default_max_tokens = Config.MAX_TOKENS
        
        logger.info("OpenAI client initialized")
    
    def generate_response(self,
                         prompt: str,
                         dilemma_id: str,
                         prompt_type: DeicticFraming,
                         model: LLMModel = None,
                         temperature: float = None,
                         max_tokens: int = None,
                         **kwargs) -> LLMResponse:
        """
        Generate a response from OpenAI GPT-4.
        
        Args:
            prompt: The formatted prompt to send
            dilemma_id: ID of the ethical dilemma
            prompt_type: Type of deictic framing used
            model: LLM model to use (defaults to GPT-4 Turbo)
            temperature: Temperature setting (0.0-2.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters for the API call
            
        Returns:
            LLMResponse object with the generated response and metadata
        """
        # Set defaults
        model = model or self.default_model
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens or self.default_max_tokens
        
        # Validate model
        if model not in [LLMModel.GPT4, LLMModel.GPT4_TURBO]:
            raise ValueError(f"Unsupported model for OpenAI client: {model}")
        
        start_time = time.time()
        
        try:
            # Prepare the API call - NO SYSTEM PROMPT for research integrity
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=model.value,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            processing_time = time.time() - start_time
            
            # Extract response data
            response_text = response.choices[0].message.content
            token_count = response.usage.completion_tokens if response.usage else 0
            
            # Create LLMResponse object
            llm_response = LLMResponse(
                id=f"{dilemma_id}_{prompt_type.value}_{int(time.time())}",
                model=model,
                prompt_type=prompt_type,
                dilemma_id=dilemma_id,
                prompt_text=prompt,
                response_text=response_text,
                token_count=token_count,
                processing_time=processing_time,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            logger.info(f"Generated response for {dilemma_id} with {prompt_type.value} framing")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_response_async(self,
                                    prompt: str,
                                    model: str = "gpt-4",
                                    temperature: float = 0.7,
                                    max_tokens: int = 2000) -> Optional[str]:
        """
        Generate a response using OpenAI's API asynchronously.
        
        Args:
            prompt: The input prompt
            model: The model to use (default: gpt-4)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text or None if failed
        """
        import asyncio
        
        try:
            # Prepare the API call - NO SYSTEM PROMPT for research integrity
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Run the synchronous call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating async OpenAI response: {e}")
            return None
            logger.error(f"Error generating response: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test the connection to OpenAI API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            logger.info("OpenAI API connection test successful")
            return True
        except Exception as e:
            logger.error(f"OpenAI API connection test failed: {e}")
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available OpenAI models.
        
        Returns:
            List of available model names
        """
        try:
            models = self.client.models.list()
            openai_models = [model.id for model in models.data if 'gpt' in model.id]
            logger.info(f"Retrieved {len(openai_models)} OpenAI models")
            return openai_models
        except Exception as e:
            logger.error(f"Error retrieving models: {e}")
            return []
    
    def estimate_cost(self, prompt: str, max_tokens: int = None) -> Dict[str, float]:
        """
        Estimate the cost of a prompt based on token count.
        
        Args:
            prompt: The prompt text
            max_tokens: Maximum response tokens
            
        Returns:
            Dictionary with cost estimates for different models
        """
        max_tokens = max_tokens or self.default_max_tokens
        
        # Rough token estimation (1 token ≈ 4 characters)
        prompt_tokens = len(prompt) // 4
        total_tokens = prompt_tokens + max_tokens
        
        # Pricing as of 2024 (per 1K tokens)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
        
        estimates = {}
        for model, prices in pricing.items():
            input_cost = (prompt_tokens / 1000) * prices["input"]
            output_cost = (max_tokens / 1000) * prices["output"]
            estimates[model] = {
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": input_cost + output_cost,
                "prompt_tokens": prompt_tokens,
                "max_response_tokens": max_tokens
            }
        
        return estimates
    
    def batch_generate(self,
                      prompts: Dict[str, str],
                      dilemma_ids: Dict[str, str],
                      prompt_types: Dict[str, DeicticFraming],
                      model: LLMModel = None,
                      temperature: float = None,
                      max_tokens: int = None,
                      delay_between_calls: float = 1.0) -> Dict[str, LLMResponse]:
        """
        Generate responses for multiple prompts in batch.
        
        Args:
            prompts: Dictionary mapping prompt_id to prompt text
            dilemma_ids: Dictionary mapping prompt_id to dilemma_id
            prompt_types: Dictionary mapping prompt_id to DeicticFraming
            model: LLM model to use
            temperature: Temperature setting
            max_tokens: Maximum tokens per response
            delay_between_calls: Delay between API calls to respect rate limits
            
        Returns:
            Dictionary mapping prompt_id to LLMResponse
        """
        responses = {}
        total_prompts = len(prompts)
        
        logger.info(f"Starting batch generation for {total_prompts} prompts")
        
        for i, (prompt_id, prompt_text) in enumerate(prompts.items(), 1):
            try:
                dilemma_id = dilemma_ids[prompt_id]
                prompt_type = prompt_types[prompt_id]
                
                response = self.generate_response(
                    prompt=prompt_text,
                    dilemma_id=dilemma_id,
                    prompt_type=prompt_type,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                responses[prompt_id] = response
                logger.info(f"Completed {i}/{total_prompts} prompts")
                
                # Rate limiting delay
                if i < total_prompts:
                    time.sleep(delay_between_calls)
                    
            except Exception as e:
                logger.error(f"Error processing prompt {prompt_id}: {e}")
                continue
        
        logger.info(f"Batch generation completed: {len(responses)}/{total_prompts} successful")
        return responses
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics (placeholder for future implementation).
        
        Returns:
            Dictionary with usage statistics
        """
        # This would require tracking usage over time
        # For now, return basic info
        return {
            "client_initialized": True,
            "default_model": self.default_model.value,
            "default_temperature": self.default_temperature,
            "default_max_tokens": self.default_max_tokens
        }