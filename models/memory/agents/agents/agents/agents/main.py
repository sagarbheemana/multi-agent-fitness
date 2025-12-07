"""
Digital Wellness Assistant - COMPLETE MAIN.PY (GROK VERSION)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Digital Wellness Assistant",
    description="Multi-agent wellness guidance system (GROK)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple mock orchestrator/synthesizer (replace with real ones later)
class MockOrchestrator:
    def process_wellness_query(self, query):
        return {
            "user_id": query["user_id"],
            "query": query["query"],
            "intent": self.detect_intent(query["query"]),
            "agent_responses": self.get_agent_responses(query["query"]),
            "agent_count": 1
        }
    
    def detect_intent(self, query):
        query_lower = query.lower()
        if any(word in query_lower for word in ["tired", "pain", "headache", "sick"]):
            return "symptom"
        elif any(word in query_lower for word in ["sleep", "stress", "routine"]):
            return "lifestyle"
        elif any(word in query_lower for word in ["food", "eat", "diet"]):
            return "diet"
        elif any(word in query_lower for word in ["exercise", "workout", "gym"]):
            return "fitness"
        return "general"
    
    def get_agent_responses(self, query):
        query_lower = query.lower()
        if "tired" in query_lower:
            return [{
                "agent_name": "Symptom Assessment",
                "content": "## Symptom Assessment\n\n**Your concern:** " + query + "\n\n**Analysis:** Fatigue can be caused by poor sleep, dehydration, or stress.\n\n**Recommendations:**\n• Drink 8-10 glasses of water daily\n• Aim for 7-8 hours of quality sleep\n• Take 10-minute walks daily\n• Practice deep breathing exercises\n\n**When to seek help:** If fatigue persists >2 weeks or worsens.",
                "confidence": 0.85,
                "recommendations": ["Drink 8-10 glasses water", "7-8 hours sleep", "10-min walks", "Deep breathing"]
            }]
        elif "food" in query_lower or "eat" in query_lower:
            return [{
                "agent_name": "Nutrition Guide",
                "content": "## Nutrition Guidance\n\n**Your question:** " + query + "\n\n**Recommendations:**\n• Eat complex carbs (oats, sweet potatoes, quinoa)\n• Include healthy fats (avocado, nuts, olive oil)\n• Protein sources (eggs, fish, legumes)\n• Leafy greens and colorful vegetables\n• Stay hydrated throughout day\n\n**Sample meal:** Oatmeal + berries + nuts breakfast.",
                "confidence": 0.80,
                "recommendations": ["Complex carbs", "Healthy fats", "Quality protein", "Leafy greens", "Stay hydrated"]
            }]
        elif "exercise" in query_lower:
            return [{
                "agent_name": "Fitness Coach",
                "content": "## Fitness Guidance\n\n**Your question:** " + query + "\n\n**Beginner Plan:**\n• **Week 1:** 20-min brisk walking daily\n• **Week 2:** Add bodyweight squats (3x10)\n• **Week 3:** Add push-ups (knee version, 3x8)\n\n**Safety:** Start slow, proper form, stop if pain.\n**Progress:** Increase time/reps gradually.",
                "confidence": 0.81,
                "recommendations": ["20-min walks", "Bodyweight squats", "Knee push-ups", "Proper form first"]
            }]
        else:
            return [{
                "agent_name": "Lifestyle Coach",
                "content": "## General Wellness\n\n**Query:** " + query + "\n\n**Holistic Approach:**\n• Prioritize sleep hygiene\n• Stay consistently hydrated\n• Move body daily (even walking)\n• Practice stress management\n• Eat whole nutrient-dense foods",
                "confidence": 0.75,
                "recommendations": ["Sleep hygiene", "Hydration", "Daily movement", "Stress management", "Whole foods"]
            }]

orchestrator = MockOrchestrator()

class QueryRequest(BaseModel):
    user_id: str
    query: str
    intent: Optional[str] = None
    user_profile: Optional[dict] = None

class QueryResponse(BaseModel):
    user_id: str
    query: str
    intent: str
    agent_responses: List[dict]
    synthesized_guidance: str
    primary_recommendations: List[str]
    agent_count: int
    warning: Optional[str] = None
    requires_emergency: bool = False

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    agents_available: int

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        agents_available=4
    )

@app.post("/wellness/query", response_model=QueryResponse)
async def wellness_query(request: QueryRequest):
    try:
        logger.info(f"Processing query from {request.user_id}: {request.query[:50]}...")
        
        # Check for emergency keywords
        emergency_keywords = ["chest pain", "can't breathe", "suicidal"]
        if any(keyword in request.query.lower() for keyword in emergency_keywords):
            return QueryResponse(
                user_id=request.user_id,
                query=request.query,
                intent="emergency",
                agent_responses=[],
                synthesized_guidance="🚨 CRITICAL: Seek emergency medical help immediately (911)",
                primary_recommendations=[],
                agent_count=0,
                warning="EMERGENCY REQUIRED",
                requires_emergency=True
            )
        
        # Process query
        result = orchestrator.process_wellness_query({
            "user_id": request.user_id,
            "query": request.query
        })
        
        # Synthesize response
        synthesized_guidance = result["agent_responses"][0]["content"] if result["agent_responses"] else "No guidance available"
        recommendations = result["agent_responses"][0]["recommendations"] if result["agent_responses"] else []
        
        return QueryResponse(
            user_id=result["user_id"],
            query=result["query"],
            intent=result["intent"],
            agent_responses=result["agent_responses"],
            synthesized_guidance=synthesized_guidance,
            primary_recommendations=recommendations,
            agent_count=result["agent_count"]
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wellness/intents")
async def get_intents():
    return {"intents": ["symptom", "lifestyle", "diet", "fitness", "general"]}

@app.get("/")
async def root():
    return {
        "name": "Digital Wellness Assistant (GROK)",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "query": "/wellness/query (POST)",
            "intents": "/wellness/intents",
            "docs": "/docs"
        },
        "message": "🚀 Ready! Test with: curl -X POST http://localhost:8000/wellness/query -d '{\"user_id\":\"test\",\"query\":\"I feel tired\"}' -H 'Content-Type: application/json'"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")