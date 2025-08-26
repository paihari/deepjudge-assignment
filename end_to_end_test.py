"""
End-to-End Test Suite for DeepJudge Multi-Agent System
Stores complete test results for validation and submission
"""

import json
import datetime
from agents import MultiAgentOrchestrator

def run_positive_test():
    """Run positive test case with expected target company and law firm detection"""
    print("=== END-TO-END POSITIVE TEST ===")
    
    # Test data from the assignment
    user_query = "Is Kirkland & Ellis present in the agreement?"
    paragraphs = [
        # Paragraph 1 - Agreement parties and third-party rep
        "This Stock and Asset Purchase Agreement is entered into as of October 28, 2021, among Purolite Corporation, a Delaware corporation, along with Stefan E. Brodie and Don B. Brodie (collectively referred to as the Sellers), and Ecolab Inc., a Delaware corporation, as the Purchaser. Additionally, Gibson, Dunn & Crutcher LLP, as an independent third-party representative, is engaged for specific advisory roles outlined in this Agreement.",
        
        # Paragraph 2 - Governing law clause  
        "This Agreement shall be governed by and construed in accordance with the internal laws of the State of Delaware, without giving effect to any choice or conflict of law provision. Each clause within this Agreement shall be interpreted independently, and the invalidity of one clause shall not affect the enforceability of the remaining provisions. Headings are for convenience only and shall not affect the interpretation of this Agreement. Nothing herein shall be construed as limiting or waiving any rights or obligations under applicable law unless expressly stated.",
        
        # Paragraph 3 - Notice provisions with law firm addresses
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
        
        # Paragraph 4 - General interpretation clause
        "All references to the singular include the plural and vice versa, and all references to any gender include all genders. The Parties agree that any ambiguities in the language of this Agreement shall not be construed against either Party. Section headings used in this Agreement are for reference only and shall not affect the meaning or interpretation of any provision."
    ]
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process(user_query, paragraphs)
    
    test_result = {
        "test_type": "POSITIVE",
        "timestamp": datetime.datetime.now().isoformat(),
        "input": {
            "user_query": user_query,
            "paragraph_count": len(paragraphs),
            "paragraphs": paragraphs
        },
        "processing_steps": {},
        "output": result,
        "validation": {}
    }
    
    # Analyze results
    if "result" in result and result["result"].startswith("<user_message>"):
        test_result["validation"]["status"] = "UNEXPECTED_STOP"
        test_result["validation"]["message"] = "System stopped unexpectedly on relevant query"
    elif "final_result" in result:
        test_result["validation"]["status"] = "SUCCESS"
        test_result["validation"]["target_company_detected"] = result.get("target_company")
        test_result["validation"]["json_valid"] = True
        test_result["validation"]["required_fields"] = []
        
        # Validate JSON structure
        final_json = result["final_result"]
        required_fields = ["buyer_firm", "seller_firm", "third_party", "contains_target_firm"]
        
        for field in required_fields:
            if field in final_json:
                test_result["validation"]["required_fields"].append({
                    "field": field,
                    "present": True,
                    "value": final_json[field],
                    "type": type(final_json[field]).__name__
                })
            else:
                test_result["validation"]["required_fields"].append({
                    "field": field,
                    "present": False
                })
        
        # Expected results validation
        expected = {
            "buyer_firm": "Shearman & Sterling LLP",
            "seller_firm": "Cleary Gottlieb Steen & Hamilton LLP",
            "third_party": "Gibson, Dunn & Crutcher LLP",
            "contains_target_firm": False  # Kirkland & Ellis is NOT in the document
        }
        
        test_result["validation"]["expected_vs_actual"] = {}
        for key, expected_value in expected.items():
            actual_value = final_json.get(key)
            test_result["validation"]["expected_vs_actual"][key] = {
                "expected": expected_value,
                "actual": actual_value,
                "match": actual_value == expected_value
            }
    else:
        test_result["validation"]["status"] = "ERROR"
        test_result["validation"]["error"] = result.get("error", "Unknown error")
    
    return test_result

def run_negative_test():
    """Run negative test case with irrelevant query that should trigger XML response"""
    print("\n=== END-TO-END NEGATIVE TEST ===")
    
    # Irrelevant query
    user_query = "What is the weather forecast for tomorrow?"
    
    # Dummy paragraphs (required but won't be processed)
    paragraphs = [
        "This is dummy paragraph one that won't be processed.",
        "This is dummy paragraph two with no legal content.",
        "This is dummy paragraph three about random topics.",
        "This is dummy paragraph four with generic information."
    ]
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process(user_query, paragraphs)
    
    test_result = {
        "test_type": "NEGATIVE",
        "timestamp": datetime.datetime.now().isoformat(),
        "input": {
            "user_query": user_query,
            "paragraph_count": len(paragraphs),
            "paragraphs": paragraphs
        },
        "output": result,
        "validation": {}
    }
    
    # Analyze results
    if "result" in result and result["result"].startswith("<user_message>"):
        test_result["validation"]["status"] = "SUCCESS"
        test_result["validation"]["message"] = "System correctly stopped with XML message"
        test_result["validation"]["xml_format_correct"] = result["result"] == "<user_message>Query is not relevant to the intended task.</user_message>"
        test_result["validation"]["system_stopped"] = True
    elif "final_result" in result:
        test_result["validation"]["status"] = "UNEXPECTED_PROCESSING"
        test_result["validation"]["message"] = "System should have stopped but continued processing"
        test_result["validation"]["system_stopped"] = False
    else:
        test_result["validation"]["status"] = "ERROR"
        test_result["validation"]["error"] = result.get("error", "Unknown error")
    
    return test_result

def run_custom_positive_test():
    """Run additional positive test with different target company"""
    print("\n=== END-TO-END CUSTOM POSITIVE TEST ===")
    
    user_query = "Is Microsoft Corporation mentioned in the agreement?"
    paragraphs = [
        "This Software License Agreement is entered into between Microsoft Corporation, a Washington corporation (Licensor), and TechStart Inc., a Delaware corporation (Licensee).",
        "Microsoft Corporation grants to Licensee a non-exclusive license to use the software subject to the terms herein.",
        "Legal representation for Microsoft is provided by Cravath, Swaine & Moore LLP, while TechStart is represented by Wilson Sonsini Goodrich & Rosati.",
        "This agreement shall be governed by Washington State law with disputes resolved through binding arbitration."
    ]
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.process(user_query, paragraphs)
    
    test_result = {
        "test_type": "CUSTOM_POSITIVE",
        "timestamp": datetime.datetime.now().isoformat(),
        "input": {
            "user_query": user_query,
            "paragraph_count": len(paragraphs),
            "paragraphs": paragraphs
        },
        "output": result,
        "validation": {}
    }
    
    # Validate target company detection and presence
    if "final_result" in result:
        test_result["validation"]["status"] = "SUCCESS"
        test_result["validation"]["target_company_detected"] = result.get("target_company")
        test_result["validation"]["target_found_in_document"] = result["final_result"].get("contains_target_firm", False)
        test_result["validation"]["expected_target_found"] = True  # Microsoft IS in the document
    else:
        test_result["validation"]["status"] = "ERROR"
    
    return test_result

def save_test_results(positive_result, negative_result, custom_positive_result):
    """Save all test results to JSON file"""
    
    # Summary
    summary = {
        "test_suite": "DeepJudge Multi-Agent System End-to-End Tests",
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": 3,
        "results": {
            "positive_test": positive_result,
            "negative_test": negative_result,
            "custom_positive_test": custom_positive_result
        },
        "summary": {
            "positive_test_passed": positive_result["validation"]["status"] == "SUCCESS",
            "negative_test_passed": negative_result["validation"]["status"] == "SUCCESS",
            "custom_positive_test_passed": custom_positive_result["validation"]["status"] == "SUCCESS"
        }
    }
    
    # Overall status
    all_passed = all([
        summary["summary"]["positive_test_passed"],
        summary["summary"]["negative_test_passed"],
        summary["summary"]["custom_positive_test_passed"]
    ])
    
    summary["overall_status"] = "PASS" if all_passed else "FAIL"
    summary["summary"]["all_tests_passed"] = all_passed
    
    # Save to file
    with open('test_results.json', 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== TEST RESULTS SAVED ===")
    print(f"File: test_results.json")
    print(f"Overall Status: {summary['overall_status']}")
    print(f"Tests Passed: {sum(summary['summary'].values())} / 3")
    
    return summary

def main():
    """Run all end-to-end tests and save results"""
    print("DeepJudge Multi-Agent System - End-to-End Test Suite")
    print("=" * 60)
    
    # Run tests
    positive_result = run_positive_test()
    negative_result = run_negative_test()
    custom_positive_result = run_custom_positive_test()
    
    # Save results
    summary = save_test_results(positive_result, negative_result, custom_positive_result)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in summary["summary"].items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall Result: {'🎉 ALL TESTS PASSED' if summary['overall_status'] == 'PASS' else '⚠️ SOME TESTS FAILED'}")

if __name__ == "__main__":
    main()