"""
Image processing utilities for the Canva to HTML generator
"""
import base64
import io
import os
import random
from pathlib import Path
from PIL import Image
from typing import Set
import config

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_local_images() -> list[str]:
    """Get list of all images from the local images folder"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    images = []

    for file in os.listdir(config.LOCAL_IMAGES_FOLDER):
        if Path(file).suffix.lower() in image_extensions:
            images.append(file)

    return sorted(images)

def get_local_image_path(image_type: str, used_images: Set[str]) -> str:
    """Get a local image path based on image type"""
    local_images = get_local_images()

    if not local_images:
        return f"https://source.unsplash.com/800x600/?{image_type}"

    category_keywords = {
        "people": ["people", "person", "portrait", "team", "human", "face"],
        "business": ["business", "office", "work", "corporate", "meeting"],
        "technology": ["tech", "computer", "digital", "device", "laptop"],
        "nature": ["nature", "landscape", "tree", "mountain", "forest", "outdoor"],
        "food": ["food", "cuisine", "meal", "dish", "restaurant"],
        "product": ["product", "item", "object", "minimal"],
        "abstract": ["abstract", "pattern", "texture", "background"],
    }

    image_type_lower = image_type.lower()
    matched_images = []

    for category, keywords in category_keywords.items():
        if category in image_type_lower or any(kw in image_type_lower for kw in keywords):
            matched_images = [img for img in local_images
                            if any(kw in img.lower() for kw in keywords)
                            and img not in used_images]
            if matched_images:
                break

    if not matched_images:
        matched_images = [img for img in local_images if img not in used_images]

    if not matched_images:
        matched_images = local_images

    selected_image = random.choice(matched_images)
    return f"./images/{selected_image}"