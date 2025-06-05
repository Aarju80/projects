import datetime
import pyautogui
from modules.core import *  # Functions like speak, take_command, data_sound, etc.
from modules.web_utils import *  # Web-related functions like search_wikipedia, open_website
from modules.system_controls import perform_system_task, control_volume, movements, adjust_brightness
from self_learning.training_data import load_knowledge, save_knowledge, learn_new_qa
from modules.system import *

def main():
    """Main function to handle user interactions."""
    data_sound()
    # Wait for the wake word to activate
    listen_for_wake_word()  
    wish_Me()

    # Load the knowledge base
    knowledge = load_knowledge()  

    def handle_query(query):
        """Processes the user's query and performs the corresponding action."""
        query = query.lower().strip()  # Normalize the query

        # Check the knowledge base for predefined answers
        if query in knowledge:
            speak(f"The answer is: {knowledge[query]}")
            return

        # Command-specific actions
        if 'tell me about' in query or 'search' in query or 'find' in query:
            search_wikipedia(query)
        elif 'open youtube' in query:
            open_website("https://www.youtube.com", "YouTube")
        elif 'open google' in query:
            open_website("https://www.google.com", "Google")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")
        elif 'the date' in query:
            strDate = datetime.datetime.now().strftime("%d:%m")
            speak(f"Sir, the date is {strDate}")
        elif 'press enter' in query:
            pyautogui.press('enter')    
        elif 'volume' in query:
            control_volume(query)
        elif 'training mode' in query:
            training_mode()
        elif 'increase brightness' in query:
            adjust_brightness(1)
        elif 'decrease brightness' in query:
            adjust_brightness(-1)
        elif 'move' in query:
            movements(query)
        elif 'close all the tabs' in query:
            data_sound()
            speak("Closing all tabs.")
            pyautogui.hotkey("ctrl", "shift", "w")
        elif 'minimise the window' in query:
            data_sound()
            speak("Minimizing window.")
            pyautogui.hotkey("winleft", "down")
        elif 'show all tabs' in query:
            data_sound()
            speak("Showing all tabs.")
            pyautogui.hotkey("winleft", "tab")
        elif 'change current tab' in query:
            data_sound()
            speak("Switching tab.")
            pyautogui.hotkey("alt", "tab")
        elif 'reopen closed tab' in query:
            pyautogui.hotkey("ctrl", "shift", "t")
            speak("Reopened the last closed tab.")
        elif 'go to desktop' in query:
            pyautogui.hotkey("winleft", "d")
            speak("Showing desktop.")
        elif 'open file explorer' in query:
            pyautogui.hotkey("winleft", "e")
            speak("File Explorer opened.")
        elif 'open task manager' in query:
            pyautogui.hotkey("ctrl", "shift", "esc")
            speak("Task Manager opened.")
        elif 'play music' in query or 'pause music' in query:
            pyautogui.press("playpause")
            speak("Toggled play/pause.")
        elif 'next song' in query:
            pyautogui.press("nexttrack")
            speak("Playing the next song.")
        elif 'previous song' in query:
            pyautogui.press("prevtrack")
            speak("Playing the previous song.")
        elif 'increase volume' in query:
            pyautogui.press("volumeup", presses=5)
            speak("Volume increased.")
        elif 'decrease volume' in query:
            pyautogui.press("volumedown", presses=5)
            speak("Volume decreased.")
        elif 'mute volume' in query:
            pyautogui.press("volumemute")
            speak("Volume muted.")
        elif 'tell me a joke' in query:
            random_joke()
        elif 'go to search bar' in query:
            query = query.replace("go to search bar", "").replace("and search", "").strip()
            pyautogui.press("tab", presses=4)
            speak("What do you want to search?")
            pyautogui.typewrite(query, interval=0.1)
            pyautogui.press("enter")
        elif 'what can you do for me' in query:
            speak("I can perform various tasks like searching the web, opening websites, controlling your system, and more.")
        elif 'play lag ja gale' in query:
            play_songs(r"https://youtu.be/TFr6G5zveS8?si=-D7XWn9yRN-Wsny8")
        elif 'go to sleep' in query:
            data_sound()
            speak("Going to sleep. Goodbye, sir.")
            sleep_sound()
            exit()
        else:
            speak("I'm sorry, I don't understand that command.")

    # Main loop to listen for commands
    while True:
        query = take_command()
        if query:
            try:
                handle_query(query)
            except Exception as e:
                speak("I encountered an error while processing your request.")
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
