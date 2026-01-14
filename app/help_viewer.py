"""
Help system viewer for user-facing documentation.

Provides functions to list and load help content from the help/ directory.
This is a simplified version of the docs viewer, focused on end-user help.
"""

import os
from aide_frame import paths
from aide_frame.log import logger


def get_help_dir():
    """Get the help directory path."""
    return paths.get("HELP_DIR")


def list_help_files():
    """List all markdown files in help/ directory.

    Returns:
        List of relative paths like ["index.md", "api.md", ...]
    """
    help_dir = get_help_dir()
    if not help_dir or not os.path.isdir(help_dir):
        return []

    files = []
    for f in os.listdir(help_dir):
        if f.endswith('.md') and os.path.isfile(os.path.join(help_dir, f)):
            files.append(f)
    return sorted(files)


def load_help_file(filename):
    """Load a specific markdown file from help/.

    Args:
        filename: Filename like "index.md" or "api.md"

    Returns:
        File content as string, or None if not found or invalid path
    """
    help_dir = get_help_dir()
    if not help_dir:
        return None

    # Security: block path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        logger.warning(f"Path traversal attempt blocked: {filename}")
        return None

    filepath = os.path.join(help_dir, filename)

    # Verify the resolved path is still within help_dir
    real_path = os.path.realpath(filepath)
    real_base = os.path.realpath(help_dir)
    if not real_path.startswith(real_base + os.sep) and real_path != real_base:
        logger.warning(f"Path escape attempt blocked: {filename}")
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def extract_title(filepath):
    """Extract the first H1 heading from a markdown file.

    Args:
        filepath: Full path to the markdown file

    Returns:
        Title string (from first H1 or fallback to filename)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
    except (FileNotFoundError, IOError):
        pass

    # Fallback: filename without extension
    basename = os.path.basename(filepath).replace('.md', '')
    return basename.replace('-', ' ').replace('_', ' ').title()


def get_help_structure():
    """Get help file structure with titles.

    Returns:
        dict with "files" list, each with path and title
    """
    help_dir = get_help_dir()
    if not help_dir or not os.path.isdir(help_dir):
        return {"files": []}

    files = []
    for f in list_help_files():
        filepath = os.path.join(help_dir, f)
        title = extract_title(filepath)
        files.append({"path": f, "title": title})

    # index.md first, then alphabetical
    files.sort(key=lambda d: (0 if d["path"] == "index.md" else 1, d["path"]))

    return {"files": files}
