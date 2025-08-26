"""
Direct test of LLM1 to debug the negative case
"""

from agents import LLM1Agent

def test_llm1_directly():
    llm1 = LLM1Agent()
    
    print("=== Testing LLM1 Directly ===")
    
    # Test relevant query
    relevant_query = "Is Kirkland & Ellis present in the agreement?"
    result1 = llm1.process(relevant_query)
    print(f"Relevant Query: {relevant_query}")
    print(f"Result: '{result1}'")
    print(f"Starts with <user_message>: {result1.startswith('<user_message>')}")
    print()
    
    # Test irrelevant query
    irrelevant_query = "What is the weather today?"
    result2 = llm1.process(irrelevant_query)
    print(f"Irrelevant Query: {irrelevant_query}")
    print(f"Result: '{result2}'")
    print(f"Starts with <user_message>: {result2.startswith('<user_message>')}")
    print()
    
    # Test another irrelevant query
    irrelevant_query2 = "How do I cook pasta?"
    result3 = llm1.process(irrelevant_query2)
    print(f"Irrelevant Query 2: {irrelevant_query2}")
    print(f"Result: '{result3}'")
    print(f"Starts with <user_message>: {result3.startswith('<user_message>')}")

if __name__ == "__main__":
    test_llm1_directly()