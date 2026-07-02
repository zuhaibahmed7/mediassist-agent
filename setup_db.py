from mongodb_tools import *

# Test connection
test_connection()

# Add sample users
user1_id = create_user(
    name="Zuhaib Ahmed",
    age=22,
    gender="male",
    email="zuhaib@email.com",
    blood_type="O+",
    allergies=["penicillin"],
    chronic_conditions=["diabetes"],
    medications=["metformin"]
)
print(f"✅ User 1 created: {user1_id}")

user2_id = create_user(
    name="Sara",
    age=23,
    gender="female",
    email="sarah@email.com",
    blood_type="A+",
    allergies=[],
    chronic_conditions=[],
    medications=[]
)
print(f"✅ User 2 created: {user2_id}")

# Add sample symptom log
log_id = log_symptom(
    user_id=user1_id,
    symptoms=["headache", "fever", "fatigue"],
    severity="moderate",
    duration="2 days",
    agent_response="Could be viral infection. Rest and stay hydrated.",
    recommended_action="Monitor symptoms. See doctor if fever exceeds 39°C."
)
print(f"✅ Symptom log created: {log_id}")

# Add sample chat history
save_chat(user1_id, "session_001", "user", "I have a headache and fever")
save_chat(user1_id, "session_001", "agent", "Could be viral infection. Rest and stay hydrated.")
print("✅ Chat history saved!")

print("\n Database setup complete! Check MongoDB Atlas to see your collections.")