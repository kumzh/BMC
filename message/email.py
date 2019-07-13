from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib,re

class EmailHandler(object):
    def __init__(self,user,password,type = 1):
        # self.__QQ = {'smtp':'smtp.qq.com','port':465}
        self.__163 = {'smtp':'smtp.163.com','port':25}
        self.user = user
        self.password = password
        # if type == 0:
        #    self.server=smtplib.SMTP(self.__QQ['smtp'],self.__QQ['port'])
        #    self.server.login (self.user,self.password)
        # elif type == 1:
        self.server = smtplib.SMTP(self.__163['smtp'], self.__163['port'])
        self.server.login (self.user,self.password)

    def send_mail(self,To,subject,content):
        try:
            msg = MIMEText(content,'plain','utf-8')
            msg['From'] = formataddr(['Alarm System',self.user])
            msg['To'] = formataddr(['',To])
            msg['Subject'] = subject
            self.server.sendmail(self.user,To,msg.as_string())
            return "【%s】发送成功"%subject
        except Exception as f:
            print(f)
            return "【%s】发送失败,请检查信息"%subject