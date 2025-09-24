# AskRemoHealth AI Chatbot Backend

This repository contains the complete backend service for the AskRemoHealth AI Chatbot Assistant. Built with FastAPI, it provides a creative, context-aware, and empathetic conversational experience for patients, guiding them from initial contact to specialist booking.

## Core Features

- **Conversational Intelligence**: Powered by Google Gemini for natural, non-repetitive dialogue with full conversational memory.
- **Patient-Centric Flow**: A multi-stage conversation designed to listen, reassure, and guide users without being robotic or rushed.
- **Session Management**: Thread-safe, in-memory session handling with a 6-hour automatic cleanup cycle.
- **Scalable Architecture**: Designed to handle a high volume of concurrent sessions.
- **Easy Deployment**: Includes a one-run setup script for Debian/Ubuntu-based VPS environments.

---

## Getting Started

### 1. Environment Configuration

Create a `.env` file in the project root (`askremo_backend/`) and add your Google Gemini API key:

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Specify a Gemini model (defaults to models/gemini-1.5-flash)
# GEMINI_MODEL=models/gemini-1.5-pro
```

### 2. Local Development Setup

These steps will get you running on your local machine.

```bash
# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

---

## Deployment on a Contabo VPS

This project includes a setup script to automate deployment on a fresh Debian/Ubuntu VPS.

1.  **Upload Project**: Transfer the `askremo_backend` directory to your VPS.
2.  **Navigate to Project Root**: `cd askremo_backend`
3.  **Make Script Executable**:
    ```bash
    chmod +x setup_vps.sh
    ```
4.  **Run the Setup Script**:
    ```bash
    ./setup_vps.sh
    ```

The script will update the system, install Python, create a virtual environment, and install all dependencies.

### Running in Production

After setup, activate the environment and run the app using a production-grade server like Gunicorn:

```bash
# Activate the environment
source venv/bin/activate

# Start the application with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

For a permanent setup, it is recommended to run the application as a `systemd` service.

---

## API Endpoints

### Main Chat Endpoint

-   **URL**: `/chat`
-   **Method**: `POST`
-   **Request Body**:
    ```json
    {
      "session_id": "<unique_session_string>",
      "message": "<user_message_string>"
    }
    ```
-   **Response Body**:
    ```json
    {
      "response": "<chatbot_response_string>",
      "stage": "<current_conversation_stage>",
      "session_active": true,
      "interaction_count": 1,
      "expires_in": "5h 59m"
    }
    ```

### Health Check

-   **URL**: `/health`
-   **Method**: `GET`
-   **Description**: Returns the operational status, active session count, and uptime.

### API Documentation

Interactive API documentation is available when the server is running:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`
