#!/usr/bin/env python

import sys,signal
import urllib
import time
from getpass import getpass

def get_data():
    resp=urllib.urlopen('https://gkel.teipir.gr/gkelv2/prog_process/progress-e.2011.html')
    resp=resp.read()
    sub='\xf4\xe5\xeb\xe5\xf5\xf4\xe1\xdf\xe1 \xea\xe1\xf4\xe1\xf7\xfe\xf1\xe7\xf3\xe7 : '
    start_index=resp.index(sub)+len(sub)
    resp=resp[start_index:start_index+19]
    return resp

def check_for_new():
    #c=0
    last=new=get_data()
    while(new==last):
        new=get_data()
        print new
        #c+=1
        #if c==5:
        #    new='test'
        time.sleep(int(sys.argv[1]))
    print 'Nea kataxorisi! ' + new

def help():
    print 'Usage: %s <time in seconds>' % (sys.argv[0])
    print '\nGmail SMTP Server: smtp.gmail.com'
    print 'Hotmail SMTP Server: smtp.live.com'

def send_sms():
    from otenet import Otenet

    username=raw_input('Username: ')
    password=getpass()

    otenet=Otenet(username,password)
    otenet.login()
    otenet.check_limit()

    number=raw_input('Kinhto: ')                
    if not number.startswith('69') or len(number) != 10:    #sanity check
        print 'Mi egkyros arithmos tilefonou.'
        sys.exit(0)

    check_for_new()
    otenet.send_sms(number,'Nea kataxorisi bathmologias sto Gkel')

def send_mail():
    import smtplib
    from email.mime.text import MIMEText

    try:
        server=raw_input('SMTP Server: ') 
        server=smtplib.SMTP(server)           

        username=raw_input('Username: ')
        password=getpass()
        server.starttls()
        server.login(username,password)
    except:
        print 'Login Error'
        sys.exit(1)
    print 'Logged in...'
    mail=raw_input('Email address: ')
    check_for_new()
    mail_text=MIMEText('Nea Kataxorisi bathmologias sto Gkel')
    mail_text['Subject']='Gkel'
    server.sendmail('gkel@gkel.gr', mail, mail_text.as_string())
    server.quit()  

if __name__ == '__main__':
    def handler(*args):
		print '\n\nBye Bye!'
		sys.exit(0)

    signal.signal(signal.SIGINT,handler)

    if len(sys.argv)==2 and sys.argv[1].isdigit():    
        notification=raw_input('Patiste 1 gia sms / 2 gia email: ')
        if notification=='1':
            send_sms()
        elif notification=='2':
            send_mail()
        else:
            print 'Egkyres epiloges: 1 gia sms / 2 gia email.'
    elif len(sys.argv)==2 and (sys.argv[1] in ["-h","--help"]):
        help()    
    else:
        help()
        

