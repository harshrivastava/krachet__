import cohere
from dotenv import dotenv_values
import sys
from rich import print
from .Model import FirstLayerDMM
from .RealtimeSearchEngine import RealtimeSearchEngine
from .Automation import Automation
from .TextToSpeech import TextToSpeech

class ChatBot:
    def __init__(self):
        # Load environment variables
        env_vars = dotenv_values(".env")
        self.cohere_api_key = env_vars.get("CohereAPIKey")
        if not self.cohere_api_key:
            print("[red]Error: CohereAPIKey not found in .env file[/red]")
            sys.exit(1)

        try:
            self.co = cohere.Client(api_key=self.cohere_api_key)
        except Exception as e:
            print(f"[red]Error initializing Cohere client: {str(e)}[/red]")
            sys.exit(1)

        # Initialize components
        self.decision_model = FirstLayerDMM()
        self.search_engine = RealtimeSearchEngine()
        self.automation = Automation()
        self.tts = TextToSpeech()

        # Chat history
        self.chat_history = []

    def process_message(self, message):
        """Process a user message and return the appropriate response."""
        try:
            # Get decision from FirstLayerDMM
            decisions = self.decision_model(message)
            print(f"[blue]Decisions: {decisions}[/blue]")

            responses = []
            for decision in decisions:
                if decision.startswith("general"):
                    # Handle general queries using Cohere
                    response = self.co.chat(
                        model='command-r-plus',
                        message=message,
                        temperature=0.7,
                        chat_history=self.chat_history
                    )
                    responses.append(response.text)
                    self.chat_history.append({"role": "user", "message": message})
                    self.chat_history.append({"role": "assistant", "message": response.text})

                elif decision.startswith("realtime"):
                    # Handle realtime queries using search engine
                    query = decision.split("realtime ")[1]
                    response = self.search_engine.search(query)
                    responses.append(response)

                elif decision.startswith("open"):
                    # Handle opening applications/websites
                    target = decision.split("open ")[1]
                    self.automation.open_application(target)
                    responses.append(f"Opening {target}")

                elif decision.startswith("close"):
                    # Handle closing applications
                    target = decision.split("close ")[1]
                    self.automation.close_application(target)
                    responses.append(f"Closing {target}")

                elif decision.startswith("play"):
                    # Handle playing music
                    song = decision.split("play ")[1]
                    self.automation.play_music(song)
                    responses.append(f"Playing {song}")

                elif decision.startswith("generate"):
                    # Handle image generation
                    prompt = decision.split("generate ")[1]
                    response = self.automation.generate_image(prompt)
                    responses.append(f"Generated image for: {prompt}")

                elif decision.startswith("reminder"):
                    # Handle setting reminders
                    reminder = decision.split("reminder ")[1]
                    self.automation.set_reminder(reminder)
                    responses.append(f"Set reminder: {reminder}")

                elif decision.startswith("system"):
                    # Handle system commands
                    command = decision.split("system ")[1]
                    self.automation.execute_system_command(command)
                    responses.append(f"Executed system command: {command}")

                elif decision.startswith("content"):
                    # Handle content generation
                    topic = decision.split("content ")[1]
                    response = self.co.generate(
                        model='command-r-plus',
                        prompt=f"Write content about: {topic}",
                        temperature=0.7
                    )
                    responses.append(response.text)

                elif decision.startswith("google search"):
                    # Handle Google searches
                    query = decision.split("google search ")[1]
                    self.automation.google_search(query)
                    responses.append(f"Searching Google for: {query}")

                elif decision.startswith("youtube search"):
                    # Handle YouTube searches
                    query = decision.split("youtube search ")[1]
                    self.automation.youtube_search(query)
                    responses.append(f"Searching YouTube for: {query}")

                elif decision == "exit":
                    responses.append("Goodbye!")
                    return "Goodbye!"

            # Combine all responses
            final_response = " ".join(responses)
            
            # Convert response to speech
            self.tts.speak(final_response)
            
            return final_response

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            return error_msg

if __name__=="__main__":
    chatbot = ChatBot()
    while True:
        user_input= input("Enter Your Question: ")
        print(chatbot.process_message(user_input))