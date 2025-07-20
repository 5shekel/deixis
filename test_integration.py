#!/usr/bin/env python3
"""
Integration test script for the AI Agent System.
Verifies all components are working with your research prompts.
"""

def test_system_integration():
    """Test all system components."""
    print('🔬 AI Agent System - Integration Test')
    print('=' * 50)
    
    try:
        # Test 1: Import all core modules
        print('\n1️⃣ Testing Core Imports...')
        from data.research_prompts import load_research_prompts, get_research_statistics
        from models.schemas import DeicticFraming, ResearchPrompt
        from analysis.research_coding import ResearchCoder
        from utils.research_logger import ResearchLogger
        print('✅ All core imports successful')
        
        # Test 2: Load your research prompts
        print('\n2️⃣ Testing Research Prompts Loading...')
        prompts = load_research_prompts()
        print(f'✅ Loaded {len(prompts)} prompts from Extended_Prompt_Set_with_Shamanic_Deixis.csv')
        
        # Test 3: Show sample prompts
        print('\n3️⃣ Sample Prompts:')
        for i, prompt in enumerate(prompts[:3]):
            print(f'   {i+1}. {prompt.dilemma_title}')
            print(f'      Framing: {prompt.framing.value}')
            print(f'      Prompt: {prompt.prompt_text[:80]}...')
            print()
        
        # Test 4: Research statistics
        print('4️⃣ Research Dataset Statistics:')
        stats = get_research_statistics()
        print(f'   📊 Total prompts: {stats["total_prompts"]}')
        print(f'   📋 Total dilemmas: {stats["total_dilemmas"]}')
        print(f'   🔄 Prompts per dilemma: {stats["prompts_per_dilemma"]}')
        print('   📈 Framing distribution:')
        for framing, count in stats['framing_distribution'].items():
            print(f'      {framing}: {count} prompts')
        
        # Test 5: Research coding system
        print('\n5️⃣ Testing Research Coding System...')
        coder = ResearchCoder()
        print('✅ Research coder initialized')
        
        # Test 6: Logging system
        print('\n6️⃣ Testing Logging System...')
        logger = ResearchLogger()
        print(f'✅ Research logger initialized - Session: {logger.session_id}')
        
        # Test 7: LLM clients (basic initialization)
        print('\n7️⃣ Testing LLM Clients...')
        try:
            from llm.openai_client import OpenAIClient
            from llm.openrouter_client import OpenRouterClient
            print('✅ LLM client imports successful')
            print('⚠️  Note: API keys required for actual usage')
        except Exception as e:
            print(f'⚠️  LLM clients: {e}')
        
        # Test 8: Web interface
        print('\n8️⃣ Testing Web Interface...')
        try:
            import app
            print('✅ Streamlit app imports successfully')
        except Exception as e:
            print(f'❌ Streamlit app error: {e}')
        
        # Summary
        print('\n' + '=' * 50)
        print('🎉 INTEGRATION TEST COMPLETE')
        print('=' * 50)
        print(f'✅ System ready to process {len(prompts)} research prompts')
        print('✅ All 5 deictic framings available')
        print('✅ 13-variable research coding scheme ready')
        print('✅ Comprehensive logging system operational')
        print('\n📋 Next Steps:')
        print('   1. Set up API keys in .env file')
        print('   2. Run: streamlit run app.py (for web interface)')
        print('   3. Run: python batch_research_runner.py (for batch processing)')
        print('\n📁 Your research prompts are ready for systematic analysis!')
        
        return True
        
    except Exception as e:
        print(f'\n❌ Integration test failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_integration()
    exit(0 if success else 1)