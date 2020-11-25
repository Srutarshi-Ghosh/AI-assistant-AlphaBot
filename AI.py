import speech_recognition as sr
import pyttsx3

if __name__ == "__main__":
    from Date_Time_Events import *
    from Email_Sender import *
    from Search_Websites import *
    from App_open import *
    from AI_chatbot import *

    ACTIVATION_TEXT = ["hello alpha", "hello alpha bot"]
    NOTE_STRINGS = ["make a note", "write this down", "remember this"]
    IGNORE_STRINGS = ["can you please", "please", "can you"]


engine = pyttsx3.init()
engine.setProperty('voice', 1)
engine.setProperty('rate', 188)
engine.setProperty('volume', 3.0)


def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        print("...")
        # print("Say Something")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception:
            pass

    return said.lower()


def ignore_req(text):
    for ignore_val in IGNORE_STRINGS:
        if text.startswith(ignore_val):
            text = text.replace(ignore_val, "")
            break
    return text


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def AI():
    text = get_audio()
    if text != "":

        text = ignore_req(text)

        sp = manage_chats(text)
        if sp:
            speak(sp)
            return 1

        for cmd in ACTIVATION_TEXT:
            if cmd.lower() in text:
                speak("Hi, I am Alpha Bot. What can I do for you?")
                return 1

        if 'search' in text or 'video' in text or (text.split()[0] in QUESTIONS and "date" not in text and "time" not in text):
            manage_search(text)
            return 1

        if 'mail' in text.split():
            speak(parse_mail(text))
            return 1

        datetime_event = event_manage(text)
        if datetime_event:
            if type(datetime_event) == str:
                speak(datetime_event)
            else:
                for event in datetime_event:
                    print(event)
                    speak(event)
            return 1

        if text.split().count('open'):
            file = ' '.join(text.split()[1:])
            print(file)
            res = open_app(file)
            speak(res)
            return 1

        if text.split()[0] == 'play':
            if text.split()[1] == 'song':
                text.replace('song ', '')
            # text = ' '.join(text.split()[1:])
            speak(parse_song_req(text))
            return 1

        for phrase in NOTE_STRINGS:
            if phrase in text:
                speak("What would you like me to write down?")
                note_text = get_audio().lower()
                note(note_text)
                speak("I have made a note.")
                return 1

        if text == 'stop':
            global STOP
            STOP = True
            speak("Alpha bot is shutting down")
            return 1

        speak(faulty_statement())
        return 0


if __name__ == '__main__':

    STOP = False
    speak("Alpha Bot is ready!")
    while not STOP:
        AI()
