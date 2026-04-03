import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Any, Dict
from loguru import logger
from langgraph.graph import StateGraph, END
from graph.state import WorkflowState
from agents.requirement_analyzer import analyze_requirement
from agents.test_case_generator import generate_test_cases
from agents.test_script_generator import generate_test_scripts

# --- Node 1: Fetch Requirement from ADO (mock) ---
def fetch_requirement_node(state: WorkflowState) -> WorkflowState:
    logger.info("Fetching requirement from ADO (mocked)")
    # Mocked requirement and context
    state.requirement_raw = "The system shall allow users to reset their password via email verification."
    state.application_context = {"platform": "Web", "user_roles": ["admin", "user"], "security": "OAuth2, HTTPS"}
    state.current_stage = "requirement_fetched"
    return state

# --- Node 2: Requirement Analyzer Agent ---
def requirement_analyzer_node(state: WorkflowState) -> WorkflowState:
    logger.info("Running Requirement Analyzer Agent")
    result = analyze_requirement(state.requirement_raw, state.application_context, state.reviewer_feedback.get("requirement") if state.reviewer_feedback else None)
    state.requirement_analysis = result
    state.current_stage = "requirement_analyzed"
    return state

# --- Node 3: Human Review (Requirement) ---
def human_review_requirement_node(state: WorkflowState) -> WorkflowState:
    logger.info("Human review for requirement analysis (mocked as accepted)")
    # In production, collect feedback from UI or CLI
    state.reviewer_feedback = state.reviewer_feedback or {}
    state.reviewer_feedback["requirement"] = None  # No feedback, proceed
    state.current_stage = "requirement_reviewed"
    return state

# --- Node 4: Test Case Generator Agent ---
def test_case_generator_node(state: WorkflowState) -> WorkflowState:
    logger.info("Running Test Case Generator Agent")
    result = generate_test_cases(state.requirement_analysis, state.reviewer_feedback.get("test_cases") if state.reviewer_feedback else None)
    state.test_cases = result
    state.current_stage = "test_cases_generated"
    return state

# --- Node 5: Human Review (Test Cases) ---
def human_review_test_cases_node(state: WorkflowState) -> WorkflowState:
    logger.info("Human review for test cases (mocked as accepted)")
    state.reviewer_feedback = state.reviewer_feedback or {}
    state.reviewer_feedback["test_cases"] = None  # No feedback, proceed
    state.current_stage = "test_cases_reviewed"
    return state

# --- Node 6: Test Script Generator Agent ---
def test_script_generator_node(state: WorkflowState) -> WorkflowState:
    logger.info("Running Test Script Generator Agent")
    result = generate_test_scripts(state.test_cases, state.reviewer_feedback.get("test_scripts") if state.reviewer_feedback else None)
    state.test_scripts = result
    state.current_stage = "test_scripts_generated"
    return state

# --- Node 7: Human Review (Scripts) ---
def human_review_scripts_node(state: WorkflowState) -> WorkflowState:
    logger.info("Human review for test scripts (mocked as accepted)")
    state.reviewer_feedback = state.reviewer_feedback or {}
    state.reviewer_feedback["test_scripts"] = None  # No feedback, proceed
    state.current_stage = "test_scripts_reviewed"
    return state

# --- Node 8: Export Outputs (mock) ---
def export_outputs_node(state: WorkflowState) -> WorkflowState:
    logger.info("Exporting outputs (mocked)")
    # In production, export to Excel and Java files
    state.current_stage = "outputs_exported"
    return state

# --- Build LangGraph Workflow ---
def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("fetch_requirement", fetch_requirement_node)
    graph.add_node("requirement_analyzer", requirement_analyzer_node)
    graph.add_node("human_review_requirement", human_review_requirement_node)
    graph.add_node("test_case_generator", test_case_generator_node)
    graph.add_node("human_review_test_cases", human_review_test_cases_node)
    graph.add_node("test_script_generator", test_script_generator_node)
    graph.add_node("human_review_scripts", human_review_scripts_node)
    graph.add_node("export_outputs", export_outputs_node)

    # Define entrypoint and transitions
        graph.add_edge("__start__", "fetch_requirement")
    graph.add_edge("fetch_requirement", "requirement_analyzer")
    graph.add_edge("requirement_analyzer", "human_review_requirement")
    graph.add_edge("human_review_requirement", "test_case_generator")
    graph.add_edge("test_case_generator", "human_review_test_cases")
    graph.add_edge("human_review_test_cases", "test_script_generator")
    graph.add_edge("test_script_generator", "human_review_scripts")
    graph.add_edge("human_review_scripts", "export_outputs")
    graph.add_edge("export_outputs", END)

    return graph

# --- Example runner ---
if __name__ == "__main__":
    workflow = build_workflow()
    state = WorkflowState(current_stage="start")
    app = workflow.compile()
    result = app.invoke(state)
   # result = workflow.run(state)
    print("\n--- Final Workflow State ---\n")
    print(result.model_dump())
