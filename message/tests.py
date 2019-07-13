from django.test import TestCase
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# Create your tests here.

# smtpObj = smtplib.SMTP("smtp-mail.outlook.com",587)
def connect():
    while True:
        smtpObj = smtplib.SMTP("smtp.163.com",25)
        smtpObj.ehlo()    # 向服务器打招呼
        t = smtpObj.starttls()    #TLS加密
        if 220 in t:
            print("server connected")
            return smtpObj
        else:
            print("please try again")
            i = input("Y/N>")
            if i == "Y" and i == "y":
                continue
            else:
                print("exit")
                return None

def login(smtpObj):
    while True:
        count = 0
        if count > 3:
            print("count > 3")
            return None
        user = input("user:")
        pw = input("passwd:")
        # a = smtpObj.login('z1159105388@163.com','zhoukun1996')
        a = smtpObj.login(user, pw)
        if 235 in a:
            print("login successful")
            return smtpObj,user
        else:
            print("error")
            count += 1


    # return smtpObj,user

def meg(smtpObj,user):
    name = input("发件人姓名：")
    det = input("收件人：")
    subject = input("主题：")
    m = input("内容：")
    msg = MIMEText(m, 'plain', 'utf-8')  # 中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = name +'<' + user+'>'
    msg['To'] = det
    smtpObj.sendmail(user,det,msg.as_string())
#     'Sbuject:'+



if __name__ == '__main__':
    smtpObj = connect()
    Obj, user = login(smtpObj)
    meg(Obj, user)
    smtpObj.quit()