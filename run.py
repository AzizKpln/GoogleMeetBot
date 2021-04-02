import speech_recognition as sr;import random,os;import undetected_chromedriver as uc
from selenium import webdriver;from selenium.webdriver.common.by import By;from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC;from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType;from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys;from getpass import getpass
import smtplib;from email.mime.multipart import MIMEMultipart;from email.mime.text import MIMEText
from os.path import expanduser
class startChrome():
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument(f"--user-data-dir={expanduser('~')}\\AppData\\Local\\Google\\Chrome\\User Data\\")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36.")
        self.driver = uc.Chrome(options=options)
        GMA=GoogleMeetAttendance(self.driver)
        GMA.clear();print("Input The Meet Link:\n");self.meetLink=input("#>")
        self.driver.get(str(self.meetLink))
        GMA.langOption()
        GMA.setName()
        GMA.runScript()
class GoogleMeetAttendance(startChrome):
    def __init__(self,driver):
        self.driver=driver
        self.r=sr.Recognizer()
    def clear(self):
        if os.name=="nt":os.system("cls")
        else:os.system("clear")
    def smtpCONNECT(self):
        self.mailAddress=input("Input Your GMAIL Address[Can be a fake gmail account doesn't matter]\n#>")
        self.Password=getpass("\n\nYour Password[You won't see any characters on the screen but your password will be given]:")
        self.connect=smtplib.SMTP(host='smtp.gmail.com',port=587)
        self.connect.ehlo()
        self.connect.starttls()
        self.connect.login(self.mailAddress,self.Password)
    def smtpSEND(self):
        #gmail added only
        subject="GOOGLE MEET BOT ALERT!"
        msg="ONE OF THE WORD/SENTENCE THAT YOU HAVE ENTERED TO THE SCRIPT HAS BEEN MENTIONED BY THE TEACHER"
        message='Subject:%s\n\n%s'%(subject,msg)
        self.connect.sendmail(self.mailAddress,self.mailAddress,message)
    def langOption(self):
        print("In what language is your name pronounced?")
        print("[1] Turkish");print("[2] English");self.lan=input("#>")
        if self.lan=="1":self.lang="tr";
        elif self.lan=="2":self.lang="en"
        else:print("Error!");import sys;sys.exit()
    def setName(self):
        self.clear();print("What IS Your Name-Surname?\n")
        self.name=str(input("#>"))
        nameL=self.name.split(" ")
        if len(nameL)>1:self.returnR=7
        elif len(nameL)==1:self.returnR=3
        else:sys.exit()
        self.clear();print("What Response Do You Wanna Write?(Separate With ',')\n\nPrint 'help' to get help.");self.response=input("#>")
        if self.response.lower() == "help":
            print("Example Responses:\nhere,i'm here,present,i'm here but the door knocked. Im gonna check it,I'm here but having lunch etc.")
            self.response=input("#>")
        self.responseList=self.response.split(",")
        self.clear();print("SMTP-->Do you wanna add additional Word/Sentence detection[Y/N]?\n\nPrint 'help' to get help.");print("Note:Detection will be sent via your email");self.responseAd0=input("#>")
        if self.responseAd0.lower() == "help":
            self.clear;print("Example Word/Sentence Detection(Separate With ','):\nquiz,pop quiz,exam,surprise exam,attendance,attendance list");print("Note:print y to issue this sentences/words.")
            self.responseAd0=input("#>")
            self.clear();self.smtpCONNECT()
        if self.responseAd0.lower() == "y":
            self.clear();print("Enter The Words/Sentences:")
            self.responseAd0=input("\n#>")
            self.clear();self.smtpCONNECT()
        self.responseListAd0=self.responseAd0.split(",")
    def Listen(self):
        with sr.Microphone() as source:
            audio=self.r.listen(source,phrase_time_limit=int(self.returnR))
            print("Teacher IS Listening..")
        speech=str(self.r.recognize_google(audio,language=str(self.lang)))
        self.responseChoice=random.choice(self.responseList)
        name=self.name
        print(speech)
        if name.lower() in speech.lower():
            jC=joinMeet(self.responseList,self.driver)
            print("Alert:--Teacher Calls--")
            print("Writing automated text..")
            jC.writeComment()
        elif speech.lower() in self.responseListAd0:
            self.smtpSEND()
    def runScript(self):
        while 1:
            try:
                self.Listen()
            except:
                continue
class joinMeet(GoogleMeetAttendance):
    def __init__(self,responseList,driver):
        self.responseList=responseList
        self.driver=driver
    def writeComment(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "chatTextInput"))).send_keys(random.choice(self.responseList)+Keys.ENTER)
sC=startChrome()



