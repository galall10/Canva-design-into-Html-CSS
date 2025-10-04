"""
Main application entry point for Canva to HTML Generator
"""
from ui.gradio_interface import create_ui
import config

def main():
    """Launch the Gradio interface"""
    print("=" * 50)
    print("Canva Template to HTML/CSS Generator")
    print("Self-Contained Version (Base64 Images)")
    print("=" * 50)
    print(f"OpenRouter API Key: {'Set' if config.OPENROUTER_API_KEY else 'Not Set'}")
    print(f"Gemini API Key: {'Set' if config.GEMINI_API_KEY else 'Not Set'}")
    print(f"Output Folder: {config.OUTPUT_FOLDER}")
    print("=" * 50)
    print("Images will be embedded as base64 (no external files)")
    print("=" * 50)

    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )

if __name__ == "__main__":
    main()