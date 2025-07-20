"""
Comprehensive test script for research integration and logging.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_research_integration():
    """Test complete research integration with detailed logging."""
    
    print("🔬 Testing Research Integration with Detailed Logging")
    print("=" * 60)
    
    try:
        # Test 1: Import all research components
        print("\n1️⃣ Testing Imports...")
        from data.research_prompts import get_research_dilemmas, load_research_prompts
        from analysis.research_coding import ResearchCoder
        from utils.research_logger import ResearchLogger
        from models.schemas import DeicticFraming, LLMModel, LLMResponse
        from datetime import datetime
        print("✅ All imports successful")
        
        # Test 2: Load research data
        print("\n2️⃣ Testing Research Data Loading...")
        dilemmas = get_research_dilemmas()
        prompts = load_research_prompts()
        print(f"✅ Loaded {len(dilemmas)} research dilemmas")
        print(f"✅ Loaded {len(prompts)} research prompts")
        
        # Show sample dilemma
        sample_dilemma = dilemmas[0]
        print(f"   Sample: {sample_dilemma.title}")
        print(f"   Category: {sample_dilemma.category}")
        
        # Test 3: Initialize research components
        print("\n3️⃣ Testing Component Initialization...")
        coder = ResearchCoder()
        logger = ResearchLogger()
        print(f"✅ Research coder initialized")
        print(f"✅ Research logger initialized - Session: {logger.session_id}")
        
        # Test 4: Test prompt generation and logging
        print("\n4️⃣ Testing Prompt Generation & Logging...")
        test_prompt = "Think step by step. I am trying to decide what to do about the following situation: Reporting a colleague for a serious ethical violation. What should I do?"
        
        prompt_id = logger.log_prompt_generation(
            dilemma_title=sample_dilemma.title,
            framing=DeicticFraming.ANCHORED_COT,
            prompt=test_prompt,
            source="research"
        )
        print(f"✅ Prompt logged with ID: {prompt_id}")
        
        # Test 5: Test response generation and logging
        print("\n5️⃣ Testing Response Generation & Logging...")
        mock_response = LLMResponse(
            id="test_response_integration",
            model=LLMModel.GPT4,
            prompt_type=DeicticFraming.ANCHORED_COT,
            dilemma_id=sample_dilemma.id,
            prompt_text=test_prompt,
            response_text="I believe we should consider the ethical implications carefully. First, we need to examine the consequences of reporting versus not reporting. Second, we should consider our professional duties and obligations. The ancestors would counsel us to speak truth and protect the vulnerable. From a shamanic perspective, we must honor our relations with all beings.",
            token_count=45,
            processing_time=1.2,
            timestamp=datetime.now()
        )
        
        response_id = logger.log_response_generation(mock_response, prompt_id)
        print(f"✅ Response logged with ID: {response_id}")
        
        # Test 6: Test research coding
        print("\n6️⃣ Testing Research Coding...")
        coding = coder.code_response(mock_response)
        print(f"✅ Research coding completed")
        print(f"   Ethical Mode: {coding.ethical_mode}")
        print(f"   Pronoun Usage: {coding.pronoun_usage}")
        print(f"   Shamanic Markers: {coding.shamanic_cosmological_markers}")
        print(f"   Reasoning Steps: {coding.reasoning_steps_count}")
        print(f"   Prompting Technique: {coding.prompting_technique}")
        
        # Test 7: Test coding logging
        print("\n7️⃣ Testing Coding Logging...")
        detailed_analysis = {
            "response_length": len(mock_response.response_text),
            "word_count": len(mock_response.response_text.split()),
            "sentence_count": len([s for s in mock_response.response_text.split('.') if s.strip()]),
            "ethical_indicators": {
                "deontological_markers": ["duties", "obligations"],
                "shamanic_markers": ["ancestors", "shamanic perspective", "relations"]
            }
        }
        
        coding_id = logger.log_research_coding(
            response_id=mock_response.id,
            coding=coding,
            detailed_analysis=detailed_analysis
        )
        print(f"✅ Coding logged with ID: {coding_id}")
        
        # Test 8: Test session management
        print("\n8️⃣ Testing Session Management...")
        session_summary = logger.get_session_summary()
        print(f"✅ Session summary generated")
        print(f"   Session ID: {session_summary['session_id']}")
        print(f"   Total Activities: {session_summary['activities']}")
        print(f"   Statistics: {session_summary['statistics']}")
        
        # Test 9: Test export functionality
        print("\n9️⃣ Testing Export Functionality...")
        summary_file = logger.export_session_summary()
        csv_file = logger.export_research_data_csv()
        print(f"✅ Session summary exported: {summary_file}")
        print(f"✅ Research CSV exported: {csv_file}")
        
        # Test 10: Test coding export
        print("\n🔟 Testing Coding Export...")
        coding_dict = coder.export_coding_to_dict(coding)
        print(f"✅ Coding exported to dictionary")
        print(f"   Keys: {list(coding_dict.keys())}")
        
        # Final summary
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED - Research Integration Complete!")
        print("=" * 60)
        
        print(f"\n📊 Final Session Statistics:")
        final_stats = logger.get_session_summary()["statistics"]
        print(f"   Prompts Generated: {final_stats['prompts_generated']}")
        print(f"   Responses Generated: {final_stats['responses_generated']}")
        print(f"   Codings Completed: {final_stats['codings_completed']}")
        print(f"   Models Used: {final_stats['models_used']}")
        print(f"   Framings Used: {final_stats['framings_used']}")
        
        print(f"\n📁 Generated Files:")
        print(f"   Session Summary: {summary_file}")
        print(f"   Research CSV: {csv_file}")
        print(f"   Log Directory: research_logs/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_research_integration()
    sys.exit(0 if success else 1)