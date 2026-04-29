import os

def get_text(file_path: str) -> str:
    """Reads and returns the content of a text file."""
    with open(file_path, "r") as f:
        return f.read()
