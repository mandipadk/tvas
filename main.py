#Python scipt which uses Telethon - Telegram API to find messsages containing
#keywords mentioned in the regex indicate visa slots opening.
#Upon finding these keywords in new messages, it will play an alert sound.

#original Rushabh Patel, modified by Mandip Adhikari

#Importing modules
from telethon import TelegramClient, events, utils
from pygame import mixer
import threading
import time
import datetime
import re
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

date = 'Unknown'
th = None
sound = None

mixer.init()

print('---------------------------------------------------------')
print('STARTED AT', datetime.datetime.now(), 'Om Namah Shivaya Date Paiyos /\\')
print('---------------------------------------------------------')
print()
print('Select sound length:')
print(' 1. Short')
print(' 2. Long')
sip = input("Choose an option: ")
print()

if(sip=='1'):
    sound = "./shortalert.wav" #short sound file path. NOTE: USE ONLY FORWARD SLASHES IN PATH
elif(sip=='2'):
    sound = './longalert.wav' #long sound file path
else:
    sound = './shortalert.wav' #default sound file path

def alert():
    if('Visa Prep & Experience' in date or 'F1 visa interview Experience' in date):
        #Not playing sound, showing alert for visa experience groups messages
        return
    print('FOUND GO AT', datetime.datetime.now(), ' | ', date)
    print("Playing sound alert")
    mixer.music.load(sound)
    mixer.music.play()
    stop_alert()

def stop_alert():
    time.sleep(8) #Playing sound for 8 secs. You can change according to your need
    mixer.music.stop()

#Setting up the SMS alert client

SMSclient = Client(os.getenv('account_sid', default=None), os.getenv('auth_token', default=None))

#Starting client
client = TelegramClient('session_name', os.getenv('api_id', default=None), os.getenv('api_hash', default=None))
client.start()

#Setting up async handlers to find pattern in messages
regex = r"(.|)(april|may|june|july)(\s|\,|\,\s)([1-9]).+(2023)"
regexSecond = r"(.|)(2023)(\s|\,|\,\s)(april|may|june|july)[\s\S]([1-9])."
@client.on(events.NewMessage())
async def handler(event):
    global date
    chat_from = event.chat if event.chat else (await event.get_chat())
    chat_title = utils.get_display_name(chat_from)
    newText = event.raw_text
    date = chat_title + ' : ' + event.raw_text
    print("New messsage: "+ newText)
    matches = re.finditer(regex, newText, re.MULTILINE | re.IGNORECASE)
    matchesSecond = re.finditer(regexSecond, newText, re.MULTILINE | re.IGNORECASE)
    print("----------------------------------")
    for matchNum, match in enumerate(matches, start=1):
        if match:
            th = threading.Thread(target=alert())
            th.start()
            message = SMSclient.messages.create(
                body="VISA DATE ALERT "+ date,
                from_=os.getenv('twiliofrom', default=None), 
                to=os.getenv('twilioto', default=None)
)
            print("SMS Sent:",message)
        print("----------------------------------")
    for matchSecond in enumerate(matchesSecond):
        if matchSecond:
            th = threading.Thread(target=alert())
            th.start()
        print("----------------------------------")


client.run_until_disconnected() #Program will run until stopped by user






