import smtplib
import imghdr
from email.message import EmailMessage
from AI import speak, get_audio

EMAIL_ADDRESS = 'srutarshighosh06@gmail.com'
SECURE_PASS = 'onebnxlwehtpblwm'


SEND_TO = {('Deeptaneel', 'Deepto'): 'deeptaneel.dey111@gmail.com',
           ('Mainak', 'Damian', 'Damu'): 'damiankumar2000@gmail.com',
           ('me', 'Srutarshi', 'MI'): 'srutarshighosh06@gmail.com',
           ('surya sundar', 'surjya', 'surya', 'sundar'): 'suryasundarbose99@gmail.com'}

CONTENT_LIST = {'Dinner': "How about Dinner tonight at 9:30",
                'Exam': "All The Best for Today's Exam"}

EMAIL_STRING = ['send a mail', 'send an email', 'send email']


def parse_content(text):
    for suggestion in CONTENT_LIST:
        if suggestion.lower() in text.lower():
            return suggestion, CONTENT_LIST[suggestion]

    return "Cannot send mail", 0


def parse_sender(text):
    receivers = []
    for people in SEND_TO:
        for names in people:
            if names.lower() in text.lower():
                receivers.append(SEND_TO[people])
                break

    return receivers


def send_mail(receiver, content, subject="", attachment=None):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(receiver)
    msg.set_content(content)

    if attachment:
        for file in attachment:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

            msg.add_attachment(file_data, maintype='image', subtype=file_type, file_name=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, SECURE_PASS)
            smtp.send_message(msg)
        #print("Mail Sent Successfully!")
        return 1

    except:
        print("Could Not Send Email!")
        return -1


def Email_Sender(text):
    sub , content = parse_content(text)
    if content.isdigit():
        return "Error in parsing content"

    receiver_list = parse_sender(text)
    if len(receiver_list) == 0:
        return "Please specify Recipients!!"

    confirmation = send_mail(receiver_list, content, subject=sub)
    if confirmation == 1:
        return "Mail sent Successfully"

    else:
        return "Error in sending mail"



def parse_mail(text):
    for said in EMAIL_STRING:
        if said in text:
            speak("who are the recipients?")
            receiver = get_audio()
            receiver_list = parse_sender(receiver)

            if len(receiver_list) == 0:
                return "Please specify Recipients!!"

            speak("What Should I say?")
            content = get_audio()
            confirmation = send_mail(receiver_list, content)
            if confirmation == 1:
                return "Mail sent Successfully"

            else:
                return "Error in sending mail"


