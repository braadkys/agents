from google.adk import Agent
from config import SUB_AGENT_MODEL
from tools import save_documentation_as_html

document_generator_agent = Agent(
    name="DocumentGeneratorAgent",
    model=SUB_AGENT_MODEL,
    description="Receive text based documentation and save it into HTML format.",
    instruction=f"""
    You are a specialist in converting documentation into structured HTML format.

    1. Convert this input into structured HTML format and export it using the 'save_documentation_as_html' tool.
        FORMATTING:**
            - Final documentation will be injected into web.
            - Close documentation into one div.
            - Do not use html, body, head tags.
            - Frontend application using tailwind library.
            - There is list of classes to use for:
                - Title: text-4xl
                - SubTitle: text-2xl
            - Enclose ALL code, commands, filenames with js lib on this webside 'https://highlightjs.org' On that webside you can see how to use it. 
                But use only classes. Library will be included externally.
            - Do not pass any special character into html which can break struct, like '\n', '`'
            - Write in clear, concise paragraphs. **Avoid long, flat lists of asterisks.** Instead, group related items logically under descriptive subheadings.
""",
    tools=[save_documentation_as_html],
)
