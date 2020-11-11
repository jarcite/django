import smtplib

gmail_user = 'arcipond@gmail.com'
gmail_password = 'hellojung'
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
except:
    print ('Something went wrong...')