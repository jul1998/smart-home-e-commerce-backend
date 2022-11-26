import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

@app.route("/email", methods=["POST", "GET"])
def send_email():
    body = request.get_json()
    smtp_port = 465  # SSL

    msg_body = body["msg_body"]
    recipient = body["recipient"]
    subject = body["subject"]
    print(msg_body, recipient, subject)
    print(EMAIL, PASSWORD)

    # em = EmailMessage()
    # em["From"] = EMAIL
    # em["To"] = recipient
    # em["Subject"] = subject
    # em.set_content(msg_body)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]= EMAIL
    msg["To"] = recipient

    html = '''
       <html>
       <body>
       <h1>Estimado Usuario:''' + recipient + '''   </h1>
       </body>
       </html>
       '''
    asunto_text = "hola"
    # creando elemento MIMEText
    text_mime = MIMEText(asunto_text, 'plain')
    html_mime = MIMEText(html, 'html')

    # adjunta los MIMEText al MIMEMultipart
    msg.attach(text_mime)
    msg.attach(html_mime)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", smtp_port, context=context) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.sendmail(EMAIL, recipient, msg=msg.as_string())
    
    return jsonify('"ok: correo Enviado"'), 200