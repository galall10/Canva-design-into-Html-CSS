"""
Prompt templates for the AI agents
"""

DESIGN_ANALYSIS_PROMPT = """You are an expert design analyst. Analyze this Canva template image and provide:

1. **Overall Design Style**: Modern, minimal, corporate, creative, etc.
2. **Color Palette**: Extract all colors used (provide hex codes)
3. **Layout Structure**: Describe the grid, sections, and spatial organization
4. **Typography**: Font styles, sizes, hierarchy
5. **Visual Elements**: Icons, shapes, and their purposes
6. **Images Detected**: List ALL images/photos in the design with:
   - Location (header, hero section, gallery, etc.)
   - Purpose (background, product shot, team photo, etc.)
   - Type (person, landscape, product, abstract, etc.)
   - Approximate size/dimensions
7. **Spacing & Alignment**: Padding, margins, and alignment patterns
8. **Key Design Principles**: What makes this design effective

IMPORTANT: Pay special attention to identifying all images and photographs in the template.

Provide your analysis in a detailed, structured format."""

ELEMENTS_EXTRACTION_PROMPT = """Based on this design analysis:

{design_analysis}

Extract and provide in JSON format:
1. **colors**: Array of objects with hex color codes and their usage (primary, secondary, accent, background, text)
2. **typography**: Object with font families, sizes, weights, and where they're used
3. **layout**: Object describing the grid system, sections, and component hierarchy
4. **spacing**: Object with padding and margin values
5. **images**: Array of objects for each image/photo detected with:
   - "location": where the image appears (e.g., "hero-section", "gallery-item-1")
   - "type": category of image (e.g., "person", "product", "landscape", "abstract", "business")
   - "purpose": what the image is for (e.g., "hero-background", "team-member", "product-showcase")
   - "size": approximate dimensions (e.g., "large", "medium", "small")
   - "description": brief description of what should be shown

Return ONLY valid JSON, no additional text or markdown code blocks."""

HTML_GENERATION_PROMPT = """You are an expert frontend developer. Generate clean, semantic HTML5 code for this design:

Design Analysis: {design_analysis}
Layout Structure: {layout_structure}

IMAGES TO INCLUDE (use these exact paths):
{images_info}

Requirements:
- Use semantic HTML5 tags (header, section, article, etc.)
- Include proper accessibility attributes (alt, aria-labels)
- Create a responsive structure
- Use meaningful class names following BEM methodology
- Include all text content visible in the original design
- **IMPORTANT**: For each image detected, use the provided URL in an <img> tag with proper alt text
- Structure should match the Canva template exactly
- DO NOT include any CSS in this response
- Use the exact image paths provided (e.g., ./images/filename.jpg)

Generate ONLY the HTML code structure, no explanations. Start with <!DOCTYPE html> and include a <head> section with meta tags."""

CSS_GENERATION_PROMPT = """You are an expert CSS developer. Generate modern, responsive CSS for this HTML structure:

HTML Structure Preview:
{html_preview}

Design Specifications:
- Colors: {colors}
- Typography: {typography}
- Layout: {layout}

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

REFINEMENT_PROMPT = """Review and refine this HTML/CSS code to ensure it perfectly matches the original Canva template:

Current Code:
{current_code}

Original Design Analysis:
{design_analysis}

Images Used: {images_count} local images

Tasks:
1. Verify all visual elements are present including images
2. Check color accuracy against the original design
3. Ensure images are properly styled and responsive
4. Ensure responsive behavior
5. Optimize code structure
6. Fix any alignment or spacing issues
7. Add any missing hover states or interactions
8. Ensure the design looks modern and professional
9. Keep local image paths intact (./images/filename.ext)

Provide the refined COMPLETE HTML file (with embedded CSS) that's production-ready. Make sure it closely matches the original Canva template design."""