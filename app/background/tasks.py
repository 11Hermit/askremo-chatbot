from apscheduler.schedulers.background import BackgroundScheduler
from app.services.session_manager import session_manager
import logging
import os

CLEANUP_INTERVAL_MINUTES = int(os.getenv("CLEANUP_INTERVAL_MINUTES", 30))

scheduler = BackgroundScheduler()

def cleanup_sessions():
    session_manager.cleanup()
    logging.info("Session cleanup executed.")

scheduler.add_job(cleanup_sessions, 'interval', minutes=CLEANUP_INTERVAL_MINUTES)

def start_background_tasks():
    if not scheduler.running:
        scheduler.start()
        logging.info("Background scheduler started.")
