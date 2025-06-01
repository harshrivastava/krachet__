import os
import json
import requests
from dotenv import dotenv_values
from rich import print
import sys

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

class SpeechRecognition:
    def __init__(self):
        """Initialize the speech recognition system."""
        try:
            # Create necessary directories
            os.makedirs("Data", exist_ok=True)
            os.makedirs("Frontend/Files", exist_ok=True)
            
            # Initialize status file
            self.status_file = "Frontend/Files/Status.data"
            with open(self.status_file, "w", encoding='utf-8') as f:
                f.write("Ready")
                
        except Exception as e:
            error_msg = f"Error initializing speech recognition: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            sys.exit(1)

    def set_status(self, status):
        """Update the assistant's status."""
        try:
            with open(self.status_file, "w", encoding='utf-8') as f:
                f.write(status)
        except Exception as e:
            print(f"[red]Error updating status: {str(e)}[/red]")

    def listen(self):
        """Listen for speech input using the browser's Web Speech API."""
        try:
            self.set_status("Listening...")
            
            # For now, return a placeholder message
            # In a real implementation, this would use the browser's Web Speech API
            # through the frontend JavaScript code
            return "Speech recognition is currently disabled. Please type your message instead."
            
        except Exception as e:
            error_msg = f"Error in speech recognition: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            self.set_status("Error")
            return None

if __name__ == "__main__":
    recognizer = SpeechRecognition()
    while True:
        try:
            text = recognizer.listen()
            if text:
                print(f"Recognized: {text}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[red]Error: {str(e)}[/red]")