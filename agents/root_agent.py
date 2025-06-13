from google.adk import Agent

from agents.code_reader_agent import code_reader_agent
from agents.document_generator_agent import document_generator_agent
from config import ROOT_AGENT_MODEL

project_documentation_team_instruction = f"""
    Your goal is to create documentation for a software project.
    
    There are levels of possible documentations:
        - High-level: A brief overview of the project's purpose and technology stack.
        - Medium-level: A more detailed look at the main components and how they interact.
        - Detailed: An in-depth, file-by-file or module-by-module breakdown.
    
    User have to provide you first level of documentation. If user do not provide it, ask for it.
        
    If user provide you path to project:
        Use CodeReaderAgent to which pass provided path and document level.
    
    If user want to save documentation into file:
        Use DocumentGeneratorAgent. Pass your whole knowledge about scanned projects.  
    
    If user asks for detailed information about the specific files / folder structure / functionality, from already known kontext.
    """

project_documentation_team = Agent(
    name="ProjectDocumentationCoordinator",
    model=ROOT_AGENT_MODEL,  # Your most capable model
    description="Manages the end-to-end process of generating documentation for a software project by coordinating sub-agents.",
    instruction=project_documentation_team_instruction,
    # The coordinator has access to the sub-agents, not the tools directly.
    sub_agents=[code_reader_agent, document_generator_agent],
)
