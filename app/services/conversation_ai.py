from datetime import datetime
from typing import Dict
from app.utils.prompts import SYSTEM_PROMPT_TEMPLATE
from app.services.gemini_client import GeminiClient

from app.utils.prompts import SYSTEM_PROMPT_TEMPLATE
BOOKING_LINK = "https://askremohealth.com/find-specialists"

STAGES = [
    "welcome",
    "listening",
    "assessing",
    "guiding",
    "booking",
    "closing"
]

def next_stage(current, user_message, interaction_count):
    # Only allow booking after at least 3 stages or clear booking intent
    booking_intent = any(word in user_message.lower() for word in ["book", "appointment", "specialist", "doctor", "yes"])
    if current == "welcome":
        return "listening"
    elif current == "listening":
        return "assessing"
    elif current == "assessing":
        if booking_intent and interaction_count >= 3:
            return "booking"
        return "guiding"
    elif current == "guiding":
        if booking_intent and interaction_count >= 3:
            return "booking"
        # If we've reached guiding and 3+ stages, allow booking next
        if interaction_count >= 3:
            return "booking"
        return "closing"
    elif current == "booking":
        return "closing"
    return "closing"

gemini_client = GeminiClient()

def build_conversation_history(session):
    history = session.conversation_history[-5:]  # Use last 5 turns for context
    if not history:
        return "No previous conversation."
    return "\n".join([
        f"User: {i['user_message']}\nAssistant: {i['bot_response']}"
        for i in history
    ])

def get_ai_response(session, user_message):
    stage = session.conversation_state["current_stage"]
    interaction_count = session.conversation_state["interaction_count"]
    history_str = build_conversation_history(session)

    # Special handling for the two-step booking process
    if stage == "booking" and not session.conversation_state.get("booking_offer_made"):
        session.conversation_state["booking_offer_made"] = True
        # The prompt will guide Gemini to ask for confirmation
    
    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        conversation_history=history_str,
        patient_context=session.patient_context,
        interaction_count=interaction_count,
        current_stage=stage,
        user_message=user_message
    )

    ai_response = gemini_client.generate_response(prompt)

    # Only advance the stage if we are not waiting for booking confirmation
    if not (stage == "booking" and session.conversation_state.get("booking_offer_made") and not any(word in user_message.lower() for word in ["yes", "no", "okay", "sure"])):
        session.conversation_state["current_stage"] = next_stage(stage, user_message, interaction_count + 1)
    
    return ai_response
