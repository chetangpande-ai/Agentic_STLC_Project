import os
from typing import Optional, Dict, Any
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
 # ChatPromptTemplate import removed; using f-string for prompt
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print("GOOGLE_API_KEY =", GOOGLE_API_KEY)
#GEMINI_MODEL = "gemini-pro"  # Use the recommended Gemini model name
GEMINI_MODEL = "gemini-2.5-flash"  # Use the recommended Gemini model name

# Initialize Gemini LLM via LangChain
llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model=GEMINI_MODEL)


def build_prompt(requirement_raw, application_context, reviewer_feedback):
    prompt = """
You are a Senior QA Automation Engineer.
Your task is to analyze the following software requirement and application context.
"""
    if reviewer_feedback:
        prompt += f"\nReviewer Feedback: {reviewer_feedback}\n"
    prompt += f"\nRequirement:\n{requirement_raw}\n"
    prompt += f"\nApplication Context:\n{application_context}\n"
    prompt += """
\nAnalyze and provide:
- Functional requirements
- Edge cases
- Risks
- Missing requirements
\nBe concise, context-aware, and avoid hallucination. Output as a structured JSON object with keys: functional_requirements, edge_cases, risks, missing_requirements.
"""
    return prompt

def analyze_requirement(requirement_raw: str, application_context: Optional[Dict[str, Any]] = None, reviewer_feedback: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze requirements using Gemini LLM. Returns structured analysis.
    """
    logger.info("Analyzing requirement with context and feedback.")
    prompt = build_prompt(requirement_raw or "", application_context or {}, reviewer_feedback or "")
    response = llm.invoke(prompt)
    logger.info("LLM response: {}", response.content)
    try:
        import json
        return json.loads(response.content)
    except Exception as e:
        logger.error(f"Failed to parse LLM output as JSON: {e}")
        return {"error": "Invalid LLM output", "raw_output": response.content}
