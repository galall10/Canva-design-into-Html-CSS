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