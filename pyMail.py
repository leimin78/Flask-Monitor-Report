import smtplib
import email.mime.multipart
import email.mime.text
import os

class mailSend:

    def __init__(self):
        self.msg = email.mime.multipart.MIMEMultipart()

    def mailMsg(self,mail_from,mail_to,mail_subject,mail_content):
        self.msg['from'] = mail_from
        self.msg['to'] = mail_to
        self.msg['subject'] = mail_subject
        txt = email.mime.text.MIMEText(mail_content)
        self.msg.attach(txt)

    def mailsend(self):
        smtp = smtplib
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com', '25')
        username = 'andy.lei@taiway.net'
        password = '1qaz@WSX'
        print(username,password)
        smtp.login(username,password)

        try:
            smtp.sendmail(self.msg['from'],self.msg['to'],str(self.msg))
            print("邮件已发送..")
        except Exception as e:
            print(e.args)
            print("邮件发送失败..")

        smtp.quit()



