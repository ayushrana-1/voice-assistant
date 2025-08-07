import webbrowser
import pyautogui
import time
import os
import time
import pywhatkit as kit

def bomber():
    webbrowser.open("https://www.callbomberz.in/unlimited-sms-bomber.html")

def img_enchance():
    webbrowser.open("https://imgupscaler.com/")

def spotify():
    webbrowser.open("https://open.spotify.com/collection/tracks")

def forward_spotify():
    pyautogui.hotkey('alt','right arrow') 

def backwark_spotify():
    pyautogui.hotkey('alt','left arrow')

def next_song():
    pyautogui.hotkey('ctrl','right arrow')

def previous_song():
    pyautogui.hotkey('ctrl' ,'left arrow')

def calendar():
    webbrowser.open("https://calendar.google.com")

def canva():
    webbrowser.open("https://www.canva.com")

def youtube():
    webbrowser.open("https://www.youtube.com")

def gmail():
    webbrowser.open("https://mail.google.com")

def github():
    webbrowser.open("https://github.com")

def stackoverflow():
    webbrowser.open("https://stackoverflow.com")

def linkedin():
    webbrowser.open("https://www.linkedin.com")

def reddit():
    webbrowser.open("https://www.reddit.com")

def google_drive():
    webbrowser.open("https://drive.google.com")

def netflix():
    webbrowser.open("https://www.netflix.com")

def twitter():
    webbrowser.open("https://twitter.com")

def instagram():
    webbrowser.open("https://www.instagram.com")

def huggingface():
    webbrowser.open("https://huggingface.co")

def chatgpt():
    webbrowser.open("https://chat.openai.com")

def blackbox():
    webbrowser.open("https://www.blackbox.ai")

def google_photos():
    webbrowser.open("https://photos.google.com")

def whatsapp():
    webbrowser.open("https://web.whatsapp.com")

def telegram():
    webbrowser.open("https://web.telegram.org")

def chrome():
    os.startfile("chrome")

def settings():
    os.system("start ms-settings:")

def notepad():
    os.system("start notepad")

def file_explorer():
    os.system("start explorer")

def cmd():
    os.system("start cmd")

def powershell():
    os.system("start powershell")

def code_editor():
    pyautogui.press('win') 
    pyautogui.write("cursor")
    pyautogui.press('enter')

def task_manager():
    os.system("start taskmgr")

def control_panel():
    os.system("start control")

def paint():
    os.system("start mspaint")

def refresh():
    pyautogui.hotkey('win','d')
    time.sleep(1)
    pyautogui.press('f5')
    pyautogui.press('f5')
    pyautogui.press('f5') 

def anime_movie_download(): 
    webbrowser.open("https://web.telegram.org/a/#7706418172")

def watch_anime():
    webbrowser.open("https://www.rareanimes.com/")

# def play_mp4(name):
#     kit.playonyt(name)

# def anime_watch(anime_movie):
#     formatted_anime = anime_movie.replace(" ", "-")
#     webbrowser.open(f"https://www.rareanimes.com/{formatted_anime}")
#     webbrowser.open(f"https://anime-world.in/{formatted_anime}")