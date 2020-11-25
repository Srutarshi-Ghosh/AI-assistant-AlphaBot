import random

chat_data = {
                ("hello", "hi", "hey", "hey there"): ["Hello, I am Alpha Bot, your personal assistant"],
                ("what can you do", "what are the things you can do", "can you help me with someting"): ["I can search websites, manage your calendars, take notes, send emails, open any app, play music and also play youtube videos"],
                ("who are you", "what is your function"): ["I am your personal assistant, Alpha Bot"],
                ("what is your name", "tell me your name"): ["I am Alpha Bot"]
            }

No_data = ["I cannot help you with that!", "I don't know what you mean"]

def manage_chats(text):
    for chat in chat_data:
        for phrase in chat:
            if phrase in text:
                return random.choice(chat_data[chat])

    return None

def faulty_statement():
    return random.choice(No_data)

