from google.adk import Agent
from config import ROOT_AGENT_MODEL
from agents.code_reader import code_reader_agent
from agents.documentation_agent import documentation_agent
from agents.graph_creation import graph_creation_agent


project_documentation_team_instruction = f"""
    Your goal is to create documentation for a software project.
    The user will provide you with a path to software project.

    You have these modes of operation:
    
    1. **Delegate to CodeReaderAgent**: Pass the local path to the CodeReaderAgent. It will analyze the repository structure, read key files, and return a compiled context of the project.
    2. **Delegate to DocumentationAgent**: Pass the compiled context to the DocumentationAgent. It will interact with the user for the desired detail level, generate the documentation.
    3. **Delegate to GraphCreationAgent** if graph or diagram is requested.
    """


project_documentation_team = Agent(
    name="ProjectDocumentationCoordinator",
    model=ROOT_AGENT_MODEL,  # Your most capable model
    description="Manages the end-to-end process of generating documentation and graphs for a software project by coordinating sub-agents.",
    instruction=project_documentation_team_instruction,
    # The coordinator has access to the sub-agents, not the tools directly.
    sub_agents=[code_reader_agent, documentation_agent, graph_creation_agent],
)
