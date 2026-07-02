import streamlit as st
import uuid
from agent import chat_with_agent
from mongodb_tools import (
    get_user_by_email, create_user, get_recent_chat_history,
    get_all_sessions, get_session_messages
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
    st.session_state.memory_context = []  # Persistent memory, survives "New Conversation"

# --- Simple Login (Email-based) ---
if st.session_state.user_id is None:
    st.subheader("👋 Welcome! Enter your email to get started")
    email = st.text_input("Email")
    name = st.text_input("Name")

    if st.button("Continue"):
        if email and name:
            user = get_user_by_email(email)
            if user:
                st.session_state.user_id = str(user["_id"])
            else:
                new_id = create_user(name=name, age=0, gender="", email=email)
                st.session_state.user_id = new_id

            # Load past history once — used for both display AND long-term memory
            history = get_recent_chat_history(st.session_state.user_id)
            st.session_state.messages = history
            st.session_state.memory_context = history

            st.rerun()
        else:
            st.warning("Please enter both name and email.")

# --- Chat Interface ---
else:
    st.success("Logged in ✅")

    if len(st.session_state.messages) > 0:
        st.info("👋 Welcome back! I remember our previous conversation.")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Describe your symptoms or ask a health question...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Combine long-term memory + current visible messages for context
                full_context = st.session_state.memory_context + st.session_state.messages

                reply = chat_with_agent(
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id,
                    user_message=user_input,
                    conversation_history=full_context
                )
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        # Update memory context too, so it carries forward
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
            # memory_context is NOT cleared — agent still remembers you!
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