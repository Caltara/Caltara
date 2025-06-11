import streamlit as st
import pandas as pd
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials
twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE")
client = Client(twilio_sid, twilio_auth_token)

# Streamlit UI
st.title("📞 Caltara – AI Collections Agent")
st.markdown("Upload your CSV of past-due customers, and Caltara will call them automatically.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("Start Calls"):
        st.info("Starting calls...")

        for i, row in df.iterrows():
            name = row['name']
            phone = row['phone']
            balance = row['balance_due']
            due = row['due_date']

            message = (
                f"Hello {name}, this is Caltara calling on behalf of your service provider. "
                f"Our records show a past-due balance of ${balance} was due on {due}. "
                f"We'd love to help you resolve this today. Please contact us or visit the payment link sent to your phone. Thank you."
            )

            # Place the call
            try:
                call = client.calls.create(
                    twiml=f'<Response><Say voice="alice">{message}</Say></Response>',
                    to=phone,
                    from_=twilio_phone
                )
                st.success(f"📞 Called {name} at {phone}")
            except Exception as e:
                st.error(f"❌ Failed to call {name} at {phone}: {e}")
