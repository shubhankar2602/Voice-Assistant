import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyfirmata
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import pywhatkit



username="raspberry02pi2003@gmail.com"
password="shubhankar@2003"

comport='COM3'

board=pyfirmata.Arduino(comport)

led1=board.get_pin('d:8:o')



def led_switch(val):
    if val==1:
        led1.write(1)
    elif val==0:
        led1.write(0)





engine = pyttsx3.init('sapi5')
voices=engine.getProperty("voices")
print(voices[0].id)
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
    speak('I am Friday sir. please tell me how may I help you')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

# def sendMail():
    
def Whats_App():
    speak("what you want to  send")
    message=query
    sk='+91 9764318545'
    if person=="a":
        pywhatkit.sendwhatmsg_instantly(sk,message)
        


def readMail():
           
            N = 1


            imap = imaplib.IMAP4_SSL("imap.gmail.com")

            imap.login(username, password)

            status, messages = imap.select("INBOX")

            messages = int(messages[0])

            for i in range(messages, messages-N, -1):
            
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        print("Subject:", subject)
                        print("From:", From)
                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    body1=body[0:10]
                                    print(body1)
                                    speak(body1)
                                
                        
                    
            imap.close()
            imap.logout()




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
        elif 'light off' in query:
            print('light off......')
            speak('light off........')
            led_switch(1)
        elif 'light on' in query:
            print('light on......')
            speak('light on........')
            led_switch(0)
        elif 'inbox' in query:
            speak("Your Mail's are'")
            readMail()
        elif 'whatsapp' in query:
            speak("Whom you want to send message")
            person=query
            Whats_App()
        elif 'exit' in query:
            break
        # elif 'send mail to harry' in query:
        #     try:
        #         speak("what should I say")
        #         content=take_command()
        #         to='shubhankar2003karajkhede007@gmail.com'
        #         sendEmail(to,content)
        #         speak('email sent.')
        #     except Exception as e:
        #         print(e)
        #         speak('sorry sir but i cant send email.')
                

