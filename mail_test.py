import smtplib, ssl


sender = "from@example.com"
receiver = "to@example.com"
user = "f69396842d193f"
password = "c831385ef5eec6"
host = "smtp.mailtrap.io"
port = 2525
ssl_port = 465

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}
This is a test e-mail message."""



with smtplib.SMTP(host, port) as server:
    server.login(user, password)
    server.sendmail(sender, receiver, message)
    print('mail successfully sent')



context = ssl.create_default_context()

with smtplib.SMTP_SSL(host, ssl_port, context=context) as server:
    server.login(user, password)
    server.sendmail(sender, receivers, message)
    print('ssl mail successfully sent')