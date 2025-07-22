#!/usr/bin/env python3
"""
Test script to verify OpenRouter-only setup for the research system.
"""

import os
from pathlib import Path
from config import Config
from llm.openrouter_client import OpenRouterClient
from models.schemas import LLMModel

def test_environment():
    """Test environment setup."""
    print("🔧 Testing Environment Setup")
    print("=" * 50)
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return False
    
    # Check OpenRouter API key
    config = Config()
    if config.OPENROUTER_API_KEY:
        print("✅ OPENROUTER_API_KEY configured")
        key = config.OPENROUTER_API_KEY
        print(f"   Key: {key[:8]}...{key[-4:]}")
    else:
        print("❌ OPENROUTER_API_KEY not found in .env")
        return False
    
    return True

def test_openrouter_client():
    """Test OpenRouter client initialization and connection."""
    print("\n🔌 Testing OpenRouter Client")
    print("=" * 50)
    
    try:
        # Initialize client
        client = OpenRouterClient()
        print("✅ OpenRouter client initialized successfully")
        
        # Test connection
        if client.test_connection():
            print("✅ OpenRouter API connection successful")
        else:
            print("❌ OpenRouter API connection failed")
            return False
        
        # Check supported models
        supported_models = client.get_supported_models()
        print(f"✅ Supported models: {[m.value for m in supported_models]}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter client error: {e}")
        return False

def test_model_access():
    """Test access to specific models via OpenRouter."""
    print("\n🤖 Testing Model Access")
    print("=" * 50)
    
    try:
        client = OpenRouterClient()
        
        # Test models
        test_models = [
            (LLMModel.GPT4, "openai/gpt-4"),
            (LLMModel.CLAUDE_3_SONNET, "anthropic/claude-3-sonnet"),
            (LLMModel.DEEPSEEK_R1, "deepseek/deepseek-r1")
        ]
        
        test_prompt = "Hello, please respond with just 'OK' to confirm you're working."
        
        for model_enum, model_name in test_models:
            try:
                print(f"Testing {model_enum.value}...")
                
                # Make a simple test call
                response = client.client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=10,
                    temperature=0.1
                )
                
                response_text = response.choices[0].message.content.strip()
                print(f"✅ {model_enum.value}: {response_text}")
                
            except Exception as e:
                print(f"❌ {model_enum.value}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Model access test failed: {e}")
        return False

def test_research_data_loading():
    """Test research data loading."""
    print("\n📊 Testing Research Data Loading")
    print("=" * 50)
    
    try:
        from data.research_prompts import load_research_prompts, get_all_dilemma_prompt_combinations
        
        # Load research prompts
        prompts = load_research_prompts()
        if prompts:
            print(f"✅ Research prompts loaded: {len(prompts)} prompts")
        else:
            print("❌ No research prompts loaded")
            return False
        
        # Load prompt combinations
        combinations = get_all_dilemma_prompt_combinations()
        if combinations:
            print(f"✅ Prompt combinations loaded: {len(combinations)} combinations")
            
            # Show sample
            sample = combinations[0]
            print(f"   Sample combination keys: {list(sample.keys())}")
        else:
            print("❌ No prompt combinations loaded")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Research data loading failed: {e}")
        return False

def test_concurrent_runner_init():
    """Test concurrent research runner initialization."""
    print("\n🚀 Testing Concurrent Research Runner")
    print("=" * 50)
    
    try:
        from concurrent_research_runner import ConcurrentResearchRunner
        
        # Initialize with minimal settings
        runner = ConcurrentResearchRunner(
            models=[LLMModel.GPT4],  # Test with just one model
            max_concurrent=1
        )
        
        print("✅ ConcurrentResearchRunner initialized successfully")
        print(f"   Models configured: {[m.value for m in runner.models]}")
        print(f"   Prompt combinations: {len(runner.prompt_combinations)}")
        print(f"   Session ID: {runner.logger.session_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ ConcurrentResearchRunner initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 OpenRouter Setup Test Suite")
    print("=" * 60)
    print("Testing the OpenRouter-only configuration for the research system")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment),
        ("OpenRouter Client", test_openrouter_client),
        ("Model Access", test_model_access),
        ("Research Data Loading", test_research_data_loading),
        ("Concurrent Runner Init", test_concurrent_runner_init)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your OpenRouter setup is ready.")
        print("\nNext steps:")
        print("1. Run: python concurrent_research_runner.py")
        print("2. Or run: streamlit run streamlit_research_app.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check your configuration.")
        print("\nTroubleshooting:")
        print("1. Ensure OPENROUTER_API_KEY is set in your .env file")
        print("2. Check your internet connection")
        print("3. Verify your OpenRouter account has sufficient credits")

if __name__ == "__main__":
    main()
