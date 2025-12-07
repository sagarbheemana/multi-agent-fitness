"""
Symptom assessment agent - GROK VERSION
"""
from langchain import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def create_symptom_agent():
    """Create symptom assessment agent with GROK"""
    model = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768",
        temperature=0.3,
    )

    system_prompt = """You are a wellness symptom assessment specialist. Your role is to:
1. Understand the user's reported symptoms
2. Ask clarifying questions if needed
3. Provide general wellness suggestions
4. Identify when professional medical advice is needed
5. NEVER diagnose medical conditions

Format your response with:
- Symptom summary
- General wellness suggestions (3-5 items)
- When to seek professional help

Always emphasize: "This is general wellness guidance, not medical advice."
"""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt,
    )

    return agent


async def assess_symptoms(query: str, conversation_context: str = "") -> dict:
    """Assess user symptoms"""
    agent = create_symptom_agent()

    messages = []
    if conversation_context:
        messages.append({"role": "system", "content": f"Previous context:\n{conversation_context}"})
    
    messages.append({"role": "user", "content": query})

    try:
        response = await agent.ainvoke({"messages": messages})
        content = response.get("messages", [])[-1].content if response.get("messages") else ""
        
        return {
            "success": True,
            "agent_name": "Symptom Assessment",
            "content": content,
            "confidence": 0.85,
            "recommendations": extract_recommendations(content),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_name": "Symptom Assessment",
        }


def extract_recommendations(content: str) -> list:
    """Extract recommendations from agent response"""
    recommendations = []
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if line.startswith("•") or line.startswith("-") or line.startswith("*"):
            recommendations.append(line.lstrip("•-* "))
    
    return recommendations[:5]