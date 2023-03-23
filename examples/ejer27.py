#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from smtplib import SMTP
import smtplib
def main():
    from_address = "lopumacp@hotmail.com"
    to_address = "Jose.Alvaro.Cedeno.Panchana@kyndryl.com"
    message = "Hello, world!"
    mime_message = MIMEText(message, "plain")
    mime_message["From"] = from_address
    mime_message["To"] = to_address
    mime_message["Subject"] = "Correo de prueba"
    smtp = smtplib.SMTP("smtp.office365.com", 587)
    smtp.connect("smtp.office365.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login("lopumacp@hotmail.com", "loDOMApu5891Jc")
    smtp.sendmail(from_address, to_address, mime_message.as_string())
    smtp.quit()
if __name__ == "__main__":
    main()