"""
Agent orchestrator - routes queries to appropriate agents and manages execution
"""
import asyncio
from typing import Optional, List
from models.schemas import WellnessQuery, IntentType, AgentResponse, UserProfile
from memory.short_memory import MemoryManager
from agents.symptom_agent import assess_symptoms
from agents.lifestyle_agent import analyze_lifestyle
from agents.diet_agent import provide_nutrition_guidance
from agents.fitness_agent import provide_fitness_guidance


class WellnessOrchestrator:
    """
    Coordinates multiple wellness agents to provide comprehensive guidance
    """

    def __init__(self):
        self.memory_manager = MemoryManager()
        self.intent_keywords = {
            IntentType.SYMPTOM: [
                "symptom", "ache", "pain", "tired", "fatigue", "sick", 
                "illness", "feel", "hurt", "sore", "dizzy", "nausea",
                "cough", "fever", "headache"
            ],
            IntentType.LIFESTYLE: [
                "sleep", "stress", "anxiety", "routine", "habit", "relax",
                "tired", "fatigue", "meditation", "work-life", "balance",
                "energy", "mood", "mental"
            ],
            IntentType.DIET: [
                "food", "eat", "diet", "nutrition", "meal", "cook",
                "recipe", "calorie", "protein", "healthy", "weight",
                "appetite", "digest", "stomach"
            ],
            IntentType.FITNESS: [
                "exercise", "workout", "gym", "run", "walk", "strength",
                "cardio", "fit", "activity", "sport", "train", "muscle",
                "flexibility", "endurance"
            ],
        }

    def identify_intent(self, query: str) -> IntentType:
        """
        Identify the primary intent of user query
        """
        query_lower = query.lower()
        intent_scores = {intent: 0 for intent in IntentType}

        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    intent_scores[intent] += 1

        max_intent = max(intent_scores, key=intent_scores.get)
        
        if intent_scores[max_intent] == 0:
            return IntentType.GENERAL
        
        return max_intent

    async def execute_agent_query(
        self,
        wellness_query: WellnessQuery,
    ) -> List[AgentResponse]:
        """
        Execute queries across relevant agents
        """
        if not wellness_query.intent:
            wellness_query.intent = self.identify_intent(wellness_query.query)

        context = self.memory_manager.get_conversation_context(wellness_query.user_id)

        agent_tasks = []
        
        if wellness_query.intent == IntentType.SYMPTOM:
            agent_tasks.append(assess_symptoms(wellness_query.query, context))
        elif wellness_query.intent == IntentType.LIFESTYLE:
            agent_tasks.append(analyze_lifestyle(wellness_query.query, context))
        elif wellness_query.intent == IntentType.DIET:
            agent_tasks.append(provide_nutrition_guidance(wellness_query.query, context))
        elif wellness_query.intent == IntentType.FITNESS:
            agent_tasks.append(provide_fitness_guidance(wellness_query.query, context))
        else:
            agent_tasks = [
                assess_symptoms(wellness_query.query, context),
                analyze_lifestyle(wellness_query.query, context),
                provide_nutrition_guidance(wellness_query.query, context),
                provide_fitness_guidance(wellness_query.query, context),
            ]

        try:
            results = await asyncio.gather(*agent_tasks, return_exceptions=True)
        except Exception as e:
            print(f"Error executing agent tasks: {e}")
            results = []

        agent_responses = []
        for result in results:
            if isinstance(result, dict) and result.get("success"):
                agent_responses.append(
                    AgentResponse(
                        agent_name=result.get("agent_name", "Unknown"),
                        content=result.get("content", ""),
                        confidence=result.get("confidence", 0.7),
                        recommendations=result.get("recommendations", []),
                    )
                )

        self.memory_manager.add_user_message(wellness_query.user_id, wellness_query.query)

        return agent_responses

    def filter_intent_safety(self, intent: IntentType, query: str) -> tuple:
        """
        Safety filter for specific intents
        """
        warning_message = ""
        
        critical_symptoms = [
            "chest pain", "difficulty breathing", "severe bleeding",
            "loss of consciousness", "seizure", "suicidal", "harm"
        ]
        
        if intent == IntentType.SYMPTOM:
            for symptom in critical_symptoms:
                if symptom in query.lower():
                    return False, f"CRITICAL: Seek emergency medical care immediately (911)"
        
        return True, warning_message

    async def process_wellness_query(
        self,
        wellness_query: WellnessQuery,
    ) -> dict:
        """
        Complete workflow to process user query
        """
        intent = self.identify_intent(wellness_query.query)
        wellness_query.intent = intent

        is_safe, warning = self.filter_intent_safety(intent, wellness_query.query)
        
        if not is_safe:
            return {
                "user_id": wellness_query.user_id,
                "query": wellness_query.query,
                "intent": intent.value,
                "agent_responses": [],
                "synthesized_guidance": warning,
                "primary_recommendations": [],
                "warning": warning,
                "requires_emergency": True,
            }

        agent_responses = await self.execute_agent_query(wellness_query)

        return {
            "user_id": wellness_query.user_id,
            "query": wellness_query.query,
            "intent": intent.value,
            "agent_responses": [
                {
                    "agent_name": resp.agent_name,
                    "content": resp.content,
                    "confidence": resp.confidence,
                    "recommendations": resp.recommendations,
                }
                for resp in agent_responses
            ],
            "agent_count": len(agent_responses),
        }

    def get_user_memory_context(self, user_id: str) -> dict:
        """Get user's conversation memory and context"""
        return self.memory_manager.get_memory_stats(user_id)

    def clear_user_memory(self, user_id: str):
        """Clear user's conversation history"""
        self.memory_manager.clear_memory(user_id)