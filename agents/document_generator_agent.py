from google.adk import Agent
from config import SUB_AGENT_MODEL
from tools import (
    save_documentation_as_html,
)

document_generator_agent = Agent(
    name="DocumentGeneratorAgent",
    model=SUB_AGENT_MODEL,
    description="Receive text based documentation and save it into HTML format.",
    instruction=f"""
    
    You are a specialist in converting html based documentation into structured HTML format.
    
    1. Convert this input into structured HTML format and export it using the 'save_documentation_as_html' tool.
        FORMATTING:**
            - Use headings (`<h2>`, `<h3>`) to create a clear hierarchy.
            - Enclose ALL code, commands, filenames with js lib on this webside 'https://highlightjs.org' On that webside you can see how to use it.
            - Use full code blocks with language identifiers (e.g., ```python) for all multi-line code snippets.
            - Write in clear, concise paragraphs. **Avoid long, flat lists of asterisks.** Instead, group related items logically under descriptive subheadings.
""",
    tools=[save_documentation_as_html],
)
