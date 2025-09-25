#!/usr/bin/env python3
"""
Integration test script for the new Angola Energy Consultant system
Tests both Firecrawl scraping and the new prompt system
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.firecrawl_scraper import AngolaEnergyScraper
from app.angola_energy_prompts import angola_energy_prompts
from app.llm_utils import LLMService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemIntegrationTest:
    def __init__(self):
        self.scraper = AngolaEnergyScraper()
        self.llm_processor = LLMService()
        self.test_results = []
    
    async def test_firecrawl_scraping(self):
        """Test Firecrawl scraping functionality"""
        logger.info("🚀 Starting Firecrawl scraping tests...")
        
        # Test companies to scrape
        test_companies = ['total', 'sonangol', 'azule']  # Start with 3 for testing
        
        for company in test_companies:
            try:
                logger.info(f"🔍 Testing scraping for {company.upper()}...")
                
                # Scrape the company data
                scraped_data = await self.scraper.scrape_company(company)
                
                if scraped_data and scraped_data.get('success'):
                    logger.info(f"✅ Successfully scraped {company}")
                    logger.info(f"📊 Content length: {len(scraped_data.get('content', ''))} characters")
                    logger.info(f"🏷️ Keywords found: {scraped_data.get('keywords', [])[:5]}")
                    
                    # Save scraped data for later use
                    self.save_test_data(f"scraped_{company}", scraped_data)
                    
                    self.test_results.append({
                        "test": f"firecrawl_{company}",
                        "status": "success",
                        "data_size": len(scraped_data.get('content', '')),
                        "keywords": len(scraped_data.get('keywords', [])),
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    logger.warning(f"⚠️ Scraping failed for {company}")
                    self.test_results.append({
                        "test": f"firecrawl_{company}",
                        "status": "failed",
                        "error": scraped_data.get('error', 'Unknown error'),
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error scraping {company}: {e}")
                self.test_results.append({
                    "test": f"firecrawl_{company}",
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        logger.info("✅ Firecrawl scraping tests completed")
    
    def test_prompt_system(self):
        """Test the new Angola Energy Prompt System"""
        logger.info("🚀 Starting prompt system tests...")
        
        # Test different types of queries
        test_queries = [
            {
                "type": "greeting",
                "query": "Olá!",
                "expected": "short_response"
            },
            {
                "type": "company_analysis", 
                "query": "Quem é a Sonangol e quais são seus principais projetos?",
                "expected": "detailed_analysis"
            },
            {
                "type": "market_trends",
                "query": "Quais são as tendências do mercado de petróleo em Angola?",
                "expected": "trend_analysis"
            },
            {
                "type": "block_analysis",
                "query": "Quais blocos de exploração a TotalEnergies opera em Angola?",
                "expected": "block_details"
            }
        ]
        
        for test in test_queries:
            try:
                logger.info(f"🔍 Testing {test['type']}: {test['query'][:50]}...")
                
                # Test system prompt creation
                system_prompt = angola_energy_prompts.create_system_prompt()
                logger.info(f"✅ System prompt created ({len(system_prompt)} chars)")
                
                # Test query prompt creation
                query_prompt = angola_energy_prompts.create_query_prompt(
                    question=test['query'],
                    context="",
                    conversation_history=None
                )
                logger.info(f"✅ Query prompt created ({len(query_prompt)} chars)")
                
                # Test with LLM processor
                result = self.llm_processor.process_query_with_llm(test['query'])
                
                if result and result.get('response'):
                    response_length = len(result['response'])
                    logger.info(f"✅ LLM response generated ({response_length} chars)")
                    logger.info(f"📊 Response type: {result.get('metadata', {}).get('type', 'unknown')}")
                    
                    # Save response for analysis
                    self.save_test_data(f"response_{test['type']}", {
                        "query": test['query'],
                        "response": result['response'],
                        "metadata": result.get('metadata', {}),
                        "confidence": result.get('confidence', 0)
                    })
                    
                    self.test_results.append({
                        "test": f"prompt_{test['type']}",
                        "status": "success", 
                        "response_length": response_length,
                        "confidence": result.get('confidence', 0),
                        "metadata": result.get('metadata', {}),
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    logger.warning(f"⚠️ No response generated for {test['type']}")
                    self.test_results.append({
                        "test": f"prompt_{test['type']}",
                        "status": "failed",
                        "error": "No response generated",
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error testing {test['type']}: {e}")
                self.test_results.append({
                    "test": f"prompt_{test['type']}",
                    "status": "error", 
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        logger.info("✅ Prompt system tests completed")
    
    def test_integration(self):
        """Test full integration with scraped data"""
        logger.info("🚀 Starting integration tests...")
        
        # Test using scraped data as context
        test_queries = [
            "Com base nos dados recentes, como está a performance da TotalEnergies em Angola?",
            "Quais são os principais projetos da Sonangol mencionados nos dados recentes?"
        ]
        
        for query in test_queries:
            try:
                logger.info(f"🔍 Testing integration: {query[:50]}...")
                
                # Load scraped data as context
                context_data = self.load_scraped_data()
                
                # Process with context
                result = self.llm_processor.process_query_with_llm(
                    query, 
                    context_data=context_data
                )
                
                if result and result.get('response'):
                    logger.info(f"✅ Integration response generated ({len(result['response'])} chars)")
                    
                    self.save_test_data(f"integration_{hash(query) % 1000}", {
                        "query": query,
                        "response": result['response'],
                        "context_used": bool(context_data),
                        "metadata": result.get('metadata', {})
                    })
                    
                    self.test_results.append({
                        "test": "integration_with_context",
                        "status": "success",
                        "response_length": len(result['response']),
                        "context_used": bool(context_data),
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    logger.warning(f"⚠️ No integration response generated")
                    self.test_results.append({
                        "test": "integration_with_context",
                        "status": "failed",
                        "error": "No response generated",
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error in integration test: {e}")
                self.test_results.append({
                    "test": "integration_with_context",
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        logger.info("✅ Integration tests completed")
    
    def save_test_data(self, filename: str, data: dict):
        """Save test data for analysis"""
        output_dir = Path(__file__).parent / "test_outputs"
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Test data saved: {filepath}")
    
    def load_scraped_data(self) -> dict:
        """Load previously scraped data"""
        # This is a simplified version - in production, you'd load from database/vector store
        return {
            "companies": ["TotalEnergies", "Sonangol", "Azule Energy"],
            "recent_data": datetime.now().strftime("%Y-%m-%d"),
            "data_sources": ["firecrawl_scraping", "company_websites"]
        }
    
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("📊 Generating test report...")
        
        report = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "successful": sum(1 for r in self.test_results if r["status"] == "success"),
                "failed": sum(1 for r in self.test_results if r["status"] == "failed"),
                "errors": sum(1 for r in self.test_results if r["status"] == "error"),
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": self.test_results
        }
        
        # Save report
        self.save_test_data("integration_report", report)
        
        # Print summary
        print("\n" + "="*60)
        print("🎯 INTEGRATION TEST REPORT")
        print("="*60)
        print(f"Total Tests: {report['test_summary']['total_tests']}")
        print(f"✅ Successful: {report['test_summary']['successful']}")
        print(f"⚠️ Failed: {report['test_summary']['failed']}")
        print(f"❌ Errors: {report['test_summary']['errors']}")
        print("="*60)
        
        return report
    
    async def run_all_tests(self):
        """Run all integration tests"""
        logger.info("🚀 Starting comprehensive integration tests...")
        
        try:
            # Test Firecrawl scraping
            await self.test_firecrawl_scraping()
            
            # Test prompt system
            self.test_prompt_system()
            
            # Test integration
            self.test_integration()
            
            # Generate report
            report = self.generate_report()
            
            logger.info("✅ All integration tests completed successfully!")
            return report
            
        except Exception as e:
            logger.error(f"❌ Integration test suite failed: {e}")
            raise

async def main():
    """Main test execution"""
    tester = SystemIntegrationTest()
    
    try:
        # Run all tests
        report = await tester.run_all_tests()
        
        # Return exit code based on success rate
        success_rate = report['test_summary']['successful'] / report['test_summary']['total_tests']
        
        if success_rate >= 0.8:  # 80% success rate
            logger.info("🎉 Integration tests PASSED with high success rate!")
            return 0
        else:
            logger.warning(f"⚠️ Integration tests completed with {success_rate:.1%} success rate")
            return 1
            
    except Exception as e:
        logger.error(f"💥 Integration test suite crashed: {e}")
        return 1

if __name__ == "__main__":
    # Run the integration tests
    exit_code = asyncio.run(main())
    sys.exit(exit_code)