import os
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Configuración para el envío de correos
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

def send_email(name, email, phone, investment):
    subject = "Nuevo formulario de contacto"
    body = f"""
    Nombre: {name}
    Correo: {email}
    Teléfono: {phone}
    Inversión: {investment}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Recoger los datos del formulario
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        investment = request.form.get("investment")

        # Enviar el correo con los datos del formulario
        if send_email(name, email, phone, investment):
            return render_template("index.html", message="¡Gracias por tu interés! Hemos recibido tu mensaje.", message_type="success")
        else:
            return render_template("index.html", message="Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.", message_type="error")
    return render_template("index.html", message=None)

# Necesario para que funcione correctamente en Vercel
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Agrega este bloque para ejecutar localmente
if __name__ == "__main__":
    app.run(debug=True)