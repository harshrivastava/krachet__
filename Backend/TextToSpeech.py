import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values
import pyttsx3
from rich import print
import sys

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssitantVoice")

# Set default voice if not specified in .env
if not AssistantVoice:
    AssistantVoice = "en-US-GuyNeural"  # Male voice with natural, soothing tone

async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        # Settings for a more soothing, AI-like voice
        communicate = edge_tts.Communicate(text, AssistantVoice, pitch='-3Hz', rate='+5%')
        await communicate.save(r'Data\speech.mp3')
    except Exception as e:
        print(f"Error creating audio file: {e}")
        raise

def TTS(Text, func=lambda r=None: True, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        try:
            asyncio.run(TextToAudioFile(Text))

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)

            return True

        except Exception as e:
            print(f"Error in TTS (attempt {retry_count + 1}/{max_retries}): {e}")
            retry_count += 1

        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in cleanup: {e}")

    return False

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + "." + random.choice(responses), func)
    else:
        TTS(Text, func)

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # Configure voice properties
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
            
            # Get available voices and set a female voice if available
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
        except Exception as e:
            error_msg = f"Error initializing text-to-speech engine: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            sys.exit(1)

    def speak(self, text):
        """Convert text to speech."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            error_msg = f"Error in text-to-speech: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

if __name__ == "__main__":
    try:
        while True:
            text = input("Enter the text: ")
            if text.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            TextToSpeech(text)
    except KeyboardInterrupt:
        print("\nGoodbye!")
