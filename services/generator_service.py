"""
Service layer for the Canva to HTML generation process
"""
from models.state import AgentState
from agents.workflow import create_agent_graph
from utils.image_utils import image_to_base64, pil_to_base64_data_uri
import config


class GeneratorService:
    """Service class for handling the generation process"""

    @staticmethod
    def process_image(image, user_images_list, api_provider):
        """Process the uploaded image and generate HTML/CSS with user-provided images"""
        if image is None:
            return "Please upload a design template image!", "", ""

        # Check API keys
        if api_provider == "gemini" and not config.GEMINI_API_KEY:
            return "GEMINI_API_KEY environment variable is not set!", "", ""
        elif api_provider == "openrouter" and not config.OPENROUTER_API_KEY:
            return "OPENROUTER_API_KEY environment variable is not set!", "", ""

        try:
            # Convert template image to base64
            image_base64 = image_to_base64(image)

            # Process user-uploaded images - store separately from LLM context
            user_images_base64 = {}
            if user_images_list:
                for idx, img in enumerate(user_images_list):
                    if img is not None:
                        # Ensure img is a PIL Image, not a tuple
                        if isinstance(img, tuple):
                            img = img[0] if img[0] is not None else img[1]

                        # Generate filename
                        filename = f"user_image_{idx}"
                        # Convert to base64 data URI (stored separately, NOT sent to LLM)
                        data_uri = pil_to_base64_data_uri(img)
                        user_images_base64[filename] = data_uri

            images_msg = f"🖼️ {len(user_images_base64)} user images ready (will be reused if needed)\n" if user_images_base64 else "⚠️ No user images provided, will use placeholders\n"

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
                "progress_log": f"Starting generation process with {api_provider.upper()}...\n{images_msg}",
                "api_provider": api_provider,
                "user_images_base64": user_images_base64,  # Stored separately
                "user_images_count": len(user_images_base64)  # Only count sent to LLM
            }

            agent = create_agent_graph()
            final_state = agent.invoke(initial_state)

            progress_log = final_state.get("progress_log", "")
            html_code = final_state.get("html_code", "")
            design_analysis = final_state.get("design_analysis", "")

            return progress_log, html_code, design_analysis

        except Exception as e:
            error_msg = f"Error: {str(e)}\n\nPlease check your API keys in environment variables."
            return error_msg, "", ""

    @staticmethod
    def save_html(html_code):
        """Save HTML code to a file"""
        if not html_code:
            return None

        output_file = config.OUTPUT_FOLDER / "generated_template.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_code)

        return str(output_file)  # Convert Path to string for Gradio