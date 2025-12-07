"""
Response synthesizer - combines agent responses into coherent guidance
"""
from typing import List
from models.schemas import AgentResponse, WellnessResponse, IntentType
import textwrap


class ResponseSynthesizer:
    """
    Synthesizes multiple agent responses into unified wellness guidance
    """

    def __init__(self):
        self.max_recommendation_length = 100
        self.min_confidence_threshold = 0.65

    def synthesize_responses(
        self,
        user_id: str,
        query: str,
        intent: IntentType,
        agent_responses: List[AgentResponse],
    ) -> WellnessResponse:
        """
        Combine agent responses into final guidance
        """
        valid_responses = [
            r for r in agent_responses 
            if r.confidence >= self.min_confidence_threshold
        ]

        if not valid_responses:
            valid_responses = agent_responses

        synthesized_text = self._synthesize_by_intent(
            intent, valid_responses, query
        )

        primary_recommendations = self._extract_unified_recommendations(
            valid_responses, limit=7
        )

        response = WellnessResponse(
            user_id=user_id,
            query=query,
            intent=intent,
            agent_responses=valid_responses,
            synthesized_guidance=synthesized_text,
            primary_recommendations=primary_recommendations,
            disclaimer="This is educational wellness guidance, not medical advice. "
                      "Consult healthcare professionals for medical concerns.",
        )

        return response

    def _synthesize_by_intent(
        self,
        intent: IntentType,
        responses: List[AgentResponse],
        query: str,
    ) -> str:
        """
        Synthesize response based on intent type
        """
        if not responses:
            return self._get_fallback_guidance(intent)

        if intent == IntentType.SYMPTOM:
            return self._synthesize_symptom_response(responses, query)
        elif intent == IntentType.LIFESTYLE:
            return self._synthesize_lifestyle_response(responses, query)
        elif intent == IntentType.DIET:
            return self._synthesize_diet_response(responses, query)
        elif intent == IntentType.FITNESS:
            return self._synthesize_fitness_response(responses, query)
        else:
            return self._synthesize_general_response(responses, query)

    def _synthesize_symptom_response(
        self, responses: List[AgentResponse], query: str
    ) -> str:
        """Synthesize symptom-related guidance"""
        primary = responses[0] if responses else None
        
        synthesis = f"""
## Symptom Assessment

**Your concern:** {query}

**Initial Assessment:**
{textwrap.fill(primary.content[:300] + "..." if primary else "Unable to assess.", width=80)}

**Key Recommendations:**
"""
        if primary and primary.recommendations:
            for i, rec in enumerate(primary.recommendations[:4], 1):
                synthesis += f"\n{i}. {rec}"
        
        synthesis += "\n\n**Important Note:**\n"
        synthesis += "This is general wellness perspective. If symptoms persist, worsen, or are severe, please consult a healthcare provider.\n"
        
        return synthesis

    def _synthesize_lifestyle_response(
        self, responses: List[AgentResponse], query: str
    ) -> str:
        """Synthesize lifestyle guidance"""
        primary = responses[0] if responses else None
        
        synthesis = f"""
## Lifestyle & Wellness Guidance

**Your question:** {query}

**Recommended Approach:**
{textwrap.fill(primary.content[:250] + "..." if primary else "Unable to provide guidance.", width=80)}

**Action Items:**
"""
        if primary and primary.recommendations:
            for i, rec in enumerate(primary.recommendations[:5], 1):
                synthesis += f"\n• {rec}"
        
        synthesis += "\n\n**Implementation Strategy:**\n"
        synthesis += "Start with 1-2 recommendations that resonate most with you. Build momentum gradually.\n"
        
        return synthesis

    def _synthesize_diet_response(
        self, responses: List[AgentResponse], query: str
    ) -> str:
        """Synthesize nutrition guidance"""
        primary = responses[0] if responses else None
        
        synthesis = f"""
## Nutrition & Diet Guidance

**Your question:** {query}

**Nutritional Perspective:**
{textwrap.fill(primary.content[:250] + "..." if primary else "No nutrition guidance available.", width=80)}

**Food Suggestions:**
"""
        if primary and primary.recommendations:
            for i, rec in enumerate(primary.recommendations[:5], 1):
                synthesis += f"\n• {rec}"
        
        synthesis += "\n\n**Dietary Note:**\n"
        synthesis += "For specific medical dietary needs, consult a registered dietitian.\n"
        
        return synthesis

    def _synthesize_fitness_response(
        self, responses: List[AgentResponse], query: str
    ) -> str:
        """Synthesize fitness guidance"""
        primary = responses[0] if responses else None
        
        synthesis = f"""
## Fitness & Exercise Guidance

**Your question:** {query}

**Exercise Recommendation:**
{textwrap.fill(primary.content[:250] + "..." if primary else "No exercise guidance available.", width=80)}

**Suggested Activities:**
"""
        if primary and primary.recommendations:
            for i, rec in enumerate(primary.recommendations[:5], 1):
                synthesis += f"\n• {rec}"
        
        synthesis += "\n\n**Safety Note:**\n"
        synthesis += "Start gradually and listen to your body. Stop if you experience pain. Consult healthcare provider before starting new programs.\n"
        
        return synthesis

    def _synthesize_general_response(
        self, responses: List[AgentResponse], query: str
    ) -> str:
        """Synthesize general/multi-intent response"""
        synthesis = f"""
## Comprehensive Wellness Perspective

**Your question:** {query}

**Multi-Dimensional Assessment:**
"""
        for response in responses[:4]:
            if response.confidence > 0.7:
                synthesis += f"\n\n**{response.agent_name}:**\n"
                synthesis += textwrap.fill(response.content[:200] + "...", width=80)
        
        synthesis += "\n\n**Integrated Recommendations:**\n"
        all_recs = self._extract_unified_recommendations(responses, limit=6)
        for i, rec in enumerate(all_recs, 1):
            synthesis += f"\n{i}. {rec}"
        
        return synthesis

    def _extract_unified_recommendations(
        self, responses: List[AgentResponse], limit: int = 5
    ) -> List[str]:
        """
        Extract and deduplicate recommendations from multiple agents
        """
        all_recs = []
        seen = set()
        
        for response in responses:
            for rec in response.recommendations:
                rec_lower = rec.lower()[:50]
                if rec_lower not in seen:
                    all_recs.append(rec)
                    seen.add(rec_lower)
        
        return all_recs[:limit]

    def _get_fallback_guidance(self, intent: IntentType) -> str:
        """Get fallback guidance when agents don't respond"""
        fallback_messages = {
            IntentType.SYMPTOM: "Unable to assess symptoms at this time. Please consult a healthcare provider.",
            IntentType.LIFESTYLE: "Unable to provide lifestyle guidance. Consider consulting a wellness coach.",
            IntentType.DIET: "Unable to provide nutrition guidance. Consult a registered dietitian.",
            IntentType.FITNESS: "Unable to provide fitness guidance. Consult a fitness professional.",
            IntentType.GENERAL: "Unable to process your query. Please rephrase and try again.",
        }
        
        return fallback_messages.get(intent, "Unable to provide guidance at this time.")