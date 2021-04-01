import random
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_address, user_name):
    sender_email = "noreply.horizon.group1"
    random_otp = ''.join(str(random.randint(0, 9)) for i in range(6))
    context = ssl.create_default_context()
    password = "wkklmyzrmgjsxpse"
    message = MIMEMultipart("alternative")
    message["Subject"] = "User Registration"
    message["From"] = sender_email
    message["To"] = email_address
    html = "<html><body><p>Hi " + user_name + ",<br> Thanks for registering with us.<br>" \
                                              "Please enter the below mentioned code to verify your email address!" \
                                              "<br>" \
                                              "<br>" \
                                              "Your one time verification code is: " + random_otp + " <br>" \
                                                                                                    "Do not share " \
                                                                                                    "this code with " \
                                                                                                    "anyone!" \
                                                                                                    "<br>From Team, " \
                                                                                                    "<br> " \
                                                                                                    "E-Voting</p" \
                                                                                                    "></body></html> "
    part1 = MIMEText(html, "html")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, email_address, message.as_string()
        )
    return random_otp
