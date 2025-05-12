# PromptShell-Desktop

A natural language terminal application that converts plain English commands into executable shell commands.

## Overview

PromptShell is a desktop application that allows users to interact with their terminal using natural language. Instead of memorizing complex command line syntax, you can simply describe what you want to do, and PromptShell will generate and execute the appropriate shell command.

Built with Flet (Flutter-powered Python UI framework) and powered by Google's Gemini 1.5 Flash AI model, PromptShell provides a modern, intuitive interface to terminal operations.

## Features

- **Natural Language Processing**: Type commands in plain English
- **Command Translation**: Automatically converts natural language to shell commands
- **Safety Filters**: Prevents execution of potentially dangerous commands
- **Modern Terminal UI**: Clean, responsive interface with syntax highlighting
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.7+
- Google AI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/PromptShell-Desktop.git
   cd PromptShell-Desktop
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/)
   - Update the `api_key` variable in `ui.py` with your key

## Usage

1. Start the application:
   ```
   python main.py
   ```

2. Type natural language commands in the input field:
   - "Show me all PDF files in this folder"
   - "Create a new directory called projects"
   - "Find all files modified in the last week"

3. Press Enter to execute the command
   - PromptShell will show the translated shell command
   - The command output will be displayed in the terminal window

4. Type "exit" or "quit" to close the application

## Examples

| Natural Language | Translated Command |
|------------------|-------------------|
| Show all PNG files | `find . -name "*.png"` |
| Create a text file called notes | `touch notes.txt` |
| Show system information | `uname -a` |
| List processes using most memory | `ps aux --sort=-%mem | head` |

## Project Structure

- `main.py`: Application entry point
- `ui.py`: Terminal UI implementation using Flet
- `smartshell.py`: Core logic for command translation and execution
- `requirements.txt`: Project dependencies

## Security Note

PromptShell includes basic safety filters to prevent execution of potentially dangerous commands. However, always review the translated command before execution, especially in production environments.

## License

[MIT License](LICENSE)

## Acknowledgements

- [Flet](https://flet.dev/) for the UI framework
- [Google Generative AI](https://ai.google.dev/) for the LLM capabilities
- [LangChain](https://python.langchain.com/) for AI integration