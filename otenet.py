import re
import sys
from mechanize import Browser

class Otenet:
    def __init__(self, username, password):
        self.msg = Browser()
        self.msg.set_handle_robots(False)
        self.username=username
        self.password=password
        self.daily=-1
        self.monthly=-1
    
    def login(self):
        self.msg.open('http://tools.otenet.gr/tools/index.do')
        self.msg.select_form(name='loginform')
        self.msg['username'] = self.username
        self.msg['password'] = self.password
        self.msg.submit()
    
    def check_limit(self):
        content=self.parser()
        self.daily=self.get_daily_remaining(content)
        #print 'Logged in...'
        self.monthly=self.get_monthly_remaining(content)
        if self.daily in [-1,5] or self.monthly in [-1,100]:
            print 'Orio SMS'
            self._exit_app()
                
    def _exit_app(self):
        sys.exit(0)
               
    def send_sms(self,number,message):
        self.check_limit()  #sanity check
        if not number.startswith('69') or len(number) != 10:
            print 'Mi egkyros arithmos tilefonou.'
            self._exit_app()
        if len(message)>=160:
            print 'Orio mhkous sms.'
            self._exit_app()
        self.msg.open('http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23')
        self.msg.select_form(name='sendform')
        self.msg['phone'] = number
        self.msg['message'] = message
        self.msg.submit()
        print 'SMS was sent!'
	          
    def parser(self):
        resp = self.msg.open('http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23')
        content = str(resp.read())
        return content
           
    def get_daily_remaining(self,content):
        content = re.search(r'<input type="hidden" name="todaySMS" value="(\d+)">', content)
        if content==None:
            print 'Login Error.'
            self._exit_app()
        return int(content.group(1))
            
    def get_monthly_remaining(self,content):
        content = re.search(r'<input type="hidden" name="monthSMS" value="(\d+)">', content)
        if content==None:
            print 'Login Error.'
            self._exit_app()
        return int(content.group(1))

