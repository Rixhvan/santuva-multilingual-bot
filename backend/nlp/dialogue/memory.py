from typing import Dict, Any, Optional, List, Tuple
from backend.models.schemas import DialogueState

class ConversationMemory:
    """
    In-memory short-term conversational context tracker.
    Stores recent turns, resolved topics, user entities (e.g., user name),
    previous intents, and supports anaphoric reference resolution (e.g., 'it', 'this').
    """

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self.sessions: Dict[str, DialogueState] = {}

    def get_or_create_state(self, session_id: str) -> DialogueState:
        """Retrieves active dialogue state or creates a clean session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = DialogueState(
                conversation_id=session_id,
                turn_count=0,
                accumulated_entities={},
                recent_turns=[]
            )
        return self.sessions[session_id]

    def update_state(
        self,
        session_id: str,
        user_text: str,
        bot_response: str,
        lang: str,
        intent: str,
        entities: Dict[str, Any],
        topic: Optional[str] = None
    ) -> DialogueState:
        """Updates dialogue state with the latest conversational turn."""
        state = self.get_or_create_state(session_id)
        state.turn_count += 1
        state.previous_language = lang
        state.last_intent = intent

        if topic:
            state.current_topic = topic

        # Store accumulated entities (e.g. user name)
        for k, v in entities.items():
            if isinstance(v, list):
                state.accumulated_entities[k] = v[-1]
            else:
                state.accumulated_entities[k] = str(v)

        # Maintain short-term turn buffer
        state.recent_turns.append({
            "turn": state.turn_count,
            "user": user_text,
            "bot": bot_response,
            "language": lang,
            "intent": intent,
            "topic": state.current_topic
        })

        if len(state.recent_turns) > self.max_turns:
            state.recent_turns.pop(0)

        return state

    def resolve_anaphora(self, text: str, session_id: str) -> Tuple[str, bool, Optional[str]]:
        """
        Resolves pronouns such as 'it', 'this', 'that', 'तत्' (tat), 'ಉಂದು' (undu)
        using current session topic and recent entities.
        Returns: (resolved_text, was_resolved, antecedent)
        """
        state = self.get_or_create_state(session_id)
        text_lower = text.lower()
        antecedent = state.current_topic

        # If user asks "What is my name?" and name is known
        if "my name" in text_lower or "मम नाम" in text or "ಎನ್ನ ಪುದರ್" in text:
            if "person" in state.accumulated_entities:
                return text, True, state.accumulated_entities["person"]

        # Pronoun check for 'it', 'this', 'that'
        pronouns_en = ["about it", "when was it", "where is it", "tell me about it", "what is it"]
        pronouns_sa = ["तस्य विषये", "तत् कुत्र", "कदा तत्"]
        pronouns_tu = ["ಅಯಿತ್ತ ಬಗ್ಗೆ", "ಅವು ವಾಡೆ", "ಉಂದು ದಾನೆ"]

        has_pronoun = any(p in text_lower for p in pronouns_en) or any(p in text for p in pronouns_sa) or any(p in text for p in pronouns_tu)

        if has_pronoun:
            if antecedent:
                # Antecedent exists, resolve successfully
                resolved = text
                if "it" in text_lower:
                    resolved = text.replace(" it", f" {antecedent}").replace("It", antecedent)
                return resolved, True, antecedent
            else:
                # Ambiguous: pronoun with no antecedent!
                return text, False, None

        return text, False, antecedent

    def clear(self, session_id: str):
        """Resets conversational memory for a given session."""
        if session_id in self.sessions:
            del self.sessions[session_id]

conversation_memory = ConversationMemory()
