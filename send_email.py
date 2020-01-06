import smtplib
import ssl
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(message_text):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    password = input("Type your password and press enter: ")
    sender_email = "matthewjrice44emailbot@gmail.com"
    receiver_email = "matthewjrice44@gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = message_text
    html = ("<html>"
                "<body>"
                    "<p>"
                        f"{message_text}"
                    "</p>"
                    "</body>"
            "</html>")
    # password = input("Type your password and press enter:")
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def handle_events(event_list: List[str]):
    event_list[0] = f"Date: {event_list[0]}"
    event_list[1] = f"Time: {event_list[1]}"
    event_list[2] = f"Age Group: {event_list[2]}"
    event_list[3] = f"Event Name: {event_list[3]}"
    event_list[4] = f"URL: {event_list[4]}"
    event_list[5] = f"Location: {event_list[5]}"
    formatted_event = '\n'.join(event_list)
    formatted_event = formatted_event + '\n'
    return formatted_event

if __name__ == '__main__':
    formatted_event = handle_events([])
    send_email(formatted_event)
