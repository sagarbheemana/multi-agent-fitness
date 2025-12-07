from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

app = FastAPI(title="Digital Wellness Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    user_id: str
    query: str
    intent: str
    synthesized_guidance: str
    recommendations: list

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/wellness/query")
async def wellness_query(request: QueryRequest):
    query_lower = request.query.lower()
    
    # Intent detection & mock responses
    if any(word in query_lower for word in ["tired", "pain", "headache"]):
        intent = "symptom"
        guidance = """
## Symptom Assessment
**Concern:** {query}

**Recommendations:**
• Drink 8-10 glasses water daily
• Get 7-8 hours sleep nightly  
• Take 10-minute walks
• Reduce caffeine after 2pm

**Note:** Consult doctor if persists >2 weeks.
        """.format(query=request.query)
        recs = ["Hydrate", "Sleep 7-8hrs", "Walk 10min", "Less caffeine"]
    elif any(word in query_lower for word in ["food", "eat", "diet"]):
        intent = "diet"
        guidance = """
## Nutrition Guide
**Question:** {query}

**Energy Foods:**
• Oats + berries breakfast
• Nuts + avocado snack
• Salmon + quinoa dinner
• Green smoothies

**Hydrate consistently!**
        """.format(query=request.query)
        recs = ["Oats+berries", "Nuts+avocado", "Salmon+quinoa", "Green smoothie"]
    elif any(word in query_lower for word in ["exercise", "workout"]):
        intent = "fitness"
        guidance = """
## Fitness Coach  
**Goal:** {query}

**Beginner Plan:**
Week 1: 20min brisk walk daily
Week 2: Add squats (3x10)
Week 3: Add pushups (3x8)

**Safety first - proper form!**
        """.format(query=request.query)
        recs = ["20min walk", "Squats 3x10", "Pushups 3x8", "Proper form"]
    else:
        intent = "general"
        guidance = f"""
## Wellness Guidance
**Query:** {request.query}

**Holistic Tips:**
• Sleep 7-8 hours nightly
• Drink water consistently  
• Walk 20 minutes daily
• Eat whole foods
• Practice deep breathing
        """
        recs = ["Sleep 7-8hrs", "Hydrate", "Walk 20min", "Whole foods"]
    
    return QueryResponse(
        user_id=request.user_id,
        query=request.query,
        intent=intent,
        synthesized_guidance=guidance,
        recommendations=recs
    )

@app.get("/")
async def root():
    return {
        "status": "🚀 Digital Wellness Assistant READY!",
        "test": "POST to /wellness/query with: {\"user_id\":\"test\",\"query\":\"I feel tired\"}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)