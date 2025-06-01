from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import pyautogui
import time
import schedule
import threading
from datetime import datetime


env_vars= dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSB YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta","IZ6rdc","O5uR6d LTKOO","vlzY6d","web-answers-webanswers_table__webanswers-table","dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask"
]

messages=[]

SystemChatBot = [{"role": "system","content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotePad(File):
        default_text_editor ='notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot +messages,
            max_token=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None

        )

        Answer = ""


        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+= chunk.choices[0].delta.content

        Answer= Answer.replace("</s","")
        messages.append({"role": "assistant", "content":Answer})
        return Answer
    
    Topic: str = Topic.replace("Content ","")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w",encoding="utf-8")as file:
        file.write(ContentByAI)
        file.close()

    OpenNotePad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True
def YoutubeSearch(Topic):
    Url4Search =f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True
def PlayYoutube(query):
    playonyt(query)
    return True
def OpenApp(app, sess=requests.session()):
    try:
        # First try using AppOpener
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error opening app with AppOpener: {e}")
        try:
            # If AppOpener fails, try searching Google and opening the first result
            def extract_links(html):
                if html is None:
                    return []
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a', {'jsname': 'UWckNb'})
                return [link.get('href') for link in links]
            
            def search_google(query):
                url = f"https://www.google.com/search?q={query}"
                headers = {"User-Agent": useragent}
                response = sess.get(url, headers=headers)
                return response.text if response.status_code == 200 else None

            html = search_google(app)
            if html:
                links = extract_links(html)
                if links:
                    webopen(links[0])
                    return True
            return False
        except Exception as e:
            print(f"Error in fallback method: {e}")
            return False

def CloseApp(app):
    if "chrome" in app.lower():
        # Special handling for Chrome
        os.system("taskkill /f /im chrome.exe")
        return True
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume unmute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")

    if command =="mute":
        mute()
    elif command =="unmute":
        unmute()
    elif command =="volume up":
        volume_up()
    elif command =="volume down":
        volume_down()

    return True


async def TranslateAndExecute(commands:list[str]):

    funcs=[]

    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file"==command:
                pass
            else: fun=asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)

        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun= asyncio.to_thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun= asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun= asyncio.to_thread(Content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun= asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun= asyncio.to_thread(YoutubeSearch,command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun= asyncio.to_thread(System,command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found. For{command}")

    results=await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands:list[str]):

    async for result in TranslateAndExecute(commands):
        pass
    return True

class Automation:
    def __init__(self):
        self.reminders = {}
        self.reminder_thread = None
        self.start_reminder_thread()

    def start_reminder_thread(self):
        """Start a background thread to check for reminders."""
        def check_reminders():
            while True:
                schedule.run_pending()
                time.sleep(1)

        self.reminder_thread = threading.Thread(target=check_reminders, daemon=True)
        self.reminder_thread.start()

    def open_application(self, app_name):
        """Open an application or website."""
        try:
            # Common applications mapping
            app_mapping = {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'facebook': 'https://www.facebook.com',
                'youtube': 'https://www.youtube.com',
                'google': 'https://www.google.com',
                'gmail': 'https://mail.google.com',
                'github': 'https://github.com',
                'linkedin': 'https://www.linkedin.com',
                'twitter': 'https://twitter.com',
                'instagram': 'https://www.instagram.com'
            }

            # Check if it's a website
            if app_name in app_mapping and app_mapping[app_name].startswith('http'):
                webbrowser.open(app_mapping[app_name])
                return

            # Check if it's a known application
            if app_name in app_mapping:
                subprocess.Popen(app_mapping[app_name])
                return

            # Try to open as a website
            if not app_name.startswith(('http://', 'https://')):
                app_name = f'https://www.{app_name}'
            webbrowser.open(app_name)

        except Exception as e:
            error_msg = f"Error opening application: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def close_application(self, app_name):
        """Close an application."""
        try:
            # Common applications mapping
            app_mapping = {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe'
            }

            if app_name in app_mapping:
                os.system(f'taskkill /f /im {app_mapping[app_name]}')
            else:
                os.system(f'taskkill /f /im {app_name}.exe')

        except Exception as e:
            error_msg = f"Error closing application: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def play_music(self, song_name):
        """Play music on YouTube."""
        try:
            search_url = f'https://www.youtube.com/results?search_query={song_name.replace(" ", "+")}'
            webbrowser.open(search_url)
        except Exception as e:
            error_msg = f"Error playing music: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def generate_image(self, prompt):
        """Generate an image using DALL-E."""
        try:
            # TODO: Implement DALL-E integration
            return "Image generation is not implemented yet."
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def set_reminder(self, reminder_text):
        """Set a reminder with the given text."""
        try:
            # Parse reminder text to extract time
            # Format: "reminder HH:MM DD/MM/YYYY message"
            parts = reminder_text.split()
            if len(parts) < 3:
                raise ValueError("Invalid reminder format")

            time_str = parts[0]
            date_str = parts[1]
            message = " ".join(parts[2:])

            # Parse date and time
            reminder_time = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")

            # Schedule the reminder
            def reminder_job():
                print(f"[yellow]REMINDER: {message}[/yellow]")
                # TODO: Add notification

            schedule.every().day.at(reminder_time.strftime("%H:%M")).do(reminder_job)

            return f"Reminder set for {reminder_time.strftime('%H:%M on %d/%m/%Y')}: {message}"

        except Exception as e:
            error_msg = f"Error setting reminder: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def execute_system_command(self, command):
        """Execute a system command."""
        try:
            if command.lower() in ['mute', 'unmute']:
                pyautogui.press('volumemute')
            elif command.lower() == 'volume up':
                pyautogui.press('volumeup')
            elif command.lower() == 'volume down':
                pyautogui.press('volumedown')
            else:
                os.system(command)
        except Exception as e:
            error_msg = f"Error executing system command: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def google_search(self, query):
        """Perform a Google search."""
        try:
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            webbrowser.open(search_url)
        except Exception as e:
            error_msg = f"Error performing Google search: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise

    def youtube_search(self, query):
        """Perform a YouTube search."""
        try:
            search_url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
            webbrowser.open(search_url)
        except Exception as e:
            error_msg = f"Error performing YouTube search: {str(e)}"
            print(f"[red]{error_msg}[/red]")
            raise
