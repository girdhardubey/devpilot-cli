import os
import json

def list_directory(path: str = ".") -> str:
    """Lists files and folders in the workspace."""
    try:
        ignored = {".git", "venv", "__pycache__", ".env"}
        items = [item for item in os.listdir(path) if item not in ignored]
        return json.dumps({"directory": path, "contents": items})
    except Exception as e:
        return json.dumps({"error": str(e)})

def read_file(file_path: str) -> str:
    """Reads the content of an existing source file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Creates or overwrites a file with new code."""
    try:
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"

# OpenAI Tool Schemas
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories in the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path, defaults to '.'"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of an existing source file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Relative path to the file"}
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or update code inside a file on disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Relative path where the file should be saved"},
                    "content": {"type": "string", "description": "Complete code content to write"},
                },
                "required": ["file_path", "content"],
            },
        },
    },
]

TOOL_MAP = {
    "list_directory": list_directory,
    "read_file": read_file,
    "write_file": write_file,
}