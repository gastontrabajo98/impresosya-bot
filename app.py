
from flask import Flask, request
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
ADMIN_NUMBER = os.getenv("ADMIN_NUMBER")

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    if sender == ADMIN_NUMBER and incoming_msg.lower() == "ok":
        if 'last_reply' in globals():
            client.messages.create(
                body=last_reply['text'],
                from_=TWILIO_WHATSAPP_FROM,
                to=last_reply['to']
            )
            return "Mensaje aprobado y enviado"
        else:
            return "No hay mensajes pendientes."

    if "whatsapp:" in sender:
        prompt = f"Cliente dice: {incoming_msg}\nRedactá una respuesta profesional y amable de ventas para ImpresosYa."
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sos un asesor de ventas profesional de ImpresosYa."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message["content"].strip()
        global last_reply
        last_reply = {"to": sender, "text": reply}

        client.messages.create(
            body=f"Sugerencia de respuesta:\n\n{reply}\n\nResponde 'OK' para aprobar y enviar.",
            from_=TWILIO_WHATSAPP_FROM,
            to=ADMIN_NUMBER
        )
        return "Respuesta enviada al admin."
    return "Nada procesado."

if __name__ == '__main__':
    app.run(debug=True)
