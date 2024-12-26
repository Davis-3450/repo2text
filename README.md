# Repo2Text

## Overview
Repo2Text is a Python-based command-line utility designed to transform entire code repositories into a human-readable text format, making them suitable for processing by large language models (LLMs). The tool respects `.gitignore` rules, provides a clean hierarchical view of the repository, and offers additional features like binary file exclusion, clipboard integration, and optional output file creation.

---

## Key Features

### 🗂️ Project Tree Generation
- Generates a hierarchical tree representation of the project structure.
- Excludes files and directories ignored by `.gitignore`.

### 🚫 Binary File Detection
- Automatically identifies and omits binary files to prevent irrelevant data from cluttering the output.

### 📋 Clipboard Integration
- Automatically copies the formatted repository content to the clipboard for easy sharing or further processing.

### 🛠️ Advanced Formatting
- Indicates empty files explicitly.
- Limits displayed content to the first 20 lines per file in the console for concise previews.
- Provides a complete copy of all file contents to the clipboard.

### 🌈 Enhanced Console Output
- Uses `colorama` for color-coded console messages, improving readability.

### 📄 Optional Output File
- Saves the formatted output to a specified file if needed.

### ⏱️ Operation Timing
- Displays the total time taken for the operation.

---

## Installation

### Prerequisites
- Python 3.6 or higher must be installed on your system.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd repo2text
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

---

## Usage

### Command-Line Interface
Run the following command to process a repository:
```bash
repo2text [root_dir] [-o OUTPUT]
```

#### Positional Arguments:
- `root_dir`: The root directory of the project to process. Defaults to the current directory (`.`).

#### Optional Arguments:
- `-o`, `--output`: Path to save the formatted output file.

### Example
To process the current directory and save the output to a file:
```bash
repo2text . -o output.txt
```

---

## How It Works

1. **Load `.gitignore` Rules:**
   - Combines custom `.gitignore` patterns with default ignore rules to exclude unnecessary files.

2. **Build Project Tree:**
   - Recursively traverses directories to create a clear hierarchical representation.

3. **Collect Files:**
   - Includes only non-binary, non-ignored files.

4. **Format Content:**
   - Prepares the project tree and file contents in a structured text format.

5. **Clipboard and File Output:**
   - Copies the result to the clipboard and optionally writes it to a file.

---

## Error Handling

- Warns if `.gitignore` is missing or empty.
- Skips files that cannot be read, marking them as inaccessible.
- Omits binary files automatically.
- Provides clear error messages for invalid input or file I/O issues.

---

## Dependencies

- `colorama`: For colorized console output.
- `pathspec`: To handle `.gitignore` patterns.
- `pyperclip`: For clipboard integration.

Install dependencies automatically with the `pip install -e .` command.

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support

For issues or feature requests, please open an issue on the GitHub repository.

