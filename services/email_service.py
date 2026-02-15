import os
import resend

# Configuración de la API Key
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
        print("⚠️ ERROR: RESEND_API_KEY no está configurada en las variables de entorno")
        return

    try:
        # Enviamos al cliente Y al admin
        # Nota: Si el dominio no está verificado, Resend fallará si 'email_cliente' 
        # no es tu propio correo (lau.montironi@gmail.com)
        resend.Emails.send({
            "from": "onboarding@resend.dev",  
            "to": [email_cliente, ADMIN_EMAIL],
            "subject": f"Confirmación de Reserva - {datos_reserva['fecha']}",
            "html": html
        })
        print(f"✅ Intento de envío de email completado para: {email_cliente}")

    except Exception as e:
        # Capturamos el error para que Railway no se vaya a 'Crashed'
        print(f"❌ Error de Resend: {str(e)}")
        print("ℹ️ Nota: Recuerda que Resend solo permite enviar a tu propio mail si no tienes dominio verificado.")
