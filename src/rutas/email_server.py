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

    msg_body = body["msg_body"]
    recipient = body["recipient"]
    subject = body["subject"]
    print(msg_body, recipient, subject)
    print(EMAIL, PASSWORD)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = msg_body
    msg["From"]= EMAIL
    msg["To"] = recipient



    with smtplib.SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.sendmail(EMAIL, recipient, msg.as_string())
    return jsonify('"ok: correo Enviado"'), 200