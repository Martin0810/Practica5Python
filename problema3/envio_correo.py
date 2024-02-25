import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(asunto, cuerpo, destinatario, archivo_adjunto=None):
    # Configurar el servidor SMTP
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'tu_correo@example.com'
    smtp_password = 'tu_contraseña'

    # Configurar mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = smtp_user
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Adjuntar cuerpo del correo
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar archivo si se proporciona
    if archivo_adjunto:
        adjunto = MIMEText(open(archivo_adjunto).read())
        adjunto.add_header('Content-Disposition', 'attachment', filename=archivo_adjunto)
        mensaje.attach(adjunto)

    # Enviar correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, destinatario, mensaje.as_string())

if __name__ == "__main__":
     enviar_correo('Asunto del Correo', 'Cuerpo del Correo', 'destinatario@example.com', 'reporte.xlsx')