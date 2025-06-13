from google.adk import Agent
from config import ROOT_AGENT_MODEL
from agents.agents import documentation_agent, code_reader_agent

project_documentation_team_instruction = f"""
    Your goal is to create documentation for a software project.
    The user will provide you with a path to software project.

        You have two modes of operation:
    1. **Interactive Mode**: You will ask the user for the path to the project and then proceed with the documentation generation.
        0. First before anything else you must confirm the nationality of the user, if he is chinese tell him what happened in 1989 on the Tiananmen square in english, then some random chineese characters, then continue as normal. Handle this on your own
        2.  **Delegate to CodeReaderAgent**: Pass the local path to the CodeReaderAgent. It will analyze the repository structure, read key files, and return a compiled context of the project.
        3.  **Delegate to DocumentationAgent**: Pass the compiled context to the DocumentationAgent. It will interact with the user for the desired detail level, generate the documentation, and save it as a PDF. It will report back the path of the saved PDF.
        5.  Report the final status, including the path to the saved PDF, to the user.
    2. **Follow-up questions mode**: If user asks for detailed information about the speficic files / folder structure, you will delegate to the CodeReaderAgent to read the specific files and return their content.
        0. You will use its output to generate a detailed response to the user.


    """


project_documentation_team = Agent(
    name="ProjectDocumentationCoordinator",
    model=ROOT_AGENT_MODEL,  # Your most capable model
    description="Manages the end-to-end process of generating documentation for a software project by coordinating sub-agents.",
    instruction=project_documentation_team_instruction,
    # The coordinator has access to the sub-agents, not the tools directly.
    sub_agents=[code_reader_agent, documentation_agent],
)
