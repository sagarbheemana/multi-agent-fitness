"""
Nutrition and diet agent - GROK VERSION
"""
from langchain import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def create_diet_agent():
    """Create nutrition and diet agent with GROK"""
    model = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768",
        temperature=0.3,
    )

    system_prompt = """You are a wellness nutritionist specializing in general dietary guidance. Your role:
1. Provide balanced nutrition information
2. Suggest nutrient-rich foods for specific goals
3. Explain dietary principles
4. Recommend meal planning approaches
5. Address common dietary concerns

Important guidelines:
- NEVER prescribe specific medical diets
- Acknowledge when professional dietitian is needed
- Base suggestions on whole, nutrient-dense foods
- Consider cultural and personal preferences

Format responses as:
- Assessment of nutritional goal/concern
- General nutrition principles
- Specific food suggestions (5-7 examples)
- Implementation strategy
"""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt,
    )

    return agent


async def provide_nutrition_guidance(query: str, conversation_context: str = "") -> dict:
    """Provide nutritional guidance"""
    agent = create_diet_agent()

    messages = []
    if conversation_context:
        messages.append({"role": "system", "content": f"Previous context:\n{conversation_context}"})
    
    messages.append({"role": "user", "content": query})

    try:
        response = await agent.ainvoke({"messages": messages})
        content = response.get("messages", [])[-1].content if response.get("messages") else ""
        
        return {
            "success": True,
            "agent_name": "Nutrition Guide",
            "content": content,
            "confidence": 0.80,
            "recommendations": extract_recommendations(content),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_name": "Nutrition Guide",
        }


def extract_recommendations(content: str) -> list:
    """Extract nutrition recommendations"""
    recommendations = []
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith("•") or line.startswith("-") or line.startswith("*")):
            rec = line.lstrip("•-* ")
            if rec and len(rec) > 8:
                recommendations.append(rec)
    
    return recommendations[:5]