import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
fromaddr = "pihealthmonitor@gmail.com"
toaddr = "hruday.95@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "SUBJECT"
data=987
data=str(data)
body = "TEXT YOU WANT TO SEND"+data
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "pimonitorhealth")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()