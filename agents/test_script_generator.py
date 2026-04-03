import os
from typing import Optional, List, Dict, Any
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-pro"
llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model=GEMINI_MODEL)

def build_prompt(test_cases, reviewer_feedback=None):
    prompt = """
You are a Senior QA Automation Engineer.
Your task is to generate Java test scripts for the following test cases.
"""
    if reviewer_feedback:
        prompt += f"\nReviewer Feedback: {reviewer_feedback}\n"
    prompt += f"\nTest Cases (JSON):\n{test_cases}\n"
    prompt += """
\nGenerate:
- Selenium Java code for UI test cases
- RestAssured Java code for API test cases

Output a JSON object with two keys:
- selenium_scripts: Java code as a string (or list of strings if multiple classes)
- restassured_scripts: Java code as a string (or list of strings if multiple classes)

Be concise, context-aware, and avoid hallucination. Output only valid JSON.
"""
    return prompt

def generate_test_scripts(test_cases: List[Dict[str, Any]], reviewer_feedback: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate Java test scripts using Gemini LLM. Returns a dict with Java code.
    """
    logger.info("Generating test scripts with context and feedback.")
    prompt = build_prompt(test_cases, reviewer_feedback)
    response = llm.invoke(prompt)
    logger.info("LLM response: {}", response.content)
    try:
        import json
        return json.loads(response.content)
    except Exception as e:
        logger.error(f"Failed to parse LLM output as JSON: {e}")
        return {"error": "Invalid LLM output", "raw_output": response.content}
