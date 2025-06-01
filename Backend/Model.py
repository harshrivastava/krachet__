import cohere 
from rich import print
from dotenv import dotenv_values
import sys

class FirstLayerDMM:
    def __init__(self):
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

        self.funcs = [
            "exit", "general", "realtime", "open", "close", "play",
            "generate image", "system", "content", "google search", 
            "youtube search", "reminder"
        ]

        self.preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

    def __call__(self, query):
        """Process a query and return the decision."""
        try:
            # Use Cohere to classify the query
            response = self.co.classify(
                model='large',
                inputs=[query],
                examples=[
                    {"text": "who was akbar?", "label": "general"},
                    {"text": "what's the time?", "label": "general"},
                    {"text": "who is the current prime minister?", "label": "realtime"},
                    {"text": "open chrome", "label": "open"},
                    {"text": "close notepad", "label": "close"},
                    {"text": "play let her go", "label": "play"},
                    {"text": "generate image of a cat", "label": "generate"},
                    {"text": "set a reminder for tomorrow", "label": "reminder"},
                    {"text": "mute the volume", "label": "system"},
                    {"text": "write a letter", "label": "content"},
                    {"text": "search for python tutorials", "label": "google search"},
                    {"text": "find cooking videos", "label": "youtube search"}
                ]
            )

            # Get the prediction
            prediction = response.classifications[0].prediction
            confidence = response.classifications[0].confidence

            # If confidence is low, default to general
            if confidence < 0.5:
                return [f"general {query}"]

            # Return the appropriate decision
            if prediction == "general":
                return [f"general {query}"]
            elif prediction == "realtime":
                return [f"realtime {query}"]
            elif prediction == "open":
                return [f"open {query.split('open ')[1]}"]
            elif prediction == "close":
                return [f"close {query.split('close ')[1]}"]
            elif prediction == "play":
                return [f"play {query.split('play ')[1]}"]
            elif prediction == "generate":
                return [f"generate {query.split('generate ')[1]}"]
            elif prediction == "reminder":
                return [f"reminder {query.split('reminder ')[1]}"]
            elif prediction == "system":
                return [f"system {query.split('system ')[1]}"]
            elif prediction == "content":
                return [f"content {query.split('content ')[1]}"]
            elif prediction == "google search":
                return [f"google search {query.split('search ')[1]}"]
            elif prediction == "youtube search":
                return [f"youtube search {query.split('search ')[1]}"]
            else:
                return [f"general {query}"]

        except Exception as e:
            print(f"[red]Error in FirstLayerDMM: {str(e)}[/red]")
            return [f"general {query}"]

if __name__ == "__main__":
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            print(FirstLayerDMM()(user_input))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"[red]Error: {str(e)}[/red]")