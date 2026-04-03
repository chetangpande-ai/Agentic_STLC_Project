from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field

class WorkflowState(BaseModel):
    """
    Central state object for the QA AI Automation System workflow.
    Tracks all data and feedback across pipeline stages.
    """
    requirement_raw: Optional[str] = Field(None, description="Raw requirement text fetched from ADO.")
    application_context: Optional[Dict[str, Any]] = Field(None, description="Application context information.")
    requirement_analysis: Optional[Dict[str, Any]] = Field(None, description="Output of the requirement analyzer agent.")
    test_cases: Optional[List[Dict[str, Any]]] = Field(None, description="List of generated test cases.")
    test_scripts: Optional[Dict[str, Any]] = Field(None, description="Generated Java test scripts (Selenium/RestAssured).")
    reviewer_feedback: Optional[Dict[str, Any]] = Field(None, description="Reviewer feedback for each stage.")
    current_stage: str = Field(..., description="Current stage in the workflow.")

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
