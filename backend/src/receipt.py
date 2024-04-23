import base64
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(recipients, base64_image):
    base64_image = base64_image.split(",")[1]

    sender = "hodominhquan02@gmail.com"
    password = "onnmxxtzcwimhxlv"
    msg = MIMEMultipart()
    msg['Subject'] = "Your music receipt"
    msg['From'] = formataddr(('Musicotherapy', sender))
    msg['To'] = ', '.join(recipients)

    text_part = MIMEText("""Hi there! 👋

🎵Thank you for participating in a music therapy session with us. We are delighted to inform you that your personalized results are ready for review. Your musical preferences are as unique as you are, and our team has meticulously analyzed them to provide you with tailored insights and recommendations.

📫Please anticipate receiving your personalized analysis in your inbox shortly. Should you have any questions or wish to further discuss the nuances of your musical taste, please do not hesitate to reach out to us. We are here to assist you.

✉️Looking forward to connecting with you soon! 

📻The Resonance Team
""")
    msg.attach(text_part)

    # Decode base64 image
    image_data = base64.b64decode(base64_image)

    # Attach the image to the email
    image_part = MIMEImage(image_data)
    image_part.add_header('Content-Disposition',
                          'attachment', filename="receipt.png")
    msg.attach(image_part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)


# if __name__ == "__main__":
#     recipients = ["quan.do@coderschool.vn"]
#     image_path = "C:/Users/user/Downloads/receipt.png"

#     send_email(recipients, image_path)
