"""
Multi-agent system for Target Company & Law Firm Identification
Following the DeepJudge assignment specifications
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ParagraphAnalysis:
    buyer_firm: str
    seller_firm: str
    third_party: str
    contains_target: bool
    
@dataclass
class FinalOutput:
    buyer_firm: str
    seller_firm: str
    third_party: str
    contains_target_firm: bool

class LLMAgent:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.2):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
    
    def query(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

class LLM1Agent(LLMAgent):
    """Step 1: Determines if the user's query mentions any target company"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """You are tasked with identifying whether a user query mentions any target company that needs to be searched for in legal documents.

Your task:
1. Analyze the user query to determine if it mentions a specific company name that should be treated as a "target company"
2. A target company is typically a specific business entity, law firm, or organization that the user wants to find in legal documents

Response format - FOLLOW EXACTLY:
- If NO target company is found: You MUST respond with EXACTLY this format: <user_message>Query is not relevant to the intended task.</user_message>
- If a target company IS found: You MUST respond with EXACTLY this format: The target company is [COMPANY NAME].

CRITICAL: 
- For irrelevant queries (weather, cooking, general questions, etc.), you MUST use the XML format with <user_message> tags
- For target company queries, do NOT use XML tags, just the plain text format
- Be precise and follow the format exactly
- Look for specific company names, law firms, or business entities in the query"""

    def process(self, user_query: str) -> str:
        return self.query(self.system_prompt, user_query)

class LLM2Agent(LLMAgent):
    """Step 2: Examines four separate paragraphs independently to extract law firm information"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """You are tasked with analyzing four separate paragraphs from a legal document independently to extract information about law firms and target company presence.

For each of the four paragraphs provided, extract the following information:

1. Buyer's representative law firm (the law firm representing the buyer/purchaser)
2. Seller's representative law firm (the law firm representing the seller)  
3. Any third-party law firm present (law firms representing other parties or serving advisory roles)
4. Whether the target company is mentioned in the paragraph

Instructions:
- Analyze each paragraph independently 
- Look for law firm names (typically ending in LLP, LLC, PC, or similar)
- Identify which party each law firm represents based on context
- A law firm name alone without clear representation context should be considered third-party
- Be precise in identifying the actual law firm names

Output format for each paragraph (follow exactly):
Paragraph 1 Analysis:
Buyer: [Company Name or "Not identified"]
Buyer Representative: [Law Firm Name or "Not stated"]
Seller: [Company Name or "Not identified"] 
Seller Representative: [Law Firm Name or "Not stated"]
Third-Party Representation: [Description and Law Firm Name or "None"]
Target Company Mentioned: [Yes/No]

Paragraph 2 Analysis:
Buyer: [Company Name or "Not identified"]
Buyer Representative: [Law Firm Name or "Not stated"]
Seller: [Company Name or "Not identified"] 
Seller Representative: [Law Firm Name or "Not stated"]
Third-Party Representation: [Description and Law Firm Name or "None"]
Target Company Mentioned: [Yes/No]

Paragraph 3 Analysis:
Buyer: [Company Name or "Not identified"]
Buyer Representative: [Law Firm Name or "Not stated"]
Seller: [Company Name or "Not identified"] 
Seller Representative: [Law Firm Name or "Not stated"]
Third-Party Representation: [Description and Law Firm Name or "None"]
Target Company Mentioned: [Yes/No]

Paragraph 4 Analysis:
Buyer: [Company Name or "Not identified"]
Buyer Representative: [Law Firm Name or "Not stated"]
Seller: [Company Name or "Not identified"] 
Seller Representative: [Law Firm Name or "Not stated"]
Third-Party Representation: [Description and Law Firm Name or "None"]
Target Company Mentioned: [Yes/No]"""

    def process(self, paragraphs: List[str], target_company: str) -> str:
        user_message = f"Target company to look for: {target_company}\n\n"
        for i, paragraph in enumerate(paragraphs, 1):
            user_message += f"Paragraph {i}:\n{paragraph}\n\n"
        return self.query(self.system_prompt, user_message)

class LLM3Agent(LLMAgent):
    """Step 3: Compiles information from all paragraphs and outputs structured JSON"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """You are tasked with compiling law firm information from multiple paragraph analyses into a single JSON object.

You will receive the analysis results from multiple paragraphs. Your task is to:

1. Identify the most consistent/accurate buyer's representative law firm across all paragraphs
2. Identify the most consistent/accurate seller's representative law firm across all paragraphs  
3. Identify any third-party law firms mentioned
4. Determine if the target company was mentioned in any paragraph

Default values:
- If a law firm is not found or unclear: "unknown"
- If target company presence is unclear: false

Output ONLY a valid JSON object with exactly these keys:
{
  "buyer_firm": "string",
  "seller_firm": "string", 
  "third_party": "string",
  "contains_target_firm": boolean
}

Important:
- Output ONLY the JSON object, no additional text
- Ensure valid JSON formatting (no trailing commas, proper quotes)
- Use "unknown" for missing law firm information
- Use actual law firm names when clearly identified
- For third_party, include the most relevant third-party law firm name"""

    def process(self, paragraph_analyses: List[str]) -> str:
        user_message = "Paragraph analyses to compile:\n\n" + "\n\n---\n\n".join(paragraph_analyses)
        return self.query(self.system_prompt, user_message)

class MultiAgentOrchestrator:
    """Orchestrates the 3-step LLM workflow for Target Company & Law Firm Identification"""
    
    def __init__(self):
        self.llm1 = LLM1Agent()
        self.llm2 = LLM2Agent()
        self.llm3 = LLM3Agent()
    
    def process(self, user_query: str, paragraphs: List[str]) -> Dict[str, Any]:
        """
        Process user query and paragraphs through the 3-step workflow
        
        Args:
            user_query: User's query to check for target company
            paragraphs: List of paragraphs to analyze
            
        Returns:
            Dict with final results or error message
        """
        # Step 1: Check for target company
        step1_result = self.llm1.process(user_query)
        
        # If no target company found, return user message
        if step1_result.startswith("<user_message>"):
            return {"result": step1_result}
        
        # Extract target company name
        target_company = step1_result.replace("The target company is ", "").rstrip(".")
        
        # Step 2: Analyze all 4 paragraphs independently in one LLM2 call
        llm2_analysis = self.llm2.process(paragraphs, target_company)
        
        # Step 3: Compile final JSON from LLM2's analysis of all paragraphs
        final_json = self.llm3.process([llm2_analysis])
        
        try:
            # Validate JSON
            final_result = json.loads(final_json)
            return {
                "target_company": target_company,
                "llm2_analysis": llm2_analysis,
                "final_result": final_result,
                "raw_json": final_json
            }
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse final JSON",
                "raw_output": final_json,
                "target_company": target_company,
                "llm2_analysis": llm2_analysis
            }