import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Caltara – Virtual Assistant", layout="centered")

# Branding
st.title("🤖 Caltara – Your Virtual Business Assistant")
st.markdown("Hi! I'm **Caltara**, here to help with client messages and billing support.")

# Mode selection
mode = st.radio("What would you like to do?", ["📬 Leave a Message", "💰 Billing/Collections Help"])

if mode == "📬 Leave a Message":
    st.subheader("📬 Message to Business")
    name = st.text_input("Your Name")
    phone = st.text_input("Phone Number")
    message = st.text_area("Your Message")

    if st.button("Send Message"):
        if name and phone and message:
            st.success("✅ Message sent! The business will contact you shortly.")
            st.write("### Message Summary")
            st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Name:** {name}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**Message:** {message}")
        else:
            st.error("❌ Please fill in all fields.")

elif mode == "💰 Billing/Collections Help":
    st.subheader("💳 Account Lookup")

    acct_name = st.text_input("Your Full Name")
    acct_phone = st.text_input("Phone or Email on File")

    if acct_name and acct_phone:
        # Simulated account data
        balance = 237.50
        due_date = "2025-05-20"

        st.success(f"Account found! Balance due: **${balance:.2f}** (Due: {due_date})")
        option = st.selectbox("How would you like to proceed?", [
            "Select an option...",
            "✅ Pay Full Amount",
            "📆 Set Up Payment Plan",
            "❓ Ask a Billing Question"
        ])

        if option == "✅ Pay Full Amount":
            st.markdown("Click [here](https://example.com/pay) to pay now. Thank you!")

        elif option == "📆 Set Up Payment Plan":
            weeks = st.slider("Spread payments over how many weeks?", 1, 6, 2)
            weekly_payment = balance / weeks
            st.info(f"Payment Plan: **{weeks} weeks** at **${weekly_payment:.2f}/week**")
            st.markdown("We’ll send you an email with the plan details shortly.")

        elif option == "❓ Ask a Billing Question":
            question = st.text_area("Please describe your concern:")
            if question and st.button("Submit Question"):
                st.success("Your question has been forwarded to the billing team.")
