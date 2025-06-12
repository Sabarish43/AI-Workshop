import streamlit as st
import requests

# --- Configuration ---
USERNAME = "admin"
PASSWORD = "pass123"
WEBHOOK_URL = "https://your-n8n-instance.com/webhook/action-items"  # Replace with your actual n8n webhook

# --- Authentication Check ---
def login():
    st.title("🔐 Employee Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

# --- Logout ---
def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# --- Action Item Form ---
def show_action_form():
    st.title("📋 Submit Meeting Action Items")

    with st.form("action_form"):
        employee_name = st.text_input("Your Name")
        meeting_date = st.date_input("Meeting Date")
        action_items = st.text_area("Action Items")
        submit = st.form_submit_button("Submit")

        if submit:
            payload = {
                "employee_name": employee_name,
                "meeting_date": meeting_date.strftime("%Y-%m-%d"),
                "action_items": action_items,
            }

            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("Action items submitted successfully!")
                else:
                    st.error(f"Failed to submit. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error sending data: {e}")

    st.button("Logout", on_click=logout)

# --- Main App ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_action_form()
    else:
        login()

if __name__ == "__main__":
    main()
