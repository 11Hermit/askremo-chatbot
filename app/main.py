import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import time

# Load environment variables
load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(title="AskRemoHealth AI Chatbot Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.models.response_models import HealthResponse
from app.services.session_manager import session_manager
from app.background.tasks import start_background_tasks
from datetime import datetime
import psutil

START_TIME = datetime.utcnow()

@app.on_event("startup")
def startup_event():
    start_background_tasks()

@app.get("/health", response_model=HealthResponse)
def health():
    uptime = datetime.utcnow() - START_TIME
    sessions = session_manager.count()
    return HealthResponse(
        status="healthy",
        sessions=sessions,
        uptime=f"{uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
    )

# Custom exception handler for 500 errors
def setup_logging():
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

setup_logging()

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# --- Chat endpoint ---
from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse
from app.services.session_manager import session_manager
from app.services.conversation_ai import get_ai_response
from app.utils.helpers import get_time_left
from fastapi import Body

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, request: Request):
    # Get or create session
    session = session_manager.get(payload.session_id)
    if not session:
        session = session_manager.create(payload.session_id, user_agent=request.headers.get("user-agent"), ip_address=request.client.host)
    # Generate AI response
    ai_response = get_ai_response(session, payload.message)
    # Update session
    now = datetime.utcnow()
    session.conversation_history.append({
        "timestamp": now.isoformat(),
        "user_message": payload.message,
        "bot_response": ai_response,
        "interaction_number": session.conversation_state["interaction_count"] + 1
    })
    session.conversation_state["interaction_count"] += 1
    session.last_activity = now
    # Stage and closure logic placeholder (to be enhanced)
    stage = session.conversation_state["current_stage"]
    session_active = session.expires_at > now
    expires_in = get_time_left(session.expires_at)
    return ChatResponse(
        response=ai_response,
        stage=stage,
        session_active=session_active,
        interaction_count=session.conversation_state["interaction_count"],
        expires_in=expires_in
    )

# --- Session termination endpoint ---
@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    session_manager.delete(session_id)
    return {"message": "Session terminated"}
