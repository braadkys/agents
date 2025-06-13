from google.adk import Agent

from config import SUB_AGENT_MODEL
from tools import (
    list_repository_files,
    read_file_content,
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
