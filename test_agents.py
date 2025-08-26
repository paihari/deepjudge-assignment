"""
Comprehensive tests for all LLM agents in the DeepJudge Multi-Agent System
"""

import json
from agents import LLM1Agent, LLM2Agent, LLM3Agent, MultiAgentOrchestrator

def test_llm1_agent():
    """Test LLM1 agent for target company detection"""
    print("=== Testing LLM1 Agent ===")
    llm1 = LLM1Agent()
    
    test_cases = [
        ("Is Kirkland & Ellis present in the agreement?", "target_found"),
        ("Does Microsoft appear in the contract?", "target_found"),
        ("Is Apple Inc. mentioned in the document?", "target_found"),
        ("What is the weather today?", "irrelevant"),
        ("How do I cook pasta?", "irrelevant"),
        ("Tell me about machine learning", "irrelevant"),
        ("What time is it?", "irrelevant")
    ]
    
    for query, expected_type in test_cases:
        result = llm1.process(query)
        is_xml = result.startswith('<user_message>')
        
        print(f"Query: {query}")
        print(f"Result: '{result}'")
        print(f"Expected: {expected_type}, Got: {'irrelevant' if is_xml else 'target_found'}")
        print(f"✅ PASS" if (expected_type == "irrelevant") == is_xml else "❌ FAIL")
        print("-" * 60)

def test_llm2_agent():
    """Test LLM2 agent for paragraph analysis"""
    print("\n=== Testing LLM2 Agent ===")
    llm2 = LLM2Agent()
    
    # Sample paragraphs with clear law firm information
    test_paragraphs = [
        "This Purchase Agreement is between Acme Corp (Buyer) represented by Baker McKenzie LLP, and TechCorp (Seller) represented by Latham & Watkins LLP.",
        "The transaction involves advisory services by Goldman Sachs Group Inc. with legal counsel from Skadden, Arps, Slate, Meagher & Flom LLP.",
        "Notice provisions require communications to be sent to the respective legal representatives at their offices.",
        "This agreement shall be governed by Delaware law with dispute resolution through arbitration."
    ]
    
    target_company = "Kirkland & Ellis"
    
    print(f"Target Company: {target_company}")
    print("Analyzing 4 test paragraphs...")
    
    result = llm2.process(test_paragraphs, target_company)
    print("LLM2 Analysis Result:")
    print(result)
    print("-" * 60)

def test_llm3_agent():
    """Test LLM3 agent for JSON compilation"""
    print("\n=== Testing LLM3 Agent ===")
    llm3 = LLM3Agent()
    
    # Sample LLM2 analysis results
    sample_analysis = ["""
Paragraph 1 Analysis:
Buyer: Acme Corp
Buyer Representative: Baker McKenzie LLP
Seller: TechCorp
Seller Representative: Latham & Watkins LLP
Third-Party Representation: None
Target Company Mentioned: No

Paragraph 2 Analysis:
Buyer: Not identified
Buyer Representative: Not stated
Seller: Not identified
Seller Representative: Not stated
Third-Party Representation: Advisory by Skadden, Arps, Slate, Meagher & Flom LLP
Target Company Mentioned: No

Paragraph 3 Analysis:
Buyer: Not identified
Buyer Representative: Not stated
Seller: Not identified
Seller Representative: Not stated
Third-Party Representation: None
Target Company Mentioned: No

Paragraph 4 Analysis:
Buyer: Not identified
Buyer Representative: Not stated
Seller: Not identified
Seller Representative: Not stated
Third-Party Representation: None
Target Company Mentioned: No
"""]
    
    result = llm3.process(sample_analysis)
    print("LLM3 JSON Compilation Result:")
    print(result)
    
    # Validate JSON format
    try:
        json_obj = json.loads(result)
        required_fields = ["buyer_firm", "seller_firm", "third_party", "contains_target_firm"]
        
        print("\nJSON Validation:")
        for field in required_fields:
            if field in json_obj:
                print(f"✅ {field}: {json_obj[field]}")
            else:
                print(f"❌ Missing field: {field}")
        
        # Check data types
        if isinstance(json_obj.get("contains_target_firm"), bool):
            print("✅ contains_target_firm is boolean")
        else:
            print("❌ contains_target_firm should be boolean")
            
    except json.JSONDecodeError:
        print("❌ Invalid JSON format")
    
    print("-" * 60)

def test_full_system_integration():
    """Test the complete multi-agent system with various scenarios"""
    print("\n=== Testing Full System Integration ===")
    orchestrator = MultiAgentOrchestrator()
    
    test_scenarios = [
        {
            "name": "Valid Legal Query",
            "query": "Is Cravath, Swaine & Moore mentioned?",
            "paragraphs": [
                "This merger agreement involves BigCorp Inc. as the acquiring entity.",
                "Legal representation for BigCorp is provided by Cravath, Swaine & Moore LLP.",
                "The target company SmallTech Inc. is represented by Wachtell, Lipton, Rosen & Katz.",
                "Transaction advisory services are handled by Morgan Stanley with Sullivan & Cromwell LLP."
            ]
        },
        {
            "name": "Irrelevant Query",
            "query": "What's the capital of France?",
            "paragraphs": [
                "Random paragraph one",
                "Random paragraph two", 
                "Random paragraph three",
                "Random paragraph four"
            ]
        },
        {
            "name": "No Law Firms Present",
            "query": "Is Apple Inc. mentioned?",
            "paragraphs": [
                "This document contains general business terms.",
                "Apple Inc. is mentioned as a technology company.",
                "No specific legal representation is identified.",
                "The agreement follows standard commercial practices."
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        print(f"Query: {scenario['query']}")
        
        result = orchestrator.process(scenario['query'], scenario['paragraphs'])
        
        if "result" in result and result["result"].startswith("<user_message>"):
            print("Result: System stopped - irrelevant query")
            print(f"Message: {result['result']}")
        else:
            print(f"Target Company: {result.get('target_company', 'Unknown')}")
            if "final_result" in result:
                print("Final JSON:")
                print(json.dumps(result["final_result"], indent=2))
            elif "error" in result:
                print(f"Error: {result['error']}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_llm1_agent()
    test_llm2_agent()
    test_llm3_agent()
    test_full_system_integration()