# repo2text/repo2text.py

#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import time
from pathlib import Path
from typing import List

import colorama
import pathspec
import pyperclip


def main() -> None:
    """
    Entry point for the repo2text command-line tool.
    Converts a repository into an LLM-friendly text format,
    copies it to the clipboard, and optionally writes it to a file.
    """
    # Initialize colorama
    colorama.init(autoreset=True)

    # Parse command-line arguments
    parser = setup_argparser()
    args = parser.parse_args()

    root_dir = args.root_dir

    if not os.path.isdir(root_dir):
        print_error(f"The specified root directory '{root_dir}' does not exist or is not a directory.")
        sys.exit(1)

    # Change the current working directory to root_dir
    os.chdir(root_dir)

    start_time = time.time()

    # Load .gitignore and combined ignore patterns
    spec = load_gitignore()

    # Build project tree
    tree = build_project_tree(spec=spec)

    # Collect files to include
    files = collect_files(spec=spec)

    # Build the final string to copy
    final_string = build_final_string(tree, files)

    # Copy to clipboard
    copy_to_clipboard(final_string)

    # Optionally write to an output file
    if args.output:
        write_output_file(final_string, args.output)

    end_time = time.time()
    duration = end_time - start_time
    print_info(f"Operation completed in {duration:.2f} seconds.")


def setup_argparser() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description='Convert an entire repository into an LLM-friendly text format and copy it to the clipboard.'
    )
    parser.add_argument(
        'root_dir',
        nargs='?',
        default='.',
        help='Root directory of the project (default: current directory)'
    )
    parser.add_argument(
        '-o',
        '--output',
        help='Output file to save the formatted repository (optional)'
    )
    return parser


def load_gitignore() -> pathspec.PathSpec:
    """
    Loads the .gitignore file and combines it with default ignore patterns.

    Returns:
        pathspec.PathSpec: Combined ignore patterns.
    """
    default_ignore_patterns = [
        '.git/',
        '.svn/',
        '.hg/',
        '.DS_Store',
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*$py.class',
        '*.so',
        'build/',
        'dist/',
        'downloads/',
        'eggs/',
        '.eggs/',
        'lib/',
        'lib64/',
        'parts/',
        'sdist/',
    ]

    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as gitignore_file:
            gitignore_lines = gitignore_file.readlines()
        if not gitignore_lines:
            print_warning("Alert: .gitignore is empty.")
        gitignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_lines)
    else:
        print_warning("Alert: .gitignore file not found. Using default ignore patterns.")
        gitignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', [])

    # Combine .gitignore with default ignore patterns
    default_spec = pathspec.PathSpec.from_lines('gitwildmatch', default_ignore_patterns)
    combined_spec = gitignore_spec + default_spec
    return combined_spec


def build_project_tree(spec: pathspec.PathSpec) -> str:
    """
    Builds a hierarchical project tree excluding ignored files and directories.

    Args:
        spec (pathspec.PathSpec): Combined ignore patterns.

    Returns:
        str: Project tree as a string.
    """
    tree: List[str] = []
    for root, dirs, files in os.walk('.'):
        # Exclude ignored directories
        dirs[:] = [
            d for d in dirs
            if not spec.match_file(os.path.normpath(os.path.join(os.path.relpath(root, '.'), d)) + '/')
        ]

        # Determine the indentation level
        rel_path = os.path.relpath(root, '.')
        if rel_path == '.':
            level = 0
        else:
            level = rel_path.count(os.sep) + 1

        indent = ' ' * 4 * level
        directory = os.path.basename(root) if rel_path != '.' else '.'
        tree.append(f"{indent}{directory}/")

        # Add files to the tree
        subindent = ' ' * 4 * (level + 1)
        for file in sorted(files):
            rel_file_path = os.path.normpath(os.path.join(os.path.relpath(root, '.'), file))
            if not spec.match_file(rel_file_path) and Path(rel_file_path).name != '.gitignore':
                tree.append(f"{subindent}{file}")

    return '\n'.join(tree)


def collect_files(spec: pathspec.PathSpec) -> List[str]:
    """
    Collects all non-ignored files, excluding .gitignore.

    Args:
        spec (pathspec.PathSpec): Combined ignore patterns.

    Returns:
        List[str]: List of file paths to include.
    """
    files_to_include: List[str] = []
    for root, dirs, files in os.walk('.'):
        # Exclude ignored directories
        dirs[:] = [
            d for d in dirs
            if not spec.match_file(os.path.normpath(os.path.join(os.path.relpath(root, '.'), d)) + '/')
        ]

        for file in sorted(files):
            rel_file_path = os.path.normpath(os.path.join(os.path.relpath(root, '.'), file))
            if not spec.match_file(rel_file_path) and Path(rel_file_path).name != '.gitignore':
                files_to_include.append(rel_file_path)

    return files_to_include


def is_binary_file(file_path: str) -> bool:
    """
    Determines if a file is binary by checking for null bytes.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if binary, False otherwise.
    """
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
    except Exception:
        # If the file cannot be read, consider it binary to omit it
        return True
    return False


def build_final_string(tree: str, files: List[str]) -> str:
    """
    Builds the final formatted string containing the project tree and file contents.

    Args:
        tree (str): Project tree.
        files (List[str]): List of files to include.

    Returns:
        str: Final formatted string.
    """
    output: List[str] = []
    output.append("Project Tree:")
    output.append(tree)
    output.append("")

    for file in files:
        # Console Output with color and header ###
        print_header(file)
        print_code_block_indicator()

        # Build string without color
        header = f"### File: {file}\n### Code block below:\n"
        output.append(header)

        if is_binary_file(file):
            message = "(Binary file omitted)"
            print_warning(message)
            output.append(f"{message}\n")
        else:
            try:
                with open(file, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
                    if not lines:
                        message = "(Empty file)"
                        print_warning(message)
                        output.append(f"{message}\n")
                    else:
                        # Truncate to first 20 lines for display
                        truncated_content = ''.join(lines[:20]).rstrip('\n')
                        output.append(f"{''.join(lines)}\n")
                        print_truncated_content(truncated_content)
            except Exception as e:
                message = f"(Could not read file: {e})"
                print_error(message)
                output.append(f"{message}\n")
        print()  # Add an empty line for better readability

    final_output = '\n'.join(output)
    return final_output


def print_header(file: str) -> None:
    """
    Prints the file header with color.

    Args:
        file (str): File path.
    """
    print(f"{colorama.Fore.GREEN}### File: {file}{colorama.Style.RESET_ALL}")


def print_code_block_indicator() -> None:
    """
    Prints the code block indicator with color.
    """
    print(f"{colorama.Fore.MAGENTA}### Code block below:{colorama.Style.RESET_ALL}")


def print_truncated_content(content: str) -> None:
    """
    Prints the truncated content with color.

    Args:
        content (str): Truncated file content.
    """
    print(f"{colorama.Fore.WHITE}{content}...\n{colorama.Style.RESET_ALL}")


def print_warning(message: str) -> None:
    """
    Prints a warning message with color.

    Args:
        message (str): Warning message.
    """
    print(f"{colorama.Fore.YELLOW}{message}{colorama.Style.RESET_ALL}")


def print_error(message: str) -> None:
    """
    Prints an error message with color.

    Args:
        message (str): Error message.
    """
    print(f"{colorama.Fore.RED}{message}{colorama.Style.RESET_ALL}")


def print_info(message: str) -> None:
    """
    Prints an informational message with color.

    Args:
        message (str): Informational message.
    """
    print(f"{colorama.Fore.CYAN}{message}{colorama.Style.RESET_ALL}")


def copy_to_clipboard(content: str) -> None:
    """
    Copies the given content to the clipboard.

    Args:
        content (str): Content to copy.
    """
    try:
        pyperclip.copy(content)
        print_info("The repository has been successfully copied to the clipboard.")
    except Exception as e:
        print_error(f"Error copying to clipboard: {e}")


def write_output_file(content: str, output_path: str) -> None:
    """
    Writes the content to the specified output file.

    Args:
        content (str): Content to write.
        output_path (str): Path to the output file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)
        print_info(f"The repository has been written to '{output_path}'.")
    except Exception as e:
        print_error(f"Error writing to output file: {e}")
