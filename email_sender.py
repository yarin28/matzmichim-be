import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from email.message import EmailMessage

class EmailSender:
    def __init__(self, sender_email=None, sender_password=None, smtp_server='smtp.google.com'):
        load_dotenv()
        if sender_email is None or sender_password is None:
            self.sender_email = os.getenv('YARIN_API_EMAIL')
            self.sender_password = os.getenv('YARIN_API_APP_PASSWORD')
            
        #The mail addresses and password
        
    async def send_email(self, receiver_email:str,otp:str):
        server = smtplib.SMTP(self.smtp_server, 587)
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        msg = EmailMessage()
        message = f'this is your otp code = {otp}\n'
        msg.set_content(message)
        msg['Subject'] = "matzmichim otp code"
        msg['From'] = 'matzmichim authentication'
        msg['To'] = receiver_email
        server.send_message(msg)

# for debuging
# def main():
#     send_email_gmail("yarin.greenfeld@gmail.com","123456")
# if __name__ == "__main__":
#     main()