#!/usr/bin/env python3
"""
Quick test runner for the new Angola Energy Consultant system
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.angola_energy_prompts import angola_energy_prompts
from app.llm_utils import LLMService

def test_prompt_system():
    """Test the new prompt system"""
    print("🚀 Testing Angola Energy Prompt System...")
    
    # Test system prompt creation
    system_prompt = angola_energy_prompts.create_system_prompt()
    print(f"✅ System prompt created ({len(system_prompt)} characters)")
    
    # Test different query types
    test_queries = [
        "Olá!",
        "Quem é a Sonangol?",
        "Quais são as tendências do mercado de petróleo?"
    ]
    
    for query in test_queries:
        query_prompt = angola_energy_prompts.create_query_prompt(
            question=query,
            context="",
            conversation_history=None
        )
        print(f"✅ Query prompt for '{query}' created ({len(query_prompt)} characters)")
    
    print("✅ Prompt system tests completed!")

def test_llm_processor():
    """Test the LLM processor"""
    print("🚀 Testing LLM Service...")
    
    try:
        processor = LLMService()
        print("✅ LLM Service initialized successfully")
        
        # Test greeting detection
        greeting_test = processor._is_simple_greeting("Olá!")
        print(f"✅ Greeting detection test: {greeting_test}")
        
        # Test greeting response
        greeting_response = processor._generate_greeting_response()
        print(f"✅ Greeting response: {greeting_response}")
        
        print("✅ LLM Service tests completed!")
        
    except Exception as e:
        print(f"❌ LLM Service test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🎯 Angola Energy Consultant - Quick Test Suite")
    print("=" * 50)
    
    try:
        # Test prompt system
        test_prompt_system()
        print()
        
        # Test LLM processor
        success = test_llm_processor()
        print()
        
        if success:
            print("🎉 All tests passed! System is ready for integration.")
            return 0
        else:
            print("⚠️ Some tests failed. Check configuration.")
            return 1
            
    except Exception as e:
        print(f"💥 Test suite failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)