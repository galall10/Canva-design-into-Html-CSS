"""
LangGraph workflow definition for Canva to HTML generation
"""
from langgraph.graph import StateGraph, END
from typing import Literal
from agents.nodes import *
from models.state import AgentState

def should_refine(state: AgentState) -> Literal["refine", "output"]:
    """Decide if we need another refinement iteration"""
    if state.get("iteration_count", 0) < 1:
        return "refine"
    return "output"

def create_agent_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("analyze_design", analyze_design_node)
    workflow.add_node("extract_elements", extract_design_elements_node)
    workflow.add_node("generate_html", generate_html_node)
    workflow.add_node("generate_css", generate_css_node)
    workflow.add_node("combine_code", combine_code_node)
    workflow.add_node("refine", refine_code_node)
    workflow.add_node("output", output_node)

    # Define workflow
    workflow.set_entry_point("analyze_design")
    workflow.add_edge("analyze_design", "extract_elements")
    workflow.add_edge("extract_elements", "generate_html")
    workflow.add_edge("generate_html", "generate_css")
    workflow.add_edge("generate_css", "combine_code")
    workflow.add_edge("combine_code", "refine")

    # Conditional refinement
    workflow.add_conditional_edges(
        "refine",
        should_refine,
        {
            "refine": "generate_html",
            "output": "output"
        }
    )

    workflow.add_edge("output", END)

    return workflow.compile()