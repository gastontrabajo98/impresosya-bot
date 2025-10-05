from flask import Flask, request
from twilio.rest import Client
import openai
import os

# Inicializar Flask
app = Flask(__name__)

# Variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
ADMIN_NUMBER = os.getenv("ADMIN_NUMBER")

# Ruta principal
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    # Si el mensaje viene del administrador
    if sender == ADMIN_NUMBER:
        if incoming_msg.lower() == "ping":
            client.messages.create(
                from_=TWILIO_WHATSAPP_FROM,
                to=ADMIN_NUMBER,
                body="✅ Servidor en línea y funcionando."
            )
            return "pong", 200

    # Lógica del bot con OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sos un asistente de ventas profesional para una empresa de packaging llamada ImpresosYa."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = response.choices[0].message["content"].strip()

    # Enviar respuesta al usuario por WhatsApp
    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=sender,
        body=reply
    )

    return "ok", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
