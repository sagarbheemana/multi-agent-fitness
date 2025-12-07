"""
Short-term memory management for user conversations
"""
from typing import Dict
from models.schemas import ConversationMemory


class MemoryManager:
    """Manages conversation memory for users"""

    def __init__(self, max_users: int = 100):
        self.memory_store: Dict[str, ConversationMemory] = {}
        self.max_users = max_users

    def get_or_create_memory(self, user_id: str) -> ConversationMemory:
        """Get existing memory or create new one"""
        if user_id not in self.memory_store:
            if len(self.memory_store) >= self.max_users:
                oldest_key = next(iter(self.memory_store))
                del self.memory_store[oldest_key]
            self.memory_store[user_id] = ConversationMemory(user_id=user_id)
        return self.memory_store[user_id]

    def add_user_message(self, user_id: str, message: str):
        """Add user message to memory"""
        memory = self.get_or_create_memory(user_id)
        memory.add_message("user", message)

    def add_assistant_message(self, user_id: str, message: str):
        """Add assistant response to memory"""
        memory = self.get_or_create_memory(user_id)
        memory.add_message("assistant", message)

    def get_conversation_context(self, user_id: str) -> str:
        """Get formatted conversation context"""
        memory = self.get_or_create_memory(user_id)
        return memory.get_context()

    def update_user_context(self, user_id: str, context: dict):
        """Update user context information"""
        memory = self.get_or_create_memory(user_id)
        memory.context.update(context)

    def clear_memory(self, user_id: str):
        """Clear user memory"""
        if user_id in self.memory_store:
            del self.memory_store[user_id]

    def get_memory_stats(self, user_id: str) -> dict:
        """Get memory statistics"""
        memory = self.get_or_create_memory(user_id)
        return {
            "user_id": user_id,
            "message_count": len(memory.messages),
            "context_keys": list(memory.context.keys()),
            "last_message": memory.messages[-1] if memory.messages else None,
        }