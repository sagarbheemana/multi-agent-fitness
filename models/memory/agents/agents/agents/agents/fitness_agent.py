"""
Fitness and exercise agent - GROK VERSION
"""
from langchain import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def create_fitness_agent():
    """Create fitness and exercise agent with GROK"""
    model = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
        temperature=0.4,
    )

    system_prompt = """You are a fitness wellness coach providing general exercise guidance. Your expertise:
1. Exercise principles and benefits
2. Beginner-friendly workout suggestions
3. Injury prevention strategies
4. Fitness goal setting
5. Activity recommendations for different preferences

Guidelines:
- Suggest modifications for different fitness levels
- Emphasize proper form and safety
- Recommend consulting professionals for specific conditions
- Include both cardio and strength concepts
- Always start with safety considerations

Format responses as:
- Assessment of fitness goal/question
- Safety considerations (first)
- Exercise recommendations (3-5 options)
- Implementation progression (week 1, 2, 3)
- Form tips and modifications
"""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt,
    )

    return agent


async def provide_fitness_guidance(query: str, conversation_context: str = "") -> dict:
    """Provide fitness guidance"""
    agent = create_fitness_agent()

    messages = []
    if conversation_context:
        messages.append({"role": "system", "content": f"Previous context:\n{conversation_context}"})
    
    messages.append({"role": "user", "content": query})

    try:
        response = await agent.ainvoke({"messages": messages})
        content = response.get("messages", [])[-1].content if response.get("messages") else ""
        
        return {
            "success": True,
            "agent_name": "Fitness Coach",
            "content": content,
            "confidence": 0.81,
            "recommendations": extract_recommendations(content),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_name": "Fitness Coach",
        }


def extract_recommendations(content: str) -> list:
    """Extract fitness recommendations"""
    recommendations = []
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith("•") or line.startswith("-") or line.startswith("*")):
            rec = line.lstrip("•-* ")
            if rec and len(rec) > 8:
                recommendations.append(rec)
    
    return recommendations[:5]