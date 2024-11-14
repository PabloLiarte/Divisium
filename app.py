from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuración para el envío de correos
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "pablo.liarteg@gmail.com"  # Reemplaza con tu dirección de correo
PASSWORD = "Mango.Kush8"    # Reemplaza con tu contraseña de correo (si tienes 2FA, usa un "app password")

# Función para enviar el correo
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
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        investment = request.form["investment"]

        # Enviar el correo con los datos del formulario
        if send_email(name, email, phone, investment):
            # Si el correo fue enviado correctamente, mostrar mensaje de éxito
            return render_template("index.html", message="¡Gracias por tu interés! Hemos recibido tu mensaje.", message_type="success")
        else:
            # Si hubo un error al enviar el correo, mostrar mensaje de error
            return render_template("index.html", message="Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.", message_type="error")
    
    return render_template("index.html", message=None)

if __name__ == "__main__":
    app.run(debug=True)
