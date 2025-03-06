# -*- coding: utf-8 -*-

import smtplib
from email.message import EmailMessage
from config import personal

def send_message(to: str, subject: str, message: str):    
    # 创建邮件对象
    msg = EmailMessage()
    msg["From"] = personal.SENDER_EMAIL
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(message)

    # 发送邮件
    try:
        with smtplib.SMTP_SSL(personal.SMTP_SERVER, personal.PORT) as server:
            server.login(personal.SENDER_EMAIL, personal.PASSWORD)
            server.send_message(msg)
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送失败: {e}")