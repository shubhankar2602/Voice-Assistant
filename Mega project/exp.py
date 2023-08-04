import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyfirmata
import pywhatkit
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import smtplib
import requests

comport='COM3'

board=pyfirmata.Arduino(comport)

led1=board.get_pin('d:8:o')
fan=board.get_pin('d:9:o')
port1=board.get_pin('d:10:o')
port2=board.get_pin('d:11:o')

def led_switch(val):
    if val==1:
        led1.write(1)
    elif val==0:
        led1.write(0)

def fan_switch(val):
    if val==1:
        fan.write(1)
    elif val==0:
        fan.write(0)

def port1_switch(val):
    if val==1:
        port1.write(1)
    elif val==0:
        port1.write(0)

def port2_switch(val):
    if val==1:
        port2.write(1)
    elif val==0:
        port2.write(0)





engine = pyttsx3.init('sapi5')
voices=engine.getProperty("voices")
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
newVoiceRate = 145
engine.setProperty('rate',newVoiceRate)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good morning')
    elif hour>12 and hour<18:
        speak('Good afternoon')
    else:
        speak('Good evening')
    speak('I am Clare sir. please tell me how may I help you')

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=5,phrase_time_limit=3)
        # r.adjust_for_ambient_noise(source, duration = 1)


    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def youtube ():
    print(f'user want to watch {topic} ')
    pywhatkit.playonyt(f'{topic}')

def readMail():
                
    #credentials
    username ="raspberry02pi2003@gmail.com"

    #generated app password
    app_password= "shubhankar@2003"

    # https://www.systoolsgroup.com/imap/
    gmail_host= 'imap.gmail.com'

    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)

    #login
    mail.login(username, app_password)

    #select inbox
    mail.select("INBOX")

    #select specific mails
    _, selected_mails = mail.search(None, '(FROM "raspberry02pi2003@gmail.com")')

    #total number of mails from specific user
    print("Total Messages from user :" , len(selected_mails[0].split()))

    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)
        print("\n===========================================")

        #access data
        print("Subject: ",email_message["subject"])
        print("To:", email_message["to"])
        print("From: ",email_message["from"])
        print("Date: ",email_message["date"])
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                print("Message: \n", message.decode())
                a=(message.decode())
                speak(a)

                print("==========================================\n")
                break

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('raspberry02pi2003@gmail.com', 'shubhankar@2003')
    server.sendmail('raspberry02pi2003@gmail.com', to, content)

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    # print(res)
    return res['slip']['advice']

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    # print(res)
    return res["joke"]



if __name__ =='__main__':
    # speak('Good afternoon')
    wishMe()
    while True:
        query=take_command().lower()

        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak('According to wikipedia')
            speak(results)
        elif 'light on' in query:
            print('light on......')
            speak('light on........')
            led_switch(1)
        elif 'light off' in query:
            print('light off......')
            speak('light off........')
            led_switch(0)
        elif 'turn on fan' in query:
            print('turning on fan.....')
            speak('turning on fan')
            fan_switch(1)
        elif 'turn off fan' in query:
            print('turning off fan.....')
            speak('turning off fan')
            fan_switch(0)
        elif 'light up' in query:
            print('turning on desk light')
            speak('turning on desk light')
            port1_switch(1)
        elif 'darkness' in query:
            print('turning off desk light')
            speak('turning off desk light')
            port1_switch(0)
        elif 'turn on device' in query:
            print('Your device is alive')
            speak('Your device is alive')
            port2_switch(1)
        elif 'turn off device' in query:
            print('Your device is off')
            speak('Your device is off')
            port2_switch(0)
        elif 'on youtube' in query:
            speak("what you want to watch")
            topic=take_command()
            youtube()
        elif 'open Youtube' in query:
            speak('opening youtube')
            webbrowser.open('https://www.youtube.com/')
        elif 'open google' in query:
            speak('opening google')
            webbrowser.open('https://www.google.com/')
        elif 'open login' in query:
            speak('opening login page')
            webbrowser.open('https://gppune.ac.in/gpp/gpp_s20/userindex.php')
        elif 'play music' in query:
            speak('hope this will entertain you')
            dir='C:\\Users\\Public\\Music\\Sample Music'
            songs=os.listdir(dir)
            print(songs)
            os.startfile(os.path.join(dir,songs[-1]))
        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H hours %M minutes and %S seconds")
            speak(f'sir the time is{strTime}')
        elif 'stop music' in query:
            os.system("TASKKILL /F /IM wmplayer.exe")
        elif 'read my mail' in query:
            speak('reading your latest emails sir')
            readMail()
        elif 'send email to' in query:
            try:
                speak('what should I say..')
                content=take_command()
                to='raspberry02pi2003@gmail.com'
                sendEmail(to,content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('sorry sir I am not able to send the mail')
        elif 'advice' in query:
            speak("Here's an advice for you sir")
            advice=get_random_advice()
            speak(advice)
            print(advice)
        elif 'joke' in query:
            speak('hope you will like this one')
            joke=get_random_joke()
            speak(joke)
            print(joke)
        elif 'exit' in query:
            speak("well see you soon sir Thank you")
            break
