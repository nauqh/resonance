import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(recipients, image_path):
    sender = "hodominhquan02@gmail.com"
    password = "onnmxxtzcwimhxlv"
    msg = MIMEMultipart()
    msg['Subject'] = "Musicotherapy - Your music receipt"
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    text_part = MIMEText("""
Hi there,

You recently used our Music Taste Analysis app, and we're excited to share your personalized results with you. Your music taste is as unique as you are, and we've carefully analyzed your preferences to provide you with insights and recommendations tailored just for you.

Keep an eye on your inbox for your personal analysis – it's heading your way soon. And hey, feel free to drop us a line if you're itching to discuss the intricacies of your music taste. We're all ears.

Catch you on the flip side,
Resonance Team
""")
    msg.attach(text_part)

    with open(image_path, 'rb') as img:
        image_part = MIMEImage(img.read())
        image_part.add_header('Content-Disposition',
                              'attachment', filename="receipt.png")
        msg.attach(image_part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)


if __name__ == "__main__":
    recipients = ["quan.do@coderschool.vn"]
    image_path = "D:/Laboratory/Projects/resonance/assets/img/Components.png"

    send_email(recipients, image_path)
