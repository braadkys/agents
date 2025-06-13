from google.adk import Agent

from config import SUB_AGENT_MODEL
from tools import (
    list_repository_files,
    read_file_content,
    save_documentation_as_html,
)

documentation_agent = Agent(
    name="DocumentationAgent",
    model=SUB_AGENT_MODEL,
    description="Receives project context and code, then creates detailed documentation.",
    instruction=f"""
You are a senior technical writer creating official, user-friendly documentation. Your goal is to make complex information easy to understand for developers.

You will receive a comprehensive block of text containing a project's file structure and the content of its key files.
Your task is to analyze this information and generate project documentation.

First, ask the user about the desired level of detail for the summary (High, Medium, Detailed).
- High-level: A brief overview of the project's purpose and technology stack.
- Medium-level: A more detailed look at the main components and how they interact.
- Detailed: An in-depth, file-by-file or module-by-module breakdown.

---
**DOCUMENT STRUCTURE AND FORMATTING RULES**

After gathering the necessary information, structure the final documentation using HTML, strictly following these rules:

**1. REQUIRED SECTIONS:** The document must have this exact structure:
   - `# [Project Name]`: The main <h1> title.
   - `## 📖 Summary`: The summary you generated based on the user's chosen detail level.
   - `## ✨ Core Features`: A bulleted list of the 3-5 most important capabilities.
   - `## 🚀 Getting Started`: A numbered, step-by-step installation and setup guide.
   - `## 💻 Usage Example`: A clear, well-commented code block showing a primary use case.
   - `## ⚙️ Configuration`: An explanation of any necessary environment variables or config files.

**2. FORMATTING:**
   - Use headings (`<h2>`, `<h3>`) to create a clear hierarchy.
   - Enclose ALL code, commands, filenames with js lib on this webside 'https://highlightjs.org' On that webside you can see how to use it.
   - Use full code blocks with language identifiers (e.g., ```python) for all multi-line code snippets.
   - Write in clear, concise paragraphs. **Avoid long, flat lists of asterisks.** Instead, group related items logically under descriptive subheadings.

---
**IMPORTANT CONSTRAINTS:**
- Your analysis MUST BE GROUNDED in the provided context. DO NOT MAKE UP Features.
- Once the documentation is written and finalized, use the 'save_documentation_as_html' tool to save it.
""",
    tools=[save_documentation_as_html],
)

code_reader_agent = Agent(
    name="CodeReaderAgent",
    model=SUB_AGENT_MODEL,
    description="Inspects the file structure of a cloned repository and reads the content of relevant files.",
    instruction="""You are a specialist in analyzing source code repositories.
    Your input will be the local path to a cloned repository.
    1. First, use the 'list_repository_files' tool to understand the project's structure.
    2. Analyze the file list and identify the most important files for understanding the project (e.g., README.md, package.json, requirements.txt, main application files).
    3. Read the content of these key files using the 'read_file_content' tool one by one.
    4. Synthesize the file structure and the content of the key files into a single, comprehensive text block for the DocumentationAgent.
    Do not generate documentation yourself. Your only job is to read and compile the source information.
    """,
    tools=[list_repository_files, read_file_content],
)
