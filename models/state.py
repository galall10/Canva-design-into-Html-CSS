"""
Agent state definitions for the LangGraph workflow
"""
from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    """State for the Canva to HTML generation workflow"""
    image_base64: str
    design_analysis: str
    color_palette: Dict[str, Any]
    layout_structure: Dict[str, Any]
    typography: Dict[str, Any]
    images_detected: List[Dict[str, Any]]
    html_code: str
    css_code: str
    refinement_notes: List[str]
    iteration_count: int
    messages: Annotated[List[str], operator.add]
    progress_log: str
    api_provider: str
    user_images_base64: Dict[str, str]  # filename: base64 data URI (stored separately, not in LLM context)
    user_images_count: int  # Just the count for LLM to know how many images available