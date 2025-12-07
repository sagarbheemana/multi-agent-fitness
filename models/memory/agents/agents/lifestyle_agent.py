"""
Lifestyle and wellness habits agent - GROK VERSION
"""
from langchain import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def create_lifestyle_agent():
    """Create lifestyle wellness agent with GROK"""
    model = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
        temperature=0.4,
    )

    system_prompt = """You are a lifestyle and wellness habits coach. Your expertise includes:
1. Sleep hygiene and quality rest
2. Stress management techniques
3. Daily routine optimization
4. Mental wellness practices
5. Work-life balance

When responding:
- Ask about current habits if not provided
- Suggest 3-5 practical, actionable lifestyle changes
- Consider individual preferences and constraints
- Provide evidence-based recommendations

Format as:
- Current pattern analysis
- Recommended changes
- Implementation tips (3-5 specific actions)
"""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt,
    )

    return agent


async def analyze_lifestyle(query: str, conversation_context: str = "") -> dict:
    """Analyze lifestyle and provide recommendations"""
    agent = create_lifestyle_agent()

    messages = []
    if conversation_context:
        messages.append({"role": "system", "content": f"Previous context:\n{conversation_context}"})
    
    messages.append({"role": "user", "content": query})

    try:
        response = await agent.ainvoke({"messages": messages})
        content = response.get("messages", [])[-1].content if response.get("messages") else ""
        
        return {
            "success": True,
            "agent_name": "Lifestyle Coach",
            "content": content,
            "confidence": 0.82,
            "recommendations": extract_recommendations(content),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_name": "Lifestyle Coach",
        }


def extract_recommendations(content: str) -> list:
    """Extract actionable recommendations"""
    recommendations = []
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if line and (line.startswith("•") or line.startswith("-") or line.startswith("*")):
            rec = line.lstrip("•-* ")
            if rec and len(rec) > 10:
                recommendations.append(rec)
    
    return recommendations[:5]