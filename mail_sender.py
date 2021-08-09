# -*- coding: utf-8 -*-
"""
@author: giancarlo.pagliaroli
"""

from email.mime.multipart import MIMEMultipart
import smtplib

SEND_FROM = '<please insert your sender mail account>'
password = '<please insert your sender mail password>'


def send_mail(send_to, subject, body):
  multipart = MIMEMultipart()
  multipart['From'] = SEND_FROM
  multipart['To'] = send_to
  multipart['Subject'] = subject
  multipart['X-Priority'] = '2'
  s = smtplib.SMTP('smtp.gmail.com:587')
  s.ehlo()
  s.starttls()
  s.login(SEND_FROM,password)

  s.sendmail(SEND_FROM, send_to, multipart.as_string())
  s.quit()