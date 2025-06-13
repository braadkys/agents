from google.adk import Agent

from config import SUB_AGENT_MODEL
from tools import create_dependency_graph

graph_creation_agent = Agent(
    name="GraphCreationAgent",
    model=SUB_AGENT_MODEL,
    description="Inspect the links between key project parts and generate an architectural graph highlighting the interactions between them",
    instruction="""You are a system analyst. Your only goal is to create a code dependency graph.

    **Your Goal:** To create a visual, dependency graph of a software project.

     **WORKFLOW:**
    1. You will be given a task containing the path to a project directory.
    2. Return a text based topological diagram representation of the code base   
    3. Use create_dependency_graph to plot it 
      """,
    tools=[create_dependency_graph],
)
