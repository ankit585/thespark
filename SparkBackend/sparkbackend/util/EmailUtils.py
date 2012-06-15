import pprint
from sparkbackend.util.Callable import Callable
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailsUtils():

    def sendRegistrationMail(email,firstName,userKey,code):
        """ send registration mail
        """
        me = "admin@thespark.org"

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Welcome to The Spark"
        msg['From'] = me
        msg['To'] = email
        #FIXME Need to make the host configurable
        url = "http://96.126.100.154/api/v1/user/confirmation?id=" + userKey + "&code=" + code
        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi "+firstName +"\nWelcome to The Spark.Please confirm your registration by clicking the following link. \n" + url
        html = "<html><head></head><body><p>Hi "+firstName+"<br>Welcome to The Spark.Please confirm your registration by clicking the following link.<br>"+url+"</p></body></html>"

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()
        sendRegistrationMail = Callable(sendRegistrationMail)

