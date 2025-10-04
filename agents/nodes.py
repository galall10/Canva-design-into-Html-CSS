"""
Agent nodes for the LangGraph workflow
"""
import json
from langchain_core.messages import HumanMessage, SystemMessage
from models.state import AgentState
from utils.llm_factory import initialize_llm
from utils.image_utils import get_next_user_image_placeholder
from prompts.templates import *

def analyze_design_node(state: AgentState) -> AgentState:
    """Analyze the design template and extract key elements including images"""
    progress_msg = "Analyzing design template...\n"
    state["progress_log"] = state.get("progress_log", "") + progress_msg

    image_data = state.get("image_base64", "")
    api_provider = state.get("api_provider", "openrouter")

    llm = initialize_llm(api_provider)

    response = llm.invoke([
        HumanMessage(content=[
            {"type": "text", "text": DESIGN_ANALYSIS_PROMPT + "\n\nAnalyze this design template in detail:"},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
        ])
    ])

    state["design_analysis"] = response.content
    state["messages"].append("Design analysis complete")
    state["progress_log"] += "Design analysis complete\n"

    return state

def extract_design_elements_node(state: AgentState) -> AgentState:
    """Extract specific design elements including images"""
    progress_msg = "Extracting design elements and preparing image slots...\n"
    state["progress_log"] += progress_msg

    api_provider = state.get("api_provider", "openrouter")
    llm = initialize_llm(api_provider)

    extraction_prompt = ELEMENTS_EXTRACTION_PROMPT.format(
        design_analysis=state['design_analysis']
    )

    messages = [
        SystemMessage(content=extraction_prompt),
        HumanMessage(content="Extract the design elements now.")
    ]

    response = llm.invoke(messages)

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        elements = json.loads(content)
        state["color_palette"] = elements.get("colors", {})
        state["typography"] = elements.get("typography", {})
        state["layout_structure"] = elements.get("layout", {})

        # Process detected images and assign placeholder tokens (NOT base64!)
        images_detected = elements.get("images", [])
        user_images_count = state.get("user_images_count", 0)

        for idx, img in enumerate(images_detected):
            # Use lightweight placeholder token instead of heavy base64
            img["url"] = get_next_user_image_placeholder(idx, idx, user_images_count)

        state["images_detected"] = images_detected

    except (json.JSONDecodeError, Exception) as e:
        # Fallback default values
        state.update({
            "color_palette": {
                "primary": "#FF6B35",
                "secondary": "#F7F7F7",
                "accent": "#004E89",
                "background": "#FFFFFF",
                "text": "#000000"
            },
            "typography": {
                "heading": {"family": "Arial, sans-serif", "weight": "bold"},
                "body": {"family": "Arial, sans-serif", "weight": "normal"}
            },
            "layout_structure": {"type": "flex", "columns": 2},
            "images_detected": []
        })

    state["messages"].append("Design elements extracted")
    state["progress_log"] += f"Design elements extracted ({len(state['images_detected'])} image slots prepared)\n"

    return state

def generate_html_node(state: AgentState) -> AgentState:
    """Generate semantic HTML structure with image placeholder tokens"""
    progress_msg = "Generating HTML structure with image placeholders...\n"
    state["progress_log"] += progress_msg

    api_provider = state.get("api_provider", "openrouter")
    llm = initialize_llm(api_provider)

    images_info = json.dumps(state["images_detected"], indent=2) if state["images_detected"] else "No images detected"

    html_prompt = f"""You are an expert frontend developer. Generate clean, semantic HTML5 code for this design:

Design Analysis: {state['design_analysis']}
Layout Structure: {json.dumps(state['layout_structure'], indent=2)}

IMAGES TO INCLUDE (use placeholder tokens):
{images_info}

Requirements:
- Use semantic HTML5 tags (header, section, article, etc.)
- Include proper accessibility attributes (alt, aria-labels)
- Create a responsive structure
- Use meaningful class names following BEM methodology
- Include all text content visible in the original design
- **IMPORTANT**: For each image, use the placeholder token from the "url" field in the src attribute
  Example: <img src="{{{{USER_IMAGE_0}}}}" alt="Description">
- DO NOT try to generate actual base64 data - just use the placeholder tokens exactly as provided
- Structure should match the Canva template exactly
- DO NOT include any CSS in this response

Generate ONLY the HTML code structure, no explanations. Start with <!DOCTYPE html> and include a <head> section with meta tags."""

    messages = [
        SystemMessage(content=html_prompt),
        HumanMessage(content="Generate the HTML structure now with image placeholder tokens.")
    ]

    response = llm.invoke(messages)
    html_content = response.content.strip()

    if "```html" in html_content:
        html_content = html_content.split("```html")[1].split("```")[0].strip()
    elif "```" in html_content:
        html_content = html_content.split("```")[1].split("```")[0].strip()

    state["html_code"] = html_content
    state["messages"].append("HTML generated with image placeholders")
    state["progress_log"] += "HTML generated with image placeholders\n"

    return state


def generate_css_node(state: AgentState) -> AgentState:
    """Generate CSS styling"""
    progress_msg = "Generating CSS styles...\n"
    state["progress_log"] += progress_msg

    api_provider = state.get("api_provider", "openrouter")
    llm = initialize_llm(api_provider)

    css_prompt = f"""You are an expert CSS developer. Generate modern, responsive CSS for this HTML structure:

HTML Structure Preview:
{state['html_code'][:800]}...

Design Specifications:
- Colors: {json.dumps(state['color_palette'], indent=2)}
- Typography: {json.dumps(state['typography'], indent=2)}
- Layout: {json.dumps(state['layout_structure'], indent=2)}

Requirements:
- Use modern CSS (Flexbox/Grid)
- Implement the exact color scheme from the template
- Match typography styles and hierarchy
- Create responsive design with media queries
- Use CSS custom properties for colors and spacing
- Add smooth transitions and hover effects
- Ensure pixel-perfect alignment and spacing
- Style images properly (object-fit, aspect ratios, rounded corners if needed)
- Make images responsive (max-width: 100%, height: auto)
- Add loading states for images
- Make it production-ready
- Include styles for all elements in the HTML

Generate ONLY the CSS code (without <style> tags), no explanations."""

    messages = [
        SystemMessage(content=css_prompt),
        HumanMessage(content="Generate the CSS styles now.")
    ]

    response = llm.invoke(messages)
    css_content = response.content.strip()

    if "```css" in css_content:
        css_content = css_content.split("```css")[1].split("```")[0].strip()
    elif "```" in css_content:
        css_content = css_content.split("```")[1].split("```")[0].strip()

    css_content = css_content.replace("<style>", "").replace("</style>", "").strip()

    state["css_code"] = css_content
    state["messages"].append("CSS generated")
    state["progress_log"] += "CSS generated\n"

    return state


def combine_code_node(state: AgentState) -> AgentState:
    """Combine HTML and CSS into a complete self-contained file"""
    progress_msg = "🔧 Combining HTML and CSS...\n"
    state["progress_log"] += progress_msg

    html = state["html_code"]
    css = state["css_code"]

    if "</head>" in html:
        style_tag = f"\n<style>\n{css}\n</style>\n"
        html = html.replace("</head>", f"{style_tag}</head>")
    else:
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Template</title>
    <style>
{css}
    </style>
</head>
<body>
{html}
</body>
</html>"""

    state["html_code"] = html
    state["messages"].append("Code combined")
    state["progress_log"] += "Code combined (fully self-contained)\n"

    return state


def refine_code_node(state: AgentState) -> AgentState:
    """Refine and optimize the generated code"""
    progress_msg = "✨ Refining code...\n"
    state["progress_log"] += progress_msg

    api_provider = state.get("api_provider", "openrouter")
    llm = initialize_llm(api_provider)

    refinement_prompt = f"""Review and refine this HTML/CSS code to ensure it perfectly matches the original Canva template:

Current Code:
{state['html_code']}

Original Design Analysis:
{state['design_analysis']}

Images: {len(state.get('images_detected', []))} image placeholders (will be replaced with base64 later)

Tasks:
1. Verify all visual elements are present including image placeholders
2. Check color accuracy against the original design
3. Ensure images are properly styled and responsive
4. Ensure responsive behavior
5. Optimize code structure
6. Fix any alignment or spacing issues
7. Add any missing hover states or interactions
8. Ensure the design looks modern and professional
9. Keep image placeholder tokens intact ({{{{USER_IMAGE_X}}}})
10. DO NOT try to generate actual base64 data

Provide the refined COMPLETE HTML file (with embedded CSS) that's production-ready. Make sure it closely matches the original Canva template design."""

    messages = [
        SystemMessage(content=refinement_prompt),
        HumanMessage(content="Refine the code now.")
    ]

    response = llm.invoke(messages)
    refined_code = response.content.strip()

    if "```html" in refined_code:
        refined_code = refined_code.split("```html")[1].split("```")[0].strip()
    elif "```" in refined_code:
        refined_code = refined_code.split("```")[1].split("```")[0].strip()

    if "<!DOCTYPE html>" in refined_code or "<html" in refined_code:
        state["html_code"] = refined_code

    state["iteration_count"] = state.get("iteration_count", 0) + 1
    state["messages"].append("Code refined")
    state["progress_log"] += "Code refined and optimized\n"

    return state

def output_node(state: AgentState) -> AgentState:
    """Final output node - replace placeholders with actual base64"""
    state["messages"].append("Embedding base64 images...")
    state["progress_log"] += "Replacing placeholders with base64 images...\n"

    # NOW we replace the lightweight placeholders with actual base64 data
    from utils.image_utils import replace_image_placeholders
    user_images_base64 = state.get("user_images_base64", {})
    state["html_code"] = replace_image_placeholders(state["html_code"], user_images_base64)

    state["messages"].append("Generation complete!")
    state["progress_log"] += "Generation complete! HTML file is fully self-contained.\n"
    return state