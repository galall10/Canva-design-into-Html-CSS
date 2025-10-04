# 🎨 Canva Template → HTML/CSS Generator

Convert your Canva designs into production-ready, responsive HTML/CSS using AI-powered analysis.

## 📋 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Optimization](#-optimization)
- [Use Cases](#-use-cases)

## ✨ Features

- **AI Design Analysis**: Extracts layout, colors, fonts, and visual elements.
- **Base64 Embedding**: All images embedded in one HTML file.
- **Responsive CSS**: Mobile-friendly layouts using Flexbox/Grid.
- **Accessibility Ready**: Semantic HTML and ARIA support.
- **Smart Image Placement**: Matches uploaded images contextually.
- **Multi-Provider Support**: Works with OpenRouter or Google Gemini.
- **Single File Output**: Self-contained, production-ready HTML.

## 🔄 How It Works

1.  **Upload Design**: AI analyzes the Canva layout.
2.  **Extract Elements**: Detects colors, fonts, structure, and images.
3.  **Generate HTML/CSS**: Produces semantic, responsive code.
4.  **Embed Images**: Converts assets to Base64.
5.  **Output**: One complete `.html` file ready to deploy.

## ⚙️ Configuration

Edit `config.py` to adjust model and output settings:

```python
OPENROUTER_MODEL = "qwen/qwen2.5-vl-72b-instruct:free"
GEMINI_MODEL = "gemini-2.0-flash-exp"
OUTPUT_FOLDER = BASE_DIR / "output"
MAX_ITERATIONS = 2
```

## 📁 Project Structure

```
canva-to-html-generator/
├── agents/ # AI workflow nodes
├── models/ # State management
├── prompts/ # Prompt templates
├── services/ # Code generation logic
├── ui/ # Gradio interface
├── utils/ # Image & LLM utilities
├── output/ # Generated files
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## 🛠️ Technology Stack

**Core Frameworks:**

-   [LangGraph](https://langchain.github.io/langgraph/): AI workflow orchestration.
-   [LangChain](https://www.langchain.com/): LLM integration.
-   [Gradio](https://www.gradio.app/): Web UI interface.

**AI Providers:**

-   OpenRouter (Qwen)
-   Google Gemini

**Image Processing:**

-   Pillow (PIL)
-   Base64 embedding

**Python Libraries:**

-   `dotenv`: Environment management.
-   `pydantic`: Data validation.

## ⚡ Optimization

-   Two-phase image handling for minimal token use.
-   Recommended: images under 500 KB.
-   **Gemini**: Faster and high-quality.
-   **OpenRouter**: Free and flexible.
-   Cached results for similar designs.

## 🎯 Use Cases

-   Landing pages & portfolios
-   Email templates
-   App mockups
-   Styled reports
-   Educational materials
