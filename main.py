"""
Main execution script for the multi-agent Target Company & Law Firm Identification system
Tests with the sample data provided in the assignment
"""

import json
from agents import MultiAgentOrchestrator

def main():
    """Test the multi-agent system with the provided sample data"""
    
    # Sample data from the assignment - exactly 4 paragraphs as specified
    user_query = "Is Kirkland & Ellis present in the agreement?"
    
    paragraphs = [
        # Paragraph 1
        "This Stock and Asset Purchase Agreement is entered into as of October 28, 2021, among Purolite Corporation, a Delaware corporation, along with Stefan E. Brodie and Don B. Brodie (collectively referred to as the Sellers), and Ecolab Inc., a Delaware corporation, as the Purchaser. Additionally, Gibson, Dunn & Crutcher LLP, as an independent third-party representative, is engaged for specific advisory roles outlined in this Agreement.",
        
        # Paragraph 2  
        "This Agreement shall be governed by and construed in accordance with the internal laws of the State of Delaware, without giving effect to any choice or conflict of law provision. Each clause within this Agreement shall be interpreted independently, and the invalidity of one clause shall not affect the enforceability of the remaining provisions. Headings are for convenience only and shall not affect the interpretation of this Agreement. Nothing herein shall be construed as limiting or waiving any rights or obligations under applicable law unless expressly stated.",
        
        # Paragraph 3
        """Such notices, demands, and other communications shall be directed to the Parties at their respective addresses. One Party may be contacted at:
1 Ecolab Place
St. Paul, Minnesota 55102
Attention: General Counsel
with a copy (which shall not constitute notice) to:
Shearman & Sterling LLP
599 Lexington Avenue
New York, New York 10022
Attention: Adam Miller
Another Party may be reached at:
Purolite Corporation
2201 Renaissance Boulevard
King of Prussia, Pennsylvania 19406
Attention: Stefan E. Brodie; Howard Brodie
with a copy (which shall not constitute notice) to:
Cleary Gottlieb Steen & Hamilton LLP
One Liberty Plaza
New York, New York 10006
Attention: John Reynolds; Sarah Lee
Additional communications relating to the role of the third-party representative shall be directed to:
Gibson, Dunn & Crutcher LLP
200 Park Avenue
New York, New York 10166
Attention: Jane Smith""",
        
        # Paragraph 4
        "All references to the singular include the plural and vice versa, and all references to any gender include all genders. The Parties agree that any ambiguities in the language of this Agreement shall not be construed against either Party. Section headings used in this Agreement are for reference only and shall not affect the meaning or interpretation of any provision."
    ]
    
    print("=== DeepJudge Multi-Agent System ===")
    print("Target Company & Law Firm Identification\n")
    
    print(f"User Query: {user_query}")
    print(f"Number of paragraphs to analyze: {len(paragraphs)}\n")
    
    # Initialize and run the multi-agent system
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process(user_query, paragraphs)
    
    # Display results
    if "result" in result and result["result"].startswith("<user_message>"):
        print("Result:", result["result"])
    else:
        print(f"Target Company Identified: {result.get('target_company', 'Unknown')}\n")
        
        print("=== LLM2 Analysis of All 4 Paragraphs ===")
        print(result.get("llm2_analysis", "No analysis available"))
        
        print("\n=== Final JSON Output ===")
        if "final_result" in result:
            print(json.dumps(result["final_result"], indent=2))
        else:
            print("Error:", result.get("error", "Unknown error"))
            print("Raw output:", result.get("raw_output", "None"))

def test_negative_case():
    """Test case where no target company is mentioned"""
    print("\n\n=== Testing Negative Case ===")
    
    # Must provide exactly 4 paragraphs even for negative test
    dummy_paragraphs = [
        "This is paragraph one with no legal content.",
        "This is paragraph two about random topics.", 
        "This is paragraph three discussing weather.",
        "This is paragraph four with generic information."
    ]
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process("What is the weather today?", dummy_paragraphs)
    
    print("Query: What is the weather today?")
    print("Result:", result.get("result", "No result"))

def test_custom_paragraphs():
    """Demonstrate system works with any 4 paragraphs at runtime"""
    print("\n\n=== Testing Custom Runtime Paragraphs ===")
    
    # Example of different 4 paragraphs that could be provided at runtime
    custom_query = "Is Microsoft mentioned in the contract?"
    custom_paragraphs = [
        "This Software License Agreement is between Microsoft Corporation and the Licensee.",
        "The agreement is governed by Washington State law and jurisdiction.",
        "Legal representation for Microsoft is provided by Cravath, Swaine & Moore LLP.",
        "Any disputes will be handled through binding arbitration procedures."
    ]
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process(custom_query, custom_paragraphs)
    
    print(f"Custom Query: {custom_query}")
    print("Custom Paragraphs provided at runtime")
    
    if "result" in result and result["result"].startswith("<user_message>"):
        print("Result:", result["result"])
    else:
        print(f"Target Company: {result.get('target_company', 'Unknown')}")
        print("Final JSON:", json.dumps(result.get("final_result", {}), indent=2))

if __name__ == "__main__":
    main()
    test_negative_case()
    test_custom_paragraphs()
