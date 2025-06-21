import os
import requests
from twilio.rest import Client

# Load credentials from environment variables
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")  # Set this for custom voice

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(to, name, amount, due_date):
    msg = f"Hi {name}, your balance of ${amount} is past due since {due_date}. Please pay now to avoid interruption."
    message = client.messages.create(body=msg, from_=TWILIO_PHONE, to=to)
    return message.sid

def make_voice_call_with_ai(to, name, amount, due_date):
    text = f"Hello {name}, this is a reminder from Caltara AI. Your payment of {amount} was due on {due_date}. Please visit our website to pay now and avoid service interruption. Thank you."

    # Generate speech using ElevenLabs
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers=headers,
        json={"text": text, "model_id": "eleven_monolingual_v1", "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}},
    )

    if response.status_code != 200:
        raise Exception("ElevenLabs TTS failed")

    with open("voice_message.mp3", "wb") as f:
        f.write(response.content)

    # Upload voice to Twilio-hosted URL or S3 bucket, then call
    # For demo, we will just call and use Twilio's <Say> fallback
    call = client.calls.create(
        to=to,
        from_=TWILIO_PHONE,
        twiml=f"<Response><Say>{text}</Say></Response>"
    )
    return call.sid
