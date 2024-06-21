import random, smtplib
from email.message import EmailMessage

def get_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0,9))
    return otp


def send_otp(otp, mail):
    from_mail = "rhr007bdu@gmail.com"
    password = "rdhg ctvm wbhk zjjr"
    to_mail = mail

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_mail, password)


    message = EmailMessage()
    message["Subject"] = "OTP Verification"
    message["From"] = from_mail
    message["To"] = to_mail
    message.set_content("Your OTP is: " + otp + "\nThank You From Team GolTable")

    server.send_message(message)
    return "Ok"