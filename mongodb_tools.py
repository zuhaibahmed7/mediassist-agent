import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

# Collections
users_col = db["users"]
symptom_logs_col = db["symptom_logs"]
chat_history_col = db["chat_history"]

def test_connection():
    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def create_user(name, age, gender, email, blood_type="", allergies=[], chronic_conditions=[], medications=[]):
    user = {
        "name": name,
        "age": age,
        "gender": gender,
        "email": email,
        "blood_type": blood_type,
        "allergies": allergies,
        "chronic_conditions": chronic_conditions,
        "medications": medications,
        "created_at": datetime.utcnow()
    }
    result = users_col.insert_one(user)
    return str(result.inserted_id)

def log_symptom(user_id, symptoms, severity, duration, agent_response, recommended_action):
    log = {
        "user_id": user_id,
        "symptoms": symptoms,
        "severity": severity,
        "duration": duration,
        "agent_response": agent_response,
        "recommended_action": recommended_action,
        "timestamp": datetime.utcnow()
    }
    result = symptom_logs_col.insert_one(log)
    return str(result.inserted_id)

def save_chat(user_id, session_id, role, content):
    chat_history_col.update_one(
        {"user_id": user_id, "session_id": session_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow()
                }
            },
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True
    )

def get_user_by_email(email):
    return users_col.find_one({"email": email})

def get_symptom_history(user_id):
    return list(symptom_logs_col.find({"user_id": user_id}))

# Test connection when file runs
if __name__ == "__main__":
    test_connection()

def get_recent_chat_history(user_id, limit=20):
    """
    Retrieves the most recent messages across all sessions for a user.
    """
    sessions = chat_history_col.find({"user_id": user_id})
    all_messages = []
    for session in sessions:
        all_messages.extend(session.get("messages", []))
    
    # Sort by timestamp
    all_messages.sort(key=lambda x: x["timestamp"])
    
    # Return only role + content (last N messages)
    return [{"role": m["role"], "content": m["content"]} for m in all_messages[-limit:]]

def get_all_sessions(user_id):
    """
    Returns a list of all chat sessions for a user,
    with a preview (first user message) and session_id.
    """
    sessions = chat_history_col.find({"user_id": user_id}).sort("created_at", -1)
    
    session_list = []
    for session in sessions:
        messages = session.get("messages", [])
        # Find first user message as preview
        preview = "New Chat"
        for msg in messages:
            if msg["role"] == "user":
                preview = msg["content"][:40] + ("..." if len(msg["content"]) > 40 else "")
                break
        
        session_list.append({
            "session_id": session["session_id"],
            "preview": preview,
            "created_at": session.get("created_at")
        })
    
    return session_list


def get_session_messages(user_id, session_id):
    """
    Returns messages for a specific session_id.
    """
    session = chat_history_col.find_one({"user_id": user_id, "session_id": session_id})
    if session:
        return [{"role": m["role"], "content": m["content"]} for m in session.get("messages", [])]
    return []