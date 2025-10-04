"""
Gradio UI interface for the Canva to HTML generator
"""
import gradio as gr
from services.generator_service import GeneratorService
import config


def create_ui():
    """Create the Gradio interface"""

    with gr.Blocks(
            title="Canva Template to HTML/CSS Generator",
            theme=gr.themes.Soft(primary_hue="orange", secondary_hue="gray")
    ) as demo:
        gr.Markdown(
            f"""
            # 🎨 Canva Template to HTML/CSS Generator

            Upload a Canva template image and your own images to generate a **fully self-contained** HTML file!

            ### 🚀 How to use:
            1. Choose your AI provider (OpenRouter or Google Gemini)
            2. Upload a Canva template image (JPG, PNG) - the design to replicate
            3. Upload your images (JPG, PNG) - these will be embedded in the HTML
            4. Click "Generate Code"
            5. Download the generated HTML file (completely self-contained with base64 images)

            ### 🖼️ Image Handling:
            - Upload multiple images that you want to use in the design
            - Images are automatically converted to base64 and embedded in HTML
            - **No external dependencies** - the HTML file contains everything
            - The AI will intelligently match your images to design elements
            - Supports JPG, PNG, and other common formats

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
                    label="📤 Upload Canva Template (Design to Replicate)",
                    type="pil",
                    height=300
                )

                gr.Markdown("### 🖼️ Upload Your Images")
                gr.Markdown("Upload images you want to use in the generated design. They will be embedded as base64.")

                user_images_input = gr.Gallery(
                    label="Your Images (will be embedded in HTML)",
                    type="pil",
                    columns=3,
                    height=300,
                    allow_preview=True
                )

                generate_btn = gr.Button(
                    "✨ Generate Self-Contained HTML",
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
                gr.Markdown("**Note:** All images are embedded as base64 - no external files needed!")

                html_output = gr.Code(
                    label="Complete Self-Contained HTML File",
                    language="html",
                    lines=20,
                    interactive=True
                )

                download_btn = gr.File(
                    label="💾 Download HTML File (Fully Self-Contained)",
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
            inputs=[image_input, user_images_input, api_provider],
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
            - ✏️ Typography detection
            - 🖼️ **Base64 image embedding (no external dependencies)**
            - 📱 Responsive design generation
            - ✨ Modern CSS with animations
            - ♿ Accessibility-ready code
            - 🤖 Support for multiple AI providers (OpenRouter & Google Gemini)
            - 🔒 Secure API key management via environment variables
            - 📦 **Completely self-contained HTML output**

            **Powered by:** LangGraph • OpenRouter • Google Gemini • Gradio
            """
        )

    return demo