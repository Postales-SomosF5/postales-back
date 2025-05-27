import smtplib
from email.mime.text import MIMEText

# Datos de tu cuenta y destinatario
remitente = "paquitasalas880@gmail.com"
destinatario = "silviarodriguezexposito76@gmail.com"
asunto = "Prueba de contraseña de aplicación"
cuerpo = "¡Hola! Este es un mensaje de prueba usando una contraseña de aplicación."

# Crear mensaje
mensaje = MIMEText(cuerpo)
mensaje['Subject'] = asunto
mensaje['From'] = remitente
mensaje['To'] = destinatario

# Iniciar conexión con Gmail
try:
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, "TU_CONTRASEÑA_DE_APLICACIÓN")  # Aquí va la contraseña de aplicación
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()
    print("✅ Correo enviado con éxito.")
except Exception as e:
    print("❌ Error al enviar el correo:", e)
