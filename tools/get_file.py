from pathlib import Path
from fpdf import FPDF
import os
import graphviz


def find_and_read_from_desktop(filename: str):
    try:
        # 1. Find the path to the user's desktop
        desktop_path = Path.home() / "Desktop"

        # Verify the de
        # ktop directory actually exists.
        if not desktop_path.is_dir():
            return f"Error: The Desktop directory was not found at '{desktop_path}'"

        # 2. Construct the full path to the target file.
        full_file_path = desktop_path / filename

        # 3. Open and read the file using the full path.
        with open(full_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

    except FileNotFoundError:
        return f"Error: The file '{filename}' was not found on the Desktop."
    except PermissionError:
        return f"Error: Permission denied to read the file '{filename}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def list_repository_files(directory: str) -> str:
    """
    Lists all files in a directory recursively, ignoring common non-code directories.

    Args:
        directory (str): The path to the repository's root directory.

    Returns:
        str: A formatted string listing all the relevant file paths.
    """
    file_list = []
    # Common directories to ignore
    ignore_common_dirs = {".git", "tests", ".idea", ".vscode", ".env", "Dockerfile", "build"}
    ignore_fe_dirs = {"node_modules", "out", ".storybook"}
    ignore_python_dirs = {".venv", ".ruff_cache", "__pycache__", "pytest", "mypy"}
    ignore_go_dirs = {"go.mod", "go.sum", "mock", "_test.go"}

    ignore_dirs = ignore_fe_dirs | ignore_common_dirs | ignore_python_dirs | ignore_go_dirs

    def is_ignored(dir_name: str) -> bool:
        return any(to_ignore in dir_name for to_ignore in ignore_dirs)

    for root, _, files in os.walk(directory):
        if is_ignored(root):
            continue

        for file_name in files:
            if is_ignored(file_name):
                print(f"ignored {file_name}")
                continue
            # Get the relative path from the root of the directory
            relative_path = os.path.relpath(os.path.join(root, file_name), directory)
            file_list.append(relative_path)

    return "Project File Structure:\n" + "\n".join(file_list)


def read_file_content(filepath: str) -> str:
    """
    Reads and returns the content of a single text file.

    Args:
        filepath (str): The full path to the file to be read.

    Returns:
        str: The content of the file, or an error message if it cannot be read.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"Error reading file '{filepath}': {e}"


def save_documentation_as_pdf(documentation_content: str) -> str:
    """
    Saves the provided string content into a PDF file on the desktop.

    Args:
        documentation_content (str): The text content to be saved as documentation.
        filename (str): The name of the output PDF file. Defaults to 'CodeDocumentation.pdf'.

    Returns:
        str: A confirmation message with the path where the file was saved.
    """
    # Use a basic PDF library like FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    # FPDF needs UTF-8 text to be decoded
    # The 'latin-1' encoding is a common way to handle arbitrary text for FPDF
    pdf.multi_cell(0, 5, documentation_content.encode("latin-1", "replace").decode("latin-1"))

    # In a real scenario, you would resolve the desktop path dynamically
    # For this example, we'll save it to the current working directory.
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        desktop_path = os.getcwd()  # Fallback to current directory

    output_path = os.path.join(desktop_path, "CodeDocumentation.pdf")
    pdf.output(output_path)
    return f"Documentation successfully saved to {output_path}"


def create_dependency_graph(dot_string: str) -> str:
    """
    Takes a string in the DOT graph language and renders it into a PNG image file.

    This function saves the output to the user's Desktop.

    Args:
        dot_string (str): A string containing the graph definition in DOT language.

    Returns:
        str: A confirmation message with the path to the saved image file.
    """
    print(f"Tool: Rendering diagram from DOT string {dot_string}...")

    try:
        # Create a graph object from the DOT language source string
        source = graphviz.Source(dot_string)

        # Define the output path on the user's Desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_path_with_name = os.path.join(desktop_path, 'dependency_plot')

        # Render the graph to a file (e.g., 'dependency_plot.png')
        # The 'view=False' argument prevents it from opening automatically.
        # The 'cleanup=True' option removes the intermediate source file.
        rendered_path = source.render(output_path_with_name, format='png', view=False, cleanup=True)

        final_message = f"Diagram creation complete. File saved to: {rendered_path}"
        print(final_message)
        return final_message

    except graphviz.backend.ExecutableNotFound:
        error_message = (
            "ERROR: Graphviz system software not found. "
            "Please install it and ensure it's in your system's PATH. "
            "See installation instructions at https://graphviz.org/download/"
        )
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message


# --- Example of how to use the function ---
if __name__ == '__main__':
    # This is the DOT string from your agent's output in the screenshot
    example_dot_string = """
    digraph G {
      rankdir=LR;
      node [shape=box];
      "app_main.py" [label="app_main.py"];
      "config.py" [label="config.py"];
      "agents/code_reader.py" [label="agents.code_reader"];
      "agents/documentation_agent.py" [label="agents.documentation_agent"];
      "core/services.py" [label="core.services"];
      "core/interaction_handler.py" [label="core.interaction_handler"];
      "tools/get_current_time.py" [label="tools.get_current_time"];
      "tools/get_file.py" [label="tools.get_file"];
      "agents/root_agent.py" [label="agents.root_agent"];
      "app_main.py" -> "dotenv";
      "app_main.py" -> "asyncio";
      "app_main.py" -> "os";
      "app_main.py" -> "uuid";
      "app_main.py" -> "traceback";
      "app_main.py" -> "google.adk";
      "app_main.py" -> "config";
      "app_main.py" -> "agents";
      "app_main.py" -> "core";
      "app_main.py" -> "call_agent_turn";
      "app_main.py" -> "session_service";
      "config.py" -> "os";
      "agents/code_reader.py" -> "google.adk";
      "agents/code_reader.py" -> "config";
      "agents/code_reader.py" -> "tools";
      "agents/documentation_agent.py" -> "google.adk";
      "agents/documentation_agent.py" -> "config";
      "core/services.py" -> "google.adk.sessions";
      "core/interaction_handler.py" -> "google.adk";
      "tools/get_current_time.py" -> "datetime";
      "tools/get_file.py" -> "os";
      "tools/get_file.py" -> "pathlib";
      "tools/get_file.py" -> "fpdf";
      "tools/get_file.py" -> "pyvis.network";
      "tools/get_file.py" -> "re";
      "agents/root_agent.py" -> "google.adk";
      "agents/root_agent.py" -> "config";
      "agents/root_agent.py" -> "tools";
      "agents/root_agent.py" -> "code_reader_agent";
      "agents/root_agent.py" -> "documentation_agent";
      "agents/root_agent.py" -> "create_dependency_graph";
    }
    """

    # Call the function with your DOT string
    create_dependency_graph(example_dot_string)


def save_documentation_as_html(documentation_content: str) -> str:
    """
    Saves the provided string content into an HTML file on the desktop.

    To preserve formatting like line breaks and spacing from the original
    documentation string, the content is wrapped in HTML <pre> tags.

    Args:
        documentation_content (str): The text content to be saved as documentation.
        filename (str): The name of the output HTML file.
                        Defaults to 'CodeDocumentation.html'.

    Returns:
        str: A confirmation message with the path where the file was saved.
    """
    # Create a basic HTML structure to wrap the content
    # The <pre> tag is used to preserve whitespace and line breaks
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF--8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Documentation</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 2em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 1em;
            border-radius: 5px;
            white-space: pre-wrap;       /* Alows text to wrap */
            word-wrap: break-word;       /* Breaks long words if necessary */
        }}
    </style>
</head>
<body>
    <pre>{documentation_content}</pre>
</body>
</html>
"""

    filename = 'test.html'

    # Get the path to the user's desktop
    # os.path.expanduser("~") gets the home directory (e.g., /Users/username or C:\\Users\\username)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # If the Desktop directory doesn't exist, fall back to the current working directory
    if not os.path.exists(desktop_path):
        desktop_path = os.getcwd()

    # Define the full path for the output file
    output_path = os.path.join(desktop_path, filename)

    try:
        # Write the HTML content to the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return f"Documentation successfully saved to {output_path}"
    except IOError as e:
        return f"Error: Could not save file. {e}"
