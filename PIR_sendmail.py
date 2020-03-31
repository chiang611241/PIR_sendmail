import time
import sys
import RPi.GPIO as GPIO
import smtplib
import numpy as np
import cv2
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

cap = cv2.VideoCapture(0)
ret = cap.set(3,1080)
ret = cap.set(4,720)

GMAIL_USER = 'yor_username'           
TO         = '<your_gmail>'  
#CC         = '<other_gmail>'
SUBJECT    = 'SUBJECT'
TEXT       = 'Your PIR sensor detected movement'

def send_email():
    print "\n"
    print "Sending Email"
    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(GMAIL_USER,'your_password')
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT + '\n'
    print header
    #msg = header + '\n' + TEXT + ' \n\n'
    
    msg2 = MIMEMultipart('related')
    msg2Text = MIMEText(TEXT,'plain', 'utf-8')
    msg2.attach(msg2Text)
    fp = open('output.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg2.attach(img)

    smtpserver.sendmail(GMAIL_USER, TO, msg2.as_string())
    smtpserver.close()

def take_picture():
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("output.png",gray)
    

GPIO.setmode(GPIO.BCM)

PIN_PIR = 18
STB_TIME = 3

try:
    
    GPIO.setup(PIN_PIR, GPIO.IN)
    print "\n",
    for i in range(0, STB_TIME):
        print "      Waitting for PIR to stable, %d sec\r" %(STB_TIME - i),
        sys.stdout.flush()
        time.sleep(1)
    
    print "\n"
    print "  READY ...",
    print "\n"
    
    while True:
        if(GPIO.input(PIN_PIR)):
            print "THE PIR SENSOR DETECTED MOVEMENT           \r",
            sys.stdout.flush()
            take_picture()
            send_email()
            
            
            time.sleep(30) 
        else:
            print "PIR sensor get ready for movement detection\r",            
    
except KeyboardInterrupt:    
    print "\n\n  Quit!  \n"
