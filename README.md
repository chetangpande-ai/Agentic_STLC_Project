
# QA AI Automation System


## Architecture Diagram

```mermaid
graph TD
	A[Fetch Requirement from ADO] --> B[Requirement Analyzer Agent]
	B --> C[Human Review (Requirement)]
	C --> D[Test Case Generator Agent]
	D --> E[Human Review (Test Cases)]
	E --> F[Test Script Generator Agent]
	F --> G[Human Review (Scripts)]
	G --> H[Export Outputs (Excel + Java files)]
	H --> I[End]
```

## Overview
A modular, production-grade AI-powered QA Automation System using Python, LangGraph, and Gemini LLM.

## Setup
1. Python 3.10+
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Fill in `.env` with your API keys and ADO credentials

## Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key
- `ADO_ORG_URL`: Azure DevOps organization URL
- `ADO_PAT`: Azure DevOps Personal Access Token
