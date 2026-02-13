import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

ADMIN_EMAIL = "lau.montironi@gmail.com"

async def enviar_confirmacion_reserva(email_cliente: str, datos_reserva: dict):

    html = f"""
    <html>
      <body style="background-color:#1a1a1a;color:#e6dcc9;font-family:sans-serif;padding:20px;">
        <h1 style="color:#d4af37;">¡Nueva Reserva Confirmada! 🍣</h1>

        <div style="border:1px solid #d4af37;padding:15px;border-radius:10px;">
          <p><strong>Cliente:</strong> {email_cliente}</p>
          <p><strong>Fecha:</strong> {datos_reserva['fecha']}</p>
          <p><strong>Hora:</strong> {datos_reserva['hora']}</p>
          <p><strong>Personas:</strong> {datos_reserva['party_size']}</p>
        </div>

        <p>Gracias por confiar en UpgradeFood.</p>
      </body>
    </html>
    """

    if not resend.api_key:
        raise RuntimeError("RESEND_API_KEY no está configurada")

    # Enviamos al cliente Y al admin
    resend.Emails.send({
        "from": "onboarding@resend.dev",  # Para pruebas
        "to": [email_cliente, ADMIN_EMAIL],
        "subject": "Confirmación de Reserva - UpgradeFood",
        "html": html
    })
