# repo2text

A Python tool to convert entire repositories into an LLM-friendly text format and copy it to the clipboard.

## Features

- **Gitignore Handling:** Respects `.gitignore` rules to include only relevant files, excluding `.gitignore` itself.
- **Project Tree:** Generates a hierarchical project tree.
- **Binary File Detection:** Detects and omits binary files from the output.
- **Empty File Indication:** Clearly indicates if a file is empty.
- **Truncated File Content:** Displays only the first 20 lines of each file in the console for brevity, while copying the entire content to the clipboard.
- **Colored Console Output:** Enhances readability using `colorama`.
- **Clipboard Integration:** Automatically copies the formatted repository content to the clipboard.
- **Operation Time Display:** Shows how long the operation took to complete.
- **Optional Output File:** Allows saving the output to a specified file.

## Installation

Ensure you have Python 3.6 or higher installed.

1. **Clone the Repository:**

   ```bash
   git clone <repo>
   cd repo2text
   ```
