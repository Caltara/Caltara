import streamlit as st
import requests
from twilio.rest import Client

# Load credentials securely from Streamlit Cloud Secrets
TWILIO_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = st.secrets["TWILIO_PHONE_NUMBER"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
ELEVENLABS_VOICE_ID = st.secrets["ELEVENLABS_VOICE_ID"]

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(to, name, amount, due_date):
    """Send SMS using Twilio"""
    msg = (
        f"Hi {name}, this is a reminder from Caltara AI. "
        f"Your balance of ${amount} was due on {due_date}. "
        "Please pay today to avoid service interruption. Thank you!"
    )
    message = client.messages.create(body=msg, from_=TWILIO_PHONE, to=to)
    return message.sid

def make_voice_call_with_ai(to, name, amount, due_date):
    """Generate AI voice with ElevenLabs and place a call via Twilio"""
    text = (
        f"Hello {name}, this is Eric from Caltara Collections. "
        f"Our records show your balance of ${amount} was due on {due_date}. "
        "To avoid service interruption how would you like to pay your balance today? "
    )

    # Prepare ElevenLabs TTS request
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    # Request TTS audio from ElevenLabs
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"ElevenLabs API error: {response.status_code} {response.text}")

    # Save the MP3 audio locally (for testing or upload)
    with open("voice_message.mp3", "wb") as f:
        f.write(response.content)

    # NOTE: Twilio cannot play MP3 files directly without hosting them online.
    # For now, we use Twilio <Say> to speak the text as a fallback.
    call = client.calls.create(
        to=to,
        from_=TWILIO_PHONE,
        twiml=f"<Response><Say>{text}</Say></Response>"
    )

    return call.sid
