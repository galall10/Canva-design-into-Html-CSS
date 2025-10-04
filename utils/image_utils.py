"""
Image processing utilities for the Canva to HTML generator
"""
import base64
import io
from PIL import Image
from typing import Dict, Set

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def pil_to_base64_data_uri(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL Image to base64 data URI for embedding in HTML"""
    buffered = io.BytesIO()

    # Determine format from image or use provided format
    if hasattr(image, 'format') and image.format:
        format = image.format.upper()

    # Ensure format is valid
    if format.upper() not in ['PNG', 'JPEG', 'JPG', 'GIF', 'WEBP']:
        format = 'PNG'

    # Convert JPEG to JPG for MIME type
    mime_format = format.lower()
    if mime_format == 'jpeg':
        mime_format = 'jpg'

    # Save image to buffer
    try:
        image.save(buffered, format=format)
    except:
        # Fallback to PNG if format fails
        image.save(buffered, format='PNG')
        mime_format = 'png'

    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return f"data:image/{mime_format};base64,{img_base64}"

def get_next_user_image_placeholder(image_index: int, used_count: int, total_images: int) -> str:
    """
    Return a placeholder reference instead of actual base64.
    This keeps the LLM context small.
    Images can be reused - we cycle through available images.
    """
    if total_images == 0:
        return "{{IMAGE_PLACEHOLDER_SVG}}"

    # Cycle through available images (allows reuse)
    actual_index = image_index % total_images
    return f"{{{{USER_IMAGE_{actual_index}}}}}"

def replace_image_placeholders(html_code: str, user_images_base64: Dict[str, str]) -> str:
    """
    Replace placeholder tokens with actual base64 data URIs in the final HTML.
    This happens AFTER all LLM processing to keep context small.
    """
    # Replace SVG placeholder
    svg_placeholder = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect width='800' height='600' fill='%23ddd'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' fill='%23999' font-size='24'%3EImage Placeholder%3C/text%3E%3C/svg%3E"
    html_code = html_code.replace("{{IMAGE_PLACEHOLDER_SVG}}", svg_placeholder)

    # Replace user image placeholders with actual base64
    for idx, (filename, data_uri) in enumerate(user_images_base64.items()):
        placeholder = f"{{{{USER_IMAGE_{idx}}}}}"
        html_code = html_code.replace(placeholder, data_uri)

    return html_code