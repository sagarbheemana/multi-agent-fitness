
# 🚀 Digital Wellness Assistant

**Multi-Agent Wellness System powered by Grok LLM (xAI)**  

[![Status](https://img.shields.io/badge/status-working-brightgreen.svg)](http://localhost:8000/health)
[![API Docs](https://img.shields.io/badge/API-Docs-blue.svg)](http://localhost:8000/docs)
[![Grok](https://img.shields.io/badge/LLM-Grok%20(xAI)-00D4AA.svg)](https://console.groq.com)

A production-ready **4-agent AI wellness system** offering intelligent guidance across symptoms, diet, fitness, and lifestyle domains.

---

## ✨ Features
```

✅ Symptom Assessment Agent
✅ Lifestyle Coach Agent
✅ Nutrition Guide Agent
✅ Fitness Coach Agent
✅ Automatic Intent Classification
✅ Conversation Memory
✅ REST API (FastAPI + Uvicorn)
✅ Swagger UI Documentation
✅ Safety Filters + Emergency Detection
✅ JSON Responses (frontend-ready)

```

---

## 🏗️ Architecture (Clean & Neat)
```

```
                ┌──────────────────────────┐
                │        User Input        │
                │      (REST Request)      │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │     Intent Classifier    │
                │ (LLM-based Routing Brain)│
                └─────────────┬────────────┘
                              │
            ┌─────────────────┼──────────────────┐
            ▼                 ▼                  ▼
  ┌────────────────┐   ┌───────────────┐   ┌────────────────┐
  │ Symptom Agent  │   │ Lifestyle     │   │ Diet Agent      │
  │ (fatigue, pain)│   │ Agent         │   │ (foods, meals)  │
  └────────────────┘   └───────────────┘   └────────────────┘
            │                 │                  │
            └──────────────┬──┴──┬──────────────┘
                           │     │
                           ▼     ▼
                    ┌───────────────────┐
                    │   Fitness Agent   │
                    │ (workouts, plans) │
                    └─────────┬─────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │   Response Synthesizer   │
                │ (Combines agent results) │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │     Final JSON Output    │
                └──────────────────────────┘
```

````

---

## 🎯 Live API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Health check |
| `POST` | `/wellness/query` | Main wellness query |
| `GET`  | `/docs` | Swagger UI |
| `GET`  | `/` | Welcome route |

---

## 🚀 Quick Start

### 1️⃣ Install Requirements
```bash
git clone <repo>
cd digital_wellness_backend
pip install -r requirements.txt
````

### 2️⃣ Configure API Key

```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

### 3️⃣ Run Server

```bash
python main.py
```

```
INFO: Uvicorn running on http://0.0.0.0:8000 ✨
```

---

## 🧪 Testing the API

### PowerShell Test

```powershell
Invoke-RestMethod http://localhost:8000/health

$body = @{ user_id="test"; query="I feel tired" } | ConvertTo-Json
Invoke-RestMethod http://localhost:8000/wellness/query -Method Post -Body $body -ContentType "application/json"
```

---

## 📊 Sample Responses

### Symptom Query

```json
{
  "user_id": "user1",
  "query": "I feel tired",
  "intent": "symptom",
  "synthesized_guidance": "## Symptom Assessment...\n• Hydrate\n• Sleep 7-8 hours\n• Light walking",
  "primary_recommendations": ["Hydrate", "Sleep", "Walk 10 minutes"],
  "agent_count": 1
}
```

### Diet Query

```json
{
  "intent": "diet",
  "primary_recommendations": ["Oats + berries", "Nuts", "Salmon"],
  "agent_count": 1
}
```

---

## 🛠️ Tech Stack

```
🤖 LLM: Grok (xAI) via langchain-groq  
🌐 Backend: FastAPI + Uvicorn  
📘 Schemas: Pydantic v2  
🧠 Multi-Agent Architecture  
📱 REST + Swagger UI  
🐳 Docker-ready
```

---

## 📱 Frontend / Postman Integration

```
🔥 CORS enabled  
🔥 Pure JSON responses  
🔥 Plug-and-play with React / Vue / Angular / Flutter  
```

Postman Example:

```json
POST http://localhost:8000/wellness/query
Content-Type: application/json
{"user_id":"test","query":"I feel stressed"}
```

---

## 🔧 Developer Commands

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📈 Agent Performance

| Agent     | Model      | Purpose                 | Speed       |
| --------- | ---------- | ----------------------- | ----------- |
| Symptom   | Mixtral    | Medical symptoms        | ⚡ Fast      |
| Lifestyle | Llama3-70B | Sleep & stress coaching | 🎯 Accurate |
| Diet      | Mixtral    | Nutrition               | ⚡ Fast      |
| Fitness   | Llama3-70B | Workouts                | 🎯 Detailed |

---

## ⚠️ Safety

```
🚨 Emergency detection (chest pain, suicidal → safety alert)
❌ No medical diagnosis
ℹ️ Educational guidance only
```

---

## 📚 Contributing

1. Fork repo
2. Create feature branch
3. Commit & push
4. Open PR

---

## 📄 License

MIT License — Free for commercial + personal use.

---

## 🎉 Made with ❤️ for Wellness

**Deploy → Scale → Improve Lives!**

```

---

If you want:

✅ **project folder structure**  
✅ **main.py, routers, agents, memory, models**  
✅ **Docker Compose + CI/CD**  

Just say **"generate full backend"**.

