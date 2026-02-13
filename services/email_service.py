from fastapi_mail import FastMail, MessageSchema, MessageType
from core.email_config import conf
import traceback


async def enviar_confirmacion_reserva(email_cliente: str, datos_reserva: dict):
    EMAIL_ADMIN = "lau.montironi@gmail.com"

    html = f"""
    <html>
        <body style="background-color: #1a1a1a; color: #e6dcc9; font-family: sans-serif; padding: 20px;">
            <h1 style="color: #d4af37;">¡Reserva Confirmada! 🍣</h1>
            <p>Hola, gracias por elegir nuestro restaurante.</p>
            <div style="border: 1px solid #d4af37; padding: 15px; border-radius: 10px;">
                <p><strong>Fecha:</strong> {datos_reserva['fecha']}</p>
                <p><strong>Hora:</strong> {datos_reserva['hora']}</p>
                <p><strong>Personas:</strong> {datos_reserva['party_size']}</p>
            </div>
            <p>Si necesitas cancelar, puedes hacerlo desde tu perfil.</p>
            <p>¡Te esperamos!</p>
        </body>
    </html>
    """

    try:
        print("📨 Intentando enviar email a:", email_cliente)

        message = MessageSchema(
            subject="Confirmación de tu Reserva - Restaurante",
            recipients=[email_cliente],
            body=html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        print("✅ Email enviado correctamente a:", email_cliente)

    except Exception as e:
        print("❌ ERROR enviando email:")
        print(str(e))
        traceback.print_exc()
