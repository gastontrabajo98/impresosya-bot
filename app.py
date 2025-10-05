from flask import Flask, request
from twilio.rest import Client
import openai, os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo correctamente en Render 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
