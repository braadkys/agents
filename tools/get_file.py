import os
from pathlib import Path


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


from fpdf import FPDF


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
    ignore_common_dirs = {".git", "tests", ".idea", ".vscode", ".env", "build"}
    ignore_fe_dirs = {"node_modules", "out", ".storybook"}
    ignore_python_dirs = {".venv", ".ruff_cache", "__pycache__", "pytest", "mypy"}

    ignore_dirs = ignore_fe_dirs | ignore_common_dirs | ignore_python_dirs

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
