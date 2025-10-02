"""
Gradio UI interface for the Canva to HTML generator
"""
import gradio as gr
from services.generator_service import GeneratorService
from utils.image_utils import get_local_images
import config


def create_ui():
    """Create the Gradio interface"""
    local_images = get_local_images()
    images_status = f"✅ {len(local_images)} images available" if local_images else "⚠️ No images in folder"

    with gr.Blocks(
            title="Canva Template to HTML/CSS Generator",
            theme=gr.themes.Soft(primary_hue="orange", secondary_hue="gray")
    ) as demo:
        gr.Markdown(
            f"""
            # 🎨 Canva Template to HTML/CSS Generator

            Upload a Canva template image and let AI generate production-ready HTML/CSS code with local images!

            ### 🚀 How to use:
            1. Choose your AI provider (OpenRouter or Google Gemini)
            2. Upload a Canva template image (JPG, PNG)
            3. Click "Generate Code"
            4. Download the generated HTML file

            ### 🖼️ Image Handling:
            - Uses images from the local `images/` folder
            - {images_status} in `images/` folder
            - Automatically matches images to design elements
            - Generates responsive, optimized image code

            ### 🔑 API Keys:
            API keys are loaded from environment variables:
            - **OpenRouter**: `OPENROUTER_API_KEY` {'✅' if config.OPENROUTER_API_KEY else '❌'}
            - **Google Gemini**: `GEMINI_API_KEY` {'✅' if config.GEMINI_API_KEY else '❌'}

            ---
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                api_provider = gr.Radio(
                    choices=["openrouter", "gemini"],
                    value=config.DEFAULT_API_PROVIDER,
                    label="🤖 AI Provider",
                    info="Choose your preferred AI provider"
                )

                image_input = gr.Image(
                    label="📤 Upload Canva Template",
                    type="pil",
                    height=400
                )

                generate_btn = gr.Button(
                    "✨ Generate Code",
                    variant="primary",
                    size="lg"
                )

                progress_output = gr.Textbox(
                    label="📊 Progress Log",
                    lines=10,
                    max_lines=15,
                    interactive=False
                )

            with gr.Column(scale=1):
                gr.Markdown("### 📝 Generated HTML/CSS Code")

                html_output = gr.Code(
                    label="Complete HTML File",
                    language="html",
                    lines=20,
                    interactive=True
                )

                download_btn = gr.File(
                    label="💾 Download HTML File",
                    interactive=False
                )

                with gr.Accordion("🔍 Design Analysis", open=False):
                    analysis_output = gr.Textbox(
                        label="AI Design Analysis",
                        lines=10,
                        interactive=False
                    )

        generate_btn.click(
            fn=GeneratorService.process_image,
            inputs=[image_input, api_provider],
            outputs=[progress_output, html_output, analysis_output]
        )

        html_output.change(
            fn=GeneratorService.save_html,
            inputs=[html_output],
            outputs=[download_btn]
        )

        gr.Markdown(
            """
            ---
            ### 📚 About

            This tool uses **LangGraph** and **Vision AI** to analyze design templates and generate code.

            **Features:**
            - 🎨 Automatic color palette extraction
            - 📐 Layout structure analysis
            - ✍️ Typography detection
            - 🖼️ **Automatic image detection with local image support**
            - 📱 Responsive design generation
            - ✨ Modern CSS with animations
            - ♿ Accessibility-ready code
            - 🤖 Support for multiple AI providers (OpenRouter & Google Gemini)
            - 🔒 Secure API key management via environment variables

            **Powered by:** LangGraph • OpenRouter • Google Gemini • Gradio
            """
        )

    return demo