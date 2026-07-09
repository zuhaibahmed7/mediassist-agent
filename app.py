import streamlit as st
import sys
sys.setrecursionlimit(10000)
import uuid
from agent import chat_with_agent
from mongodb_tools import (
    get_user_by_email, create_user, get_recent_chat_history,
    get_all_sessions, get_session_messages, verify_user
)

st.set_page_config(page_title="MediAssist", page_icon="🩺", layout="centered")

st.title("🩺 MediAssist")
st.caption("Your personal health information assistant — powered by Qwen + MongoDB")

# --- Session State Setup ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory_context" not in st.session_state:
    st.session_state.memory_context = []

# --- Login / Signup ---
if st.session_state.user_id is None:
    st.subheader("👋 Welcome to MediAssist")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # --- Login Tab ---
    with tab1:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if login_email and login_password:
                user = verify_user(login_email, login_password)
                if user:
                    st.session_state.user_id = str(user["_id"])
                    history = get_recent_chat_history(st.session_state.user_id)
                    st.session_state.messages = history
                    st.session_state.memory_context = history
                    st.rerun()
                else:
                    st.error("❌ Incorrect email or password.")
            else:
                st.warning("Please enter both email and password.")

    # --- Sign Up Tab ---
    with tab2:
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Create Account"):
            if signup_name and signup_email and signup_password and signup_confirm:
                if signup_password != signup_confirm:
                    st.error("❌ Passwords do not match.")
                elif len(signup_password) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                else:
                    existing = get_user_by_email(signup_email)
                    if existing:
                        st.error("❌ An account with this email already exists. Please login.")
                    else:
                        new_id = create_user(
                            name=signup_name,
                            age=0,
                            gender="",
                            email=signup_email,
                            password=signup_password
                        )
                        st.session_state.user_id = new_id
                        st.session_state.messages = []
                        st.session_state.memory_context = []
                        st.rerun()
            else:
                st.warning("Please fill in all fields.")

# --- Chat Interface ---
else:
    st.success("Logged in ✅")

    if len(st.session_state.messages) > 0:
        st.info("👋 Welcome back! I remember our previous conversation.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Describe your symptoms or ask a health question...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_context = st.session_state.memory_context + st.session_state.messages
                reply = chat_with_agent(
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id,
                    user_message=user_input,
                    conversation_history=full_context
                )
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.memory_context.append({"role": "user", "content": user_input})
        st.session_state.memory_context.append({"role": "assistant", "content": reply})

    # --- Sidebar ---
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("MediAssist provides general health information. It is **not a substitute** for professional medical advice.")

        st.divider()

        if st.button("➕ New Conversation"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        st.divider()
        st.subheader("🕑 Chat History")

        sessions = get_all_sessions(st.session_state.user_id)

        if not sessions:
            st.caption("No previous chats yet")
        else:
            for s in sessions:
                label = s["preview"] if s["preview"] else "New Chat"
                if st.button(label, key=s["session_id"]):
                    st.session_state.session_id = s["session_id"]
                    st.session_state.messages = get_session_messages(
                        st.session_state.user_id, s["session_id"]
                    )
                    st.rerun()

        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.user_id = None
            st.session_state.messages = []
            st.session_state.memory_context = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
