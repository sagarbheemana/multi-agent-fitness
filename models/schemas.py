"""
Data models and schemas for wellness assistant
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class IntentType(str, Enum):
    """Wellness intent categories"""
    SYMPTOM = "symptom"
    LIFESTYLE = "lifestyle"
    DIET = "diet"
    FITNESS = "fitness"
    GENERAL = "general"


class UserProfile(BaseModel):
    """User profile for context"""
    user_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    health_conditions: List[str] = Field(default_factory=list)
    preferences: dict = Field(default_factory=dict)


class WellnessQuery(BaseModel):
    """Input query structure"""
    user_id: str
    query: str
    intent: Optional[IntentType] = None
    user_profile: Optional[UserProfile] = None


class AgentResponse(BaseModel):
    """Individual agent response"""
    agent_name: str
    content: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    recommendations: List[str] = Field(default_factory=list)


class WellnessResponse(BaseModel):
    """Final synthesized response"""
    user_id: str
    query: str
    intent: IntentType
    agent_responses: List[AgentResponse]
    synthesized_guidance: str
    primary_recommendations: List[str]
    disclaimer: str = "This is educational guidance, not medical advice."


class ConversationMemory(BaseModel):
    """Short-term memory for conversation"""
    user_id: str
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    max_messages: int = 20

    def add_message(self, role: str, content: str):
        """Add message to memory"""
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> str:
        """Get formatted context for agents"""
        formatted = []
        for msg in self.messages[-5:]:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)