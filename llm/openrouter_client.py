"""
OpenRouter client for accessing multiple LLM models through a unified API.
"""

import logging
import time
from typing import Optional, Dict, Any, List
from openai import OpenAI
from models.schemas import LLMResponse, LLMModel, DeicticFraming
from config import Config

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """
    Client for interacting with multiple LLMs through OpenRouter API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key. If None, will use Config.OPENROUTER_API_KEY
        """
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        # OpenRouter uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.default_temperature = Config.TEMPERATURE
        self.default_max_tokens = Config.MAX_TOKENS
        
        # OpenRouter model mappings
        self.model_mappings = {
            LLMModel.CLAUDE_3_OPUS: "anthropic/claude-3-opus",
            LLMModel.CLAUDE_3_SONNET: "anthropic/claude-3-sonnet",
            LLMModel.DEEPSEEK_R1: "deepseek/deepseek-r1",
            LLMModel.GPT4: "openai/gpt-4",
            LLMModel.GPT4_TURBO: "openai/gpt-4-turbo"
        }
        
        logger.info("OpenRouter client initialized")
    
    def generate_response(self,
                         prompt: str,
                         dilemma_id: str,
                         prompt_type: DeicticFraming,
                         model: LLMModel,
                         temperature: float = None,
                         max_tokens: int = None,
                         **kwargs) -> LLMResponse:
        """
        Generate a response using OpenRouter.
        
        Args:
            prompt: The formatted prompt to send
            dilemma_id: ID of the ethical dilemma
            prompt_type: Type of deictic framing used
            model: LLM model to use
            temperature: Temperature setting (0.0-2.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters for the API call
            
        Returns:
            LLMResponse object with the generated response and metadata
        """
        # Set defaults
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens or self.default_max_tokens
        
        # Get OpenRouter model name
        if model not in self.model_mappings:
            raise ValueError(f"Unsupported model for OpenRouter: {model}")
        
        openrouter_model = self.model_mappings[model]
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
                model=openrouter_model,
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
                id=f"{dilemma_id}_{prompt_type.value}_{model.value}_{int(time.time())}",
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
            
            logger.info(f"Generated response for {dilemma_id} with {model.value} via OpenRouter")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error generating response via OpenRouter: {e}")
            raise
    
    async def generate_response_async(self,
                                    prompt: str,
                                    model: str = "anthropic/claude-3-sonnet",
                                    temperature: float = 0.7,
                                    max_tokens: int = 2000) -> Optional[str]:
        """
        Generate a response using OpenRouter API asynchronously.
        
        Args:
            prompt: The input prompt
            model: The model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text or None if failed
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            try:
                import aiohttp
            except ImportError:
                raise ImportError("aiohttp is required for async operations. Install with: pip install aiohttp")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        logger.error(f"OpenRouter API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error generating async OpenRouter response: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to OpenRouter API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=16
            )
            logger.info("OpenRouter API connection test successful")
            return True
        except Exception as e:
            logger.error(f"OpenRouter API connection test failed: {e}")
            return False
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from OpenRouter.
        
        Returns:
            List of available models with metadata
        """
        try:
            # OpenRouter provides a models endpoint
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models_data = response.json()
                logger.info(f"Retrieved {len(models_data.get('data', []))} OpenRouter models")
                return models_data.get('data', [])
            else:
                logger.error(f"Failed to retrieve models: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving models: {e}")
            return []
    
    def estimate_cost(self, prompt: str, model: LLMModel, max_tokens: int = None) -> Dict[str, float]:
        """
        Estimate the cost of a prompt for a specific model.
        
        Args:
            prompt: The prompt text
            model: The model to use
            max_tokens: Maximum response tokens
            
        Returns:
            Dictionary with cost estimates
        """
        max_tokens = max_tokens or self.default_max_tokens
        
        # Rough token estimation (1 token ≈ 4 characters)
        prompt_tokens = len(prompt) // 4
        total_tokens = prompt_tokens + max_tokens
        
        # OpenRouter pricing varies by model - these are approximate
        pricing = {
            LLMModel.CLAUDE_3_OPUS: {"input": 0.015, "output": 0.075},
            LLMModel.CLAUDE_3_SONNET: {"input": 0.003, "output": 0.015},
            LLMModel.DEEPSEEK_R1: {"input": 0.0014, "output": 0.0028},
            LLMModel.GPT4: {"input": 0.03, "output": 0.06},
            LLMModel.GPT4_TURBO: {"input": 0.01, "output": 0.03}
        }
        
        if model in pricing:
            prices = pricing[model]
            input_cost = (prompt_tokens / 1000) * prices["input"]
            output_cost = (max_tokens / 1000) * prices["output"]
            
            return {
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": input_cost + output_cost,
                "prompt_tokens": prompt_tokens,
                "max_response_tokens": max_tokens,
                "model": model.value
            }
        else:
            return {
                "error": f"Pricing not available for {model.value}",
                "prompt_tokens": prompt_tokens,
                "max_response_tokens": max_tokens
            }
    
    def batch_generate(self,
                      prompts: Dict[str, str],
                      dilemma_ids: Dict[str, str],
                      prompt_types: Dict[str, DeicticFraming],
                      models: Dict[str, LLMModel],
                      temperature: float = None,
                      max_tokens: int = None,
                      delay_between_calls: float = 1.0) -> Dict[str, LLMResponse]:
        """
        Generate responses for multiple prompts in batch.
        
        Args:
            prompts: Dictionary mapping prompt_id to prompt text
            dilemma_ids: Dictionary mapping prompt_id to dilemma_id
            prompt_types: Dictionary mapping prompt_id to DeicticFraming
            models: Dictionary mapping prompt_id to LLMModel
            temperature: Temperature setting
            max_tokens: Maximum tokens per response
            delay_between_calls: Delay between API calls to respect rate limits
            
        Returns:
            Dictionary mapping prompt_id to LLMResponse
        """
        responses = {}
        total_prompts = len(prompts)
        
        logger.info(f"Starting OpenRouter batch generation for {total_prompts} prompts")
        
        for i, (prompt_id, prompt_text) in enumerate(prompts.items(), 1):
            try:
                dilemma_id = dilemma_ids[prompt_id]
                prompt_type = prompt_types[prompt_id]
                model = models[prompt_id]
                
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
        
        logger.info(f"OpenRouter batch generation completed: {len(responses)}/{total_prompts} successful")
        return responses
    
    def get_supported_models(self) -> List[LLMModel]:
        """
        Get list of LLMModel enums supported by this client.
        
        Returns:
            List of supported LLMModel values
        """
        return list(self.model_mappings.keys())
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        return {
            "client_type": "OpenRouter",
            "supported_models": [model.value for model in self.model_mappings.keys()],
            "default_temperature": self.default_temperature,
            "default_max_tokens": self.default_max_tokens,
            "base_url": "https://openrouter.ai/api/v1"
        }
