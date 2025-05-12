import flet as ft
from smartshell import SmartShell
import os
import sys
import re

class TerminalUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.api_key = "Your Api Key"
        self.shell = SmartShell(self.api_key)
        
        self.setup_page()
        self.setup_ui()
        
    def setup_page(self):
        self.page.title = "SmartShell Terminal"
        self.page.padding = 0
        self.page.bgcolor = "#0D1117"  # Dark background like a terminal
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_min_width = 400
        self.page.window_min_height = 300
        self.page.fonts = {
            "JetBrainsMono": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/webfonts/JetBrainsMono-Regular.woff2"
        }
        
    def setup_ui(self):
        # Terminal output area (history)
        self.terminal_output = ft.ListView(
            expand=True,
            spacing=2,
            padding=10,
            auto_scroll=True
        )
        
        # Command input field
        self.prompt_text = ft.Text(
            f"{os.getcwd()}$ ",
            color="#4EC9B0",
            size=14,
            font_family="JetBrainsMono",
            no_wrap=False,
            selectable=True
        )
        
        self.command_input = ft.TextField(
            border=ft.InputBorder.NONE,
            color="#FFFFFF",
            bgcolor="#0D1117",
            text_size=14,
            cursor_color="#FFFFFF",
            cursor_width=1,
            cursor_height=18,
            multiline=False,
            expand=True,
            on_submit=self.process_command,
            content_padding=ft.padding.only(left=5, top=8, bottom=8),
            hint_text="Type a command in natural language...",
            hint_style=ft.TextStyle(
                color="#666666",
                font_family="JetBrainsMono",
                size=14
            )
        )
        
        # Input row with prompt and command field
        input_row = ft.Row(
            [self.prompt_text, self.command_input],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Main container
        main_container = ft.Container(
            content=ft.Column(
                [
                    self.terminal_output,
                    ft.Divider(height=1, color="#333333"),
                    input_row
                ],
                spacing=0,
                expand=True
            ),
            expand=True,
            padding=0
        )
        
        self.page.add(main_container)
        
        # Add welcome message
        self.add_system_message("SmartShell v1.0 - Natural Language Terminal, Type commands in plain English and press Enter, Type exit or quit to close the application")
        self.update_prompt()
        
        # Set focus to input field when the app starts
        self.page.on_keyboard_event = self.handle_keyboard
        self.command_input.focus()
        
    def handle_keyboard(self, e: ft.KeyboardEvent):
        """Handle keyboard shortcuts"""
        if e.key == "Escape" and e.ctrl:
            self.page.window_close()
            
    def update_prompt(self):
        """Update the prompt text with the current directory"""
        self.prompt_text.value = f"{self.shell.current_directory}$ "
        self.page.update(self.prompt_text)
        
    def add_command_entry(self, user_text):
        """Add user command to the terminal output"""
        self.terminal_output.controls.append(
            ft.Row(
                [
                    ft.Text(
                        f"{self.shell.current_directory}$ ",
                        color="#4EC9B0",
                        size=14,
                        font_family="JetBrainsMono",
                        selectable=True
                    ),
                    ft.Text(
                        user_text,
                        color="#FFFFFF",
                        size=14,
                        font_family="JetBrainsMono",
                        selectable=True
                    )
                ],
                spacing=0,
                wrap=True
            )
        )
        self.page.update(self.terminal_output)
        
    def add_system_message(self, message):
        """Add a system message to the terminal output"""
        self.terminal_output.controls.append(
            ft.Text(
                message,
                color="#888888",
                italic=True,
                size=14,
                font_family="JetBrainsMono",
                selectable=True
            )
        )
        self.page.update(self.terminal_output)
        
    def add_command_output(self, output):
        """Add command output to the terminal"""
        if output:
            # Preserve line breaks and format output
            text_spans = []
            for line in output.split('\n'):
                if line.strip():  # Skip empty lines
                    text_spans.append(
                        ft.Text(
                            line,
                            color="#CCCCCC",
                            size=14,
                            font_family="JetBrainsMono",
                            selectable=True
                        )
                    )
            
            for span in text_spans:
                self.terminal_output.controls.append(span)
            
            self.page.update(self.terminal_output)
            
    def add_error_output(self, error):
        """Add error output to the terminal"""
        if error:
            self.terminal_output.controls.append(
                ft.Text(
                    error,
                    color="#FF6347",  # Tomato red color for errors
                    size=14,
                    font_family="JetBrainsMono",
                    selectable=True
                )
            )
            self.page.update(self.terminal_output)
            
    def process_command(self, e):
        """Process the entered command"""
        command = self.command_input.value.strip()
        if not command:
            return
            
        # Add the command to history
        self.add_command_entry(command)
        
        # Clear input field
        self.command_input.value = ""
        self.page.update(self.command_input)
        
        # Handle special commands
        if command.lower() in ["exit", "quit"]:
            self.add_system_message("Exiting SmartShell...")
            self.page.window_close()
            return
            
        # Add a small delay to show "thinking" status
        self.add_system_message("Generating command...")
        
        # Execute the command
        try:
            # Get the translated command
            translated_command = self.shell.generate_command(command)
            self.add_system_message(f"Executing: {translated_command}")
            
            # Run the command
            output, error = self.shell.run_command(command)
            
            if output:
                self.add_command_output(output)
            if error:
                self.add_error_output(error)
                
            # Update the prompt if directory changed
            self.update_prompt()
            
        except Exception as e:
            self.add_error_output(f"Error: {str(e)}")
            
        # Set focus back to input field
        self.command_input.focus()
        self.page.update()

def main(page: ft.Page):
    TerminalUI(page)

if __name__ == "__main__":
    ft.app(target=main)