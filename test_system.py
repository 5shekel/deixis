"""
Test script for the Deixis AI Agent system.
"""

import logging
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from core.prompt_engine import PromptEngine
from storage.database import DatabaseManager
from analysis.annotator import ResponseAnnotator
from data.ethical_dilemmas import get_sample_dilemmas
from models.schemas import DeicticFraming, LLMModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_system_initialization():
    """Test system component initialization."""
    print("🔧 Testing System Initialization...")
    
    try:
        # Test configuration
        config_status = Config.validate_config()
        print(f"✅ Configuration: {config_status}")
        
        # Test prompt engine
        prompt_engine = PromptEngine()
        framings = prompt_engine.list_framings()
        print(f"✅ Prompt Engine: {len(framings)} deictic framings loaded")
        
        # Test database
        db_manager = DatabaseManager()
        stats = db_manager.get_experiment_stats()
        print(f"✅ Database: Initialized with {stats.get('total_responses', 0)} existing responses")
        
        # Test annotator
        annotator = ResponseAnnotator()
        print("✅ Annotator: Response annotation pipeline ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_prompt_generation():
    """Test prompt generation across all deictic framings."""
    print("\n📝 Testing Prompt Generation...")
    
    try:
        prompt_engine = PromptEngine()
        dilemmas = get_sample_dilemmas()
        test_dilemma = dilemmas[0]  # Use the trolley problem
        
        print(f"Testing with dilemma: {test_dilemma.title}")
        
        for framing in DeicticFraming:
            try:
                if framing == DeicticFraming.ROLE_BASED:
                    prompt = prompt_engine.generate_prompt(test_dilemma, framing, "philosopher")
                else:
                    prompt = prompt_engine.generate_prompt(test_dilemma, framing)
                
                print(f"✅ {framing.value}: Generated {len(prompt)} characters")
                
                # Show a snippet of each prompt type
                snippet = prompt[:100] + "..." if len(prompt) > 100 else prompt
                print(f"   Preview: {snippet}")
                
            except Exception as e:
                print(f"❌ {framing.value}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt generation test failed: {e}")
        return False

def test_annotation_pipeline():
    """Test the annotation pipeline with mock responses."""
    print("\n🔍 Testing Annotation Pipeline...")
    
    try:
        from models.schemas import LLMResponse
        from datetime import datetime
        
        annotator = ResponseAnnotator()
        
        # Create mock responses for testing
        mock_responses = [
            LLMResponse(
                id="test_1",
                model=LLMModel.GPT4,
                prompt_type=DeicticFraming.ANCHORED_COT,
                dilemma_id="trolley_classic",
                prompt_text="Test prompt",
                response_text="I believe we should consider the consequences carefully. From my perspective, saving five lives is more important than one. I would pull the lever because the utilitarian calculation shows greater good.",
                token_count=50,
                timestamp=datetime.now()
            ),
            LLMResponse(
                id="test_2", 
                model=LLMModel.GPT4,
                prompt_type=DeicticFraming.SHAMANIC,
                dilemma_id="trolley_classic",
                prompt_text="Test prompt",
                response_text="The ancestors whisper that all life is sacred. We must honor our relations with all beings. The spirits guide us to seek harmony and balance, not to play the role of deciding who lives or dies.",
                token_count=45,
                timestamp=datetime.now()
            )
        ]
        
        for response in mock_responses:
            annotated = annotator.annotate_response(response)
            
            print(f"✅ Annotated {response.id}:")
            print(f"   Primary stance: {annotated.ethical_annotation.primary_stance.value}")
            print(f"   Confidence: {annotated.ethical_annotation.confidence_score:.2f}")
            print(f"   Pronouns: {len(annotated.linguistic_annotation.pronoun_use)}")
            print(f"   Deictic anchors: {len(annotated.linguistic_annotation.deictic_anchors)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Annotation test failed: {e}")
        return False

def test_database_operations():
    """Test database storage and retrieval."""
    print("\n💾 Testing Database Operations...")
    
    try:
        from models.schemas import LLMResponse
        from datetime import datetime
        
        db_manager = DatabaseManager()
        
        # Create test response
        test_response = LLMResponse(
            id="test_db_response",
            model=LLMModel.GPT4,
            prompt_type=DeicticFraming.NEUTRAL,
            dilemma_id="test_dilemma",
            prompt_text="Test prompt for database",
            response_text="Test response for database storage",
            token_count=25,
            timestamp=datetime.now()
        )
        
        # Test storage
        success = db_manager.store_response(test_response)
        if success:
            print("✅ Response storage: Success")
        else:
            print("❌ Response storage: Failed")
            return False
        
        # Test retrieval
        retrieved = db_manager.get_response(test_response.id)
        if retrieved and retrieved.id == test_response.id:
            print("✅ Response retrieval: Success")
        else:
            print("❌ Response retrieval: Failed")
            return False
        
        # Test statistics
        stats = db_manager.get_experiment_stats()
        print(f"✅ Database stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_ethical_dilemmas_dataset():
    """Test the ethical dilemmas dataset."""
    print("\n📚 Testing Ethical Dilemmas Dataset...")
    
    try:
        from data.ethical_dilemmas import (
            get_sample_dilemmas, get_dilemma_categories, 
            get_dilemmas_by_complexity, get_all_tags
        )
        
        # Test basic loading
        dilemmas = get_sample_dilemmas()
        print(f"✅ Loaded {len(dilemmas)} ethical dilemmas")
        
        # Test categories
        categories = get_dilemma_categories()
        print(f"✅ Found {len(categories)} categories: {categories[:3]}...")
        
        # Test complexity filtering
        complex_dilemmas = get_dilemmas_by_complexity(4, 5)
        print(f"✅ Found {len(complex_dilemmas)} high-complexity dilemmas")
        
        # Test tags
        all_tags = get_all_tags()
        print(f"✅ Found {len(all_tags)} unique tags")
        
        # Validate dilemma structure
        test_dilemma = dilemmas[0]
        required_fields = ['id', 'title', 'description', 'category', 'complexity_level']
        for field in required_fields:
            if not hasattr(test_dilemma, field):
                print(f"❌ Missing field: {field}")
                return False
        
        print("✅ Dilemma structure validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Dataset test failed: {e}")
        return False

def test_visualization_components():
    """Test visualization component initialization."""
    print("\n📊 Testing Visualization Components...")
    
    try:
        from visualization.charts import VisualizationSuite
        
        viz_suite = VisualizationSuite()
        print("✅ Visualization suite initialized")
        
        # Test color schemes
        color_schemes = viz_suite.color_schemes
        expected_schemes = ["deictic_framings", "ethical_stances", "models"]
        
        for scheme in expected_schemes:
            if scheme in color_schemes:
                print(f"✅ Color scheme '{scheme}': {len(color_schemes[scheme])} colors")
            else:
                print(f"❌ Missing color scheme: {scheme}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all system tests."""
    print("🧠 Deixis AI Agent - System Test Suite")
    print("=" * 50)
    
    tests = [
        ("System Initialization", test_system_initialization),
        ("Prompt Generation", test_prompt_generation),
        ("Annotation Pipeline", test_annotation_pipeline),
        ("Database Operations", test_database_operations),
        ("Ethical Dilemmas Dataset", test_ethical_dilemmas_dataset),
        ("Visualization Components", test_visualization_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        print("\n🚀 To start the application, run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)