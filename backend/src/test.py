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

    text_part = MIMEText("""Hi there,

Thank you for participating in a music therapy session with us. We are delighted to inform you that your personalized results are ready for review. Your musical preferences are as unique as you are, and our team has meticulously analyzed them to provide you with tailored insights and recommendations.

Please anticipate receiving your personalized analysis in your inbox shortly. Should you have any questions or wish to further discuss the nuances of your musical taste, please do not hesitate to reach out to us. We are here to assist you.

Looking forward to connecting with you soon,

The Resonance Team
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
    recipients = ["quan.do@coderschool.vn", "tnklinh6969@gmail.com"]
    image_path = "C:/Users/user/Downloads/receipt.png"

    send_email(recipients, image_path)
