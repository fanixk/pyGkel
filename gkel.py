#!/usr/bin/env python

import sys,signal
import urllib
import time
from getpass import getpass
import re

def get_data():
    resp = urllib.urlopen('https://gkel.teipir.gr/gkelv2/prog_process/progress-e.2011.html')
    resp = resp.read()
    last_modified = re.search(r'(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)',resp)
    last_modified = last_modified.group()
    return last_modified

def check_for_new():
    last = new = get_data()
    while(True):
        new = get_data()
        print new
        if new != last:
            break
        time.sleep(int(sys.argv[1]))
    print 'Nea kataxorisi! ' + new

def help():
    print 'Usage: %s <time in seconds>' % (sys.argv[0])
    print '\nGmail SMTP Server: smtp.gmail.com'
    print 'Hotmail SMTP Server: smtp.live.com'

def send_sms():
    from otenet import Otenet

    username = raw_input('Username: ')
    password = getpass()

    otenet = Otenet(username,password)
    otenet.login()
    otenet.check_limit()
    
    while(True):
        number = raw_input('Kinhto: ')                
        if number.startswith('69') and len(number) ==  10:    #sanity check
            break
        print 'Mi egkyros arithmos tilefonou.'
        
    check_for_new()
    otenet.login()  #relog in case of logout
    otenet.send_sms(number,'Nea kataxorisi bathmologias sto Gkel')

def send_mail():
    import smtplib
    from email.mime.text import MIMEText

    try:
        server = raw_input('SMTP Server: ') 
        server = smtplib.SMTP(server)           

        username = raw_input('Username: ')
        password = getpass()
        server.starttls()
        server.login(username,password)
    except:
        print 'Login Error'
        sys.exit(1)
    print 'Logged in...'
    mail = raw_input('Email address: ')
    check_for_new()
    mail_text = MIMEText('Nea Kataxorisi bathmologias sto Gkel')
    mail_text['Subject'] = 'Gkel'
    try:
        server.sendmail('gkel@gkel.gr', mail, mail_text.as_string())
    except smtplib.SMTPServerDisconnected:
        server.login(username,password)
        server.sendmail('gkel@gkel.gr', mail, mail_text.as_string())
    server.quit()  

if __name__ == '__main__':
    def handler(*args):
		print '\n\nBye Bye!'
		sys.exit(0)

    signal.signal(signal.SIGINT,handler)

    if len(sys.argv) == 2 and sys.argv[1].isdigit():    
        notification = raw_input('Patiste 1 gia sms / 2 gia email: ')
        if notification == '1':
            send_sms()
        elif notification == '2':
            send_mail()
        else:
            print 'Egkyres epiloges: 1 gia sms / 2 gia email.'
    elif len(sys.argv) == 2 and (sys.argv[1] in ["-h","--help"]):
        help()    
    else:
        help()
        

