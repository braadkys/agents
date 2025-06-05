from pathlib import Path
import os


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


import subprocess
from fpdf import FPDF


def clone_github_repo(repo_url: str, local_path: str = "agent_workspace") -> str:
    """
    Clones a public GitHub repository to a local directory.
    Args:
        repo_url (str): The URL of the GitHub repository to clone.
        local_path (str): The local directory path to clone the repository into.
                          Defaults to 'agent_workspace'.
    Returns:
        str: The local path where the repository has been cloned.
             Returns an error message if cloning fails.
    """
    if os.path.exists(local_path):
        return f"Error: Directory '{local_path}' already exists. Please delete it or choose a different path."
    try:
        subprocess.run(
            ["git", "clone", repo_url, local_path],
            check=True,
            capture_output=True,
            text=True,
        )
        return local_path
    except subprocess.CalledProcessError as e:
        return f"Error cloning repository: {e.stderr}"


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
    ignore_dirs = {".git", "__pycache__", "node_modules", ".vscode", ".venv"}

    for root, dirs, files in os.walk(directory):
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for name in files:
            # Get the relative path from the root of the directory
            relative_path = os.path.relpath(os.path.join(root, name), directory)
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


def save_documentation_as_pdf(documentation_content: str, filename: str = "CodeDocumentation.pdf") -> str:
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

    output_path = os.path.join(desktop_path, filename)
    pdf.output(output_path)
    return f"Documentation successfully saved to {output_path}"


import shutil
import time


def delete_local_repo(directory: str, max_retries=5, delay_seconds=1) -> str:
    """
    Deletes a local directory, retrying on failure to handle transient file locks from other processes.
    """
    for attempt in range(max_retries):
        try:
            shutil.rmtree(directory)
            print(f"Successfully deleted directory: {directory}")
            return f"Successfully deleted directory: {directory}"
        except PermissionError as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: Permission denied. Retrying in {delay_seconds}s...")
                time.sleep(delay_seconds)  # Wait for the lock to be released
            else:
                # This was the last attempt, so return the error from here
                print(f"Final attempt failed. Could not delete directory: {e}")
                return f"Error: Failed to delete after {max_retries} attempts. Last error: {e}"
        except FileNotFoundError:
            return f"Error: Directory not found at '{directory}'"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    # --- THIS IS THE FIX ---
    # This line is only reached if the loop finishes in an unexpected way (e.g., max_retries=0).
    # It ensures the function always returns a string as promised.
    return f"Error: Could not delete '{directory}' after {max_retries} attempts."


def delete_repository_tool(directory: str) -> str:
    """
    A simple tool for the AI to delete a cloned repository directory.
    This tool handles retries and file permissions internally.
    """
    print(f"Tool called: Attempting to delete '{directory}' with internal retry logic.")
    # Call your existing, robust function with the desired retry values hardcoded.
    return delete_local_repo(directory=directory, max_retries=5, delay_seconds=2)
