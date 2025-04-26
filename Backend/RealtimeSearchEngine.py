from googlesearch import search
from groq import Groq
import json
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Ensure Data directory exists
if not os.path.exists("Data"):
    os.makedirs("Data")

# Initialize JSON files if they don't exist or are empty
for file in ["ChatLog.json", "ChangeLog.json"]:
    file_path = os.path.join("Data", file)
    try:
        # Try to read the file
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:  # If file is empty
                raise json.JSONDecodeError("Empty file", "", 0)
            # Try to parse the JSON
            json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or contains invalid JSON, create it with empty array
        with open(file_path, "w") as f:
            dump([], f, indent=4)

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The Search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title:{i.title}\nDescription: {i.description}\n\n"
    
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "system", "content": "Hi"},
    {"role": "system", "content": "Hello, how can I help you?"}
]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    try:
        with open(r"Data\ChangeLog.json", "r") as f:
            content = f.read().strip()
            if not content:
                messages = []
            else:
                messages = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []
        with open(r"Data\ChangeLog.json", "w") as f:
            dump(messages, f, indent=4)
    
    messages.append({"role": "user", "content": f"{prompt}"})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Query: ")            
        print(RealtimeSearchEngine(prompt))
