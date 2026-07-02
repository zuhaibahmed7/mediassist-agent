import os
from openai import OpenAI
from dotenv import load_dotenv
from mongodb_tools import save_chat, log_symptom, get_symptom_history

load_dotenv()

# Qwen Cloud client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

SYSTEM_PROMPT = """You are MediAssist, a helpful health information assistant.
You help users understand symptoms, provide general health information,
and explain medications. You are NOT a doctor.
Always recommend seeing a real doctor for serious or persistent symptoms.
Keep responses clear, simple, and supportive."""

def chat_with_agent(user_id, session_id, user_message, conversation_history=None):
    """
    Sends user message to Qwen model and returns the agent's response.
    Also saves the conversation to MongoDB.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include past conversation for memory/context
    if conversation_history:
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )

    agent_reply = response.choices[0].message.content

    # Save both messages to MongoDB
    save_chat(user_id, session_id, "user", user_message)
    save_chat(user_id, session_id, "assistant", agent_reply)

    return agent_reply


# Quick test
if __name__ == "__main__":
    test_user_id = "test_user_001"
    test_session_id = "test_session_001"
    
    reply = chat_with_agent(
        user_id=test_user_id,
        session_id=test_session_id,
        user_message="I have a headache and feel tired"
    )
    print("Agent:", reply)