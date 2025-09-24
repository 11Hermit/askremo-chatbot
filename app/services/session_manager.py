import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import uuid4
from copy import deepcopy
import os

SESSION_TIMEOUT_HOURS = int(os.getenv("SESSION_TIMEOUT_HOURS", 6))

class SessionData:
    def __init__(self, session_id, user_agent=None, ip_address=None):
        now = datetime.utcnow()
        self.session_id = session_id
        self.created_at = now
        self.last_activity = now
        self.expires_at = now + timedelta(hours=SESSION_TIMEOUT_HOURS)
        self.conversation_history = []
        self.patient_context = {
            "symptoms_mentioned": [],
            "concerns_raised": [],
            "questions_asked": [],
            "booking_interest_expressed": False,
            "self_care_discussed": False
        }
        self.conversation_state = {
            "current_stage": "welcome",
            "interaction_count": 0,
            "ready_for_closure": False,
            "booking_offered": False,
            "consultation_complete": False
        }
        self.metadata = {
            "user_agent": user_agent or "",
            "ip_address": ip_address or "",
            "total_response_time": 0.0,
            "gemini_calls_made": 0
        }

    def as_dict(self):
        return deepcopy(self.__dict__)

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        self.lock = threading.Lock()

    def get(self, session_id: str) -> Optional[SessionData]:
        with self.lock:
            session = self.sessions.get(session_id)
            if session and session.expires_at > datetime.utcnow():
                session.last_activity = datetime.utcnow()
                return session
            elif session:
                del self.sessions[session_id]
            return None

    def create(self, session_id: Optional[str] = None, user_agent=None, ip_address=None) -> SessionData:
        with self.lock:
            sid = session_id or str(uuid4())
            session = SessionData(sid, user_agent, ip_address)
            self.sessions[sid] = session
            return session

    def delete(self, session_id: str):
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]

    def cleanup(self):
        with self.lock:
            expired = [sid for sid, s in self.sessions.items() if s.expires_at <= datetime.utcnow()]
            for sid in expired:
                del self.sessions[sid]

    def count(self):
        with self.lock:
            return len(self.sessions)

    def all(self):
        with self.lock:
            return deepcopy(self.sessions)

session_manager = SessionManager()
