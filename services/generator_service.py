"""
Service layer for the Canva to HTML generation process
"""
import os
from models.state import AgentState
from agents.workflow import create_agent_graph
from utils.image_utils import image_to_base64, get_local_images
import config


class GeneratorService:
    """Service class for handling the generation process"""

    @staticmethod
    def process_image(image, api_provider):
        """Process the uploaded image and generate HTML/CSS"""
        if image is None:
            return "Please upload an image!", "", ""

        # Check API keys
        if api_provider == "gemini" and not config.GEMINI_API_KEY:
            return "❌ GEMINI_API_KEY environment variable is not set!", "", ""
        elif api_provider == "openrouter" and not config.OPENROUTER_API_KEY:
            return "❌ OPENROUTER_API_KEY environment variable is not set!", "", ""

        try:
            # Get local images info
            local_images = get_local_images()
            images_msg = f"📁 Found {len(local_images)} images in local folder\n" if local_images else "⚠️ No local images found, will use fallback sources\n"

            image_base64 = image_to_base64(image)

            initial_state = {
                "image_base64": image_base64,
                "design_analysis": "",
                "color_palette": {},
                "layout_structure": {},
                "typography": {},
                "images_detected": [],
                "html_code": "",
                "css_code": "",
                "refinement_notes": [],
                "iteration_count": 0,
                "messages": [],
                "progress_log": f"🚀 Starting generation process with {api_provider.upper()}...\n{images_msg}",
                "api_provider": api_provider,
                "local_images": local_images
            }

            agent = create_agent_graph()
            final_state = agent.invoke(initial_state)

            progress_log = final_state.get("progress_log", "")
            html_code = final_state.get("html_code", "")
            design_analysis = final_state.get("design_analysis", "")

            return progress_log, html_code, design_analysis

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nPlease check your API keys in environment variables."
            return error_msg, "", ""

    @staticmethod
    def save_html(html_code):
        """Save HTML code to a file"""
        if not html_code:
            return None

        output_file = config.OUTPUT_FOLDER / "generated_template.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_code)

        return output_file