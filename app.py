# 1. IMPORTS
from pyscript import document
import re
import random

# 2. YOUR CHATBOT DATA & LOGIC
negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

random_questions = (
    "Why are you here?",
    "Are there humans like you?",
    "What do you consume for sustenance?",
    "Is there life on this planet?",
    "Does Earth have a leader?",
    "What planets have you visited?",
    "What technology do you have on this planet?"
)

alienbabble = (
    {r'\s*your planet': (
        "My planet is a utopia of diverse organisms and species.",
        "I am from Opidipus, the capital of the Wayward Galaxies."
    )},
    {r'.*why\s+.*': (
        "Why do you ask that?",
        "What makes you wonder?"
    )},
    {r'.*what\s+.*': (
        "What do you think?",
        "Why do you ask?"
    )},
    {r'.*i\s+think\s(.*)': (
        "Why do you think {0}?",
        "What makes you believe {0}?"
    )},
    {r'.*': (
        "Please tell me more.",
        "Why do you say that?",
        "Interesting. Can you elaborate?",
        "How do you think I feel about that?"
    )}
)

reflections = {
    "i'm": "you are",
    "you're": "i'm",
    "i": "you",
    "you": "I",
    "me": "you",
    "my": "your",
    "your": "my"
}

def reflect(text):
    words = text.split()
    return ' '.join(reflections.get(word, word) for word in words)

def make_exit(reply):
    return any(command in reply for command in exit_commands)

def get_bot_reply(reply):
    for pair in alienbabble:
        for pattern, responses in pair.items():
            match = re.match(pattern, reply)
            if match:
                response = random.choice(responses)
                return response.format(*map(reflect, match.groups()))

# Track where we are in the conversation (replaces the while loop)
chat_step = "ask_name"
user_name = ""

# 3. THE BUTTON TRIGGER
def send_message(event):
    global chat_step, user_name
    
    input_box = document.querySelector("#user-input")
    output_div = document.querySelector("#output")
    
    user_text = input_box.value.strip()
    if not user_text:
        return  # Do nothing if input is empty
        
    input_box.value = ""  # Clear the input box
    reply_lower = user_text.lower()

    # Step 1: User just answered their name
    if chat_step == "ask_name":
        user_name = user_text
        bot_msg = f"Hi {user_name}, I'm Marvin! Will you help me?"
        chat_step = "ask_help"

    # Step 2: User answered whether they will help
    elif chat_step == "ask_help":
        if reply_lower in negative_responses:
            bot_msg = "Ok, have a great Earth day!"
            chat_step = "ended"
        else:
            bot_msg = random.choice(random_questions)
            chat_step = "chatting"

    # Step 3: Main conversation loop
    elif chat_step == "chatting":
        if make_exit(reply_lower):
            bot_msg = "Ok, have a great Earth day!"
            chat_step = "ended"
        else:
            bot_msg = get_bot_reply(reply_lower)
            
    # Step 4: Conversation is over
    else:
        bot_msg = "Marvin has left the chat. Refresh the page to talk again!"

    # Display Marvin's response on the webpage
    output_div.innerText = f"Marvin: {bot_msg}"
