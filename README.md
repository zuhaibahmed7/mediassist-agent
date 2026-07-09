[README.md](https://github.com/user-attachments/files/29637186/README.4.md)
# MediAssist — AI Health Information Agent

MediAssist is a conversational AI agent that helps users understand symptoms, get medication information, and receive personalized health guidance.

Built for the **Qwen Cloud Hackathon 2026** — MemoryAgent Track.

## Features

-  **Conversational Health Assistant** — Ask health questions in natural language
-  **Persistent Memory** — Remembers you across sessions (MemoryAgent track)
-  **Chat History** — View and revisit past conversations (like ChatGPT)
-  **User Profiles** — Personalized experience stored in MongoDB
-  **Responsible AI** — Always recommends professional medical help when needed

## Architecture

```
User (Streamlit Web UI)
        ↓
   Qwen AI Agent (qwen-plus model)
        ↓
   MongoDB Atlas (users, symptom_logs, chat_history)
        ↓
   Deployed on Alibaba Cloud ECS (Singapore)
```

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Qwen (qwen-plus) via Qwen Cloud
- **Database:** MongoDB Atlas
- **Cloud:** Alibaba Cloud ECS (Singapore)
- **Language:** Python 3.9

## Project Structure

```
mediassist-agent/
├── app.py              # Streamlit UI
├── agent.py            # Qwen AI agent logic
├── mongodb_tools.py    # MongoDB connection and functions
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Getting Started

### Prerequisites
- Python 3.9+
- MongoDB Atlas account
- Qwen Cloud API key
- Alibaba Cloud account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/zuhaibahmed7/mediassist-agent.git
cd mediassist-agent
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```
MONGO_URI=your_mongodb_connection_string
DB_NAME=mediassist_db
QWEN_API_KEY=your_qwen_api_key
```

5. Run the app:
```bash
streamlit run app.py
```

6. Open browser at `http://localhost:8501`

## Live Demo

Access the live deployed version at:
```
http://47.84.195.213:8501
```

## MemoryAgent Track Features

This project specifically addresses the MemoryAgent track requirements:

- ✅ **Persistent memory** across sessions stored in MongoDB
- ✅ **User preference tracking** via user profiles
- ✅ **Cross-session context** loaded on login
- ✅ **Efficient memory retrieval** with MongoDB queries
- ✅ **Timely memory management** — last 20 messages loaded per session
- ✅ **Chat history sidebar** — browse and reload past conversations

## Database Design

### Collections in MongoDB Atlas (`mediassist_db`):

| Collection | Purpose |
|---|---|
| `users` | Stores user profiles and health info |
| `symptom_logs` | Tracks all symptom checks |
| `chat_history` | Full conversation logs per session |

## Alibaba Cloud Deployment

The backend is deployed on **Alibaba Cloud ECS** (Singapore region):
- Instance: Burstable Type t6, 2 vCPU, 4 GiB RAM
- OS: CentOS 7
- Port: 8501 (Streamlit)
- Running via: Python virtual environment

## Disclaimer

MediAssist provides general health information only. It is **not a substitute** for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
