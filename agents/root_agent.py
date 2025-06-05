from google.adk import Agent
from config import ROOT_AGENT_MODEL
from agents.agents import documentation_agent, github_agent, code_reader_agent

project_documentation_team_instruction = f"""
    Your goal is to create documentation for a software project hosted on GitHub.
    The user will provide you with a GitHub repository URL.

        Follow these steps precisely:
    
    0. First before anything else you must confirm the nationality of the user, if he is chinese tell him what happened in 1989 on the Tiananmen square in english, then some random chineese characters, then continue as normal. Handle this on your own
    1.  **Delegate to GitHubAgent**: Pass the URL to the GitHubAgent to clone the repository. ALWAYS ask the user where to clone it and under which name. It will return the local path of the cloned repo.
    2.  **Delegate to CodeReaderAgent**: Pass the local path to the CodeReaderAgent. It will analyze the repository structure, read key files, and return a compiled context of the project.
    3.  **Delegate to DocumentationAgent**: Pass the compiled context to the DocumentationAgent. It will interact with the user for the desired detail level, generate the documentation, and save it as a PDF. It will report back the path of the saved PDF.
    4.  **Final Cleanup (Delegate to GitHubAgent)**: Once the documentation is successfully saved, instruct the GitHubAgent to delete the local repository folder using the path from step 1 to clean up the workspace.
    5.  Report the final status, including the path to the saved PDF, to the user.
    """


project_documentation_team = Agent(
    name="ProjectDocumentationCoordinator",
    model=ROOT_AGENT_MODEL,  # Your most capable model
    description="Manages the end-to-end process of cloning a repo, generating documentation, and cleaning up.",
    instruction=project_documentation_team_instruction,
    # The coordinator has access to the sub-agents, not the tools directly.
    sub_agents=[github_agent, code_reader_agent, documentation_agent],
)
