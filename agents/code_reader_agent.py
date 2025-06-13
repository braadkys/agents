from google.adk import Agent

from config import SUB_AGENT_MODEL
from agents.go_expert_agent import go_expert_agent
from agents.python_expert_agent import python_expert_agent
from agents.javascript_expert_agent import javascript_expert_agent
from tools import (
    list_repository_files,
    read_file_content,
)

code_reader_agent = Agent(
    name="CodeReaderAgent",
    model=SUB_AGENT_MODEL,
    description="Inspects the file structure of a cloned repository and reads the content of relevant files.",
    instruction=f"""
    
    You are a specialist in analyzing source code repositories.
    Your input will be text based documentation of code project.

    1. First, use the 'list_repository_files' tool to understand the project's structure
    2. Analyze the file list and identify the most important files for understanding the project (e.g., README.md, package.json, requirements.txt, main application files).
    3. Read the content of these key files using the 'read_file_content' tool one by one.
    4. Synthesize the file structure and the content of the key files into a single, comprehensive text block for next processing.
        
""",
    sub_agents=[go_expert_agent, python_expert_agent, javascript_expert_agent],
    tools=[list_repository_files, read_file_content],
)


# 5. Decide what type of stack is scanned project.
#         a. For Golang use GoExpertAgent. Pass the compiled context to the Agent. It will prepare deep documentation of project.
#         b. For Python use PythonExpertAgent. Pass the compiled context to the Agent. It will prepare deep documentation of project.
#         b. For Javascript or Typescript use JavascriptExpertAgent. Pass the compiled context to the Agent. It will prepare deep documentation of project.