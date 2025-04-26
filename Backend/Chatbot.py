from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars =dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client=Groq(api_key=GroqAPIKey)

messages= []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot =[
    {"role": "system","content":System}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except FileNotFoundError:

    with open(r"Data\ChatLog.json","w")as f:
        dump([],f)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day= current_date_time.strftime("%A")
    date= current_date_time.strftime("%d")
    month=current_date_time.strftime("%B")
    year=current_date_time.strftime("%Y")
    hour=current_date_time.strftime("%H")
    minute=current_date_time.strftime("%M")
    second=current_date_time.strftime("%S")


    data=f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate:{date}\nMonth:{month}\nYear:{year}\n"
    data += f"Time:{hour} hours:{minute}:{second}seconds.\n"
    return data

def AnswerModifier(Answer):
    """Modifies and cleans up the chatbot's response.
    
    Args:
        Answer (str): The raw response from the chatbot
        
    Returns:
        str: Cleaned and formatted response
    """
    # Remove any trailing whitespace
    Answer = Answer.strip()
    
    # Remove any special tokens or markers
    Answer = Answer.replace("</s>", "")
    Answer = Answer.replace("<|im_end|>", "")
    Answer = Answer.replace("<|im_start|>", "")
    
    # Ensure proper sentence endings
    if not Answer.endswith(('.', '!', '?')):
        Answer += '.'
    
    # Remove any duplicate newlines
    Answer = '\n'.join(line for line in Answer.split('\n') if line.strip())
    
    # Capitalize the first letter of the response
    if Answer:
        Answer = Answer[0].upper() + Answer[1:]
    
    return Answer

def ChatBot(Query):
    """This Funcion send the user's query to the chatbot and returns the AI's response. """

    try:
        with open(r"Data\ChatLog.json","r")as f:
            messages= load(f)

            messages.append({"role":"user","content": f"{Query}"})

            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=SystemChatBot + [{"role":"system","content": RealtimeInformation()}] + messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )

        Answer = "" 
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>","")

        messages.append({"role": "assistant","content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:

        print(f"Error:{e}")
        with open(r"Data\ChangeLog.json","w") as f:
            dump([],f,indent=4)
            return ChatBot(Query)
        
if __name__=="__main__":
    while True:
        user_input= input("Enter Your Question: ")
        print(ChatBot(user_input))