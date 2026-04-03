import os
from typing import Optional, Dict, Any, List
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model=GEMINI_MODEL)

def build_prompt(requirement_analysis, reviewer_feedback=None):
    prompt = """
You are a Senior QA Automation Engineer.
Your task is to generate structured test cases based on the following requirement analysis.
"""
    if reviewer_feedback:
        prompt += f"\nReviewer Feedback: {reviewer_feedback}\n"
    prompt += f"\nRequirement Analysis:\n{requirement_analysis}\n"
    prompt += """
\nGenerate a list of test cases in JSON format. Each test case should have:
- test_case_id
- title
- steps
- expected_result
- priority (High, Medium, Low)
Be concise, context-aware, and avoid hallucination. Output only valid JSON.
"""
    return prompt

def generate_test_cases(requirement_analysis: Dict[str, Any], reviewer_feedback: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generate structured test cases using Gemini LLM. Returns a list of test cases.
    """
    logger.info("Generating test cases with context and feedback.")
    prompt = build_prompt(requirement_analysis, reviewer_feedback)
    response = llm.invoke(prompt)
    logger.info("LLM response: {}", response.content)
    try:
        import json
        return json.loads(response.content)
    except Exception as e:
        logger.error(f"Failed to parse LLM output as JSON: {e}")
        return [{"error": "Invalid LLM output", "raw_output": response.content}]
