#!/bin/bash

# Deployment script for AskRemoHealth Chatbot Backend on a Contabo VPS (Debian/Ubuntu)
# This script should be run from the project's root directory.

echo "--- AskRemoHealth Backend Setup ---"

# Exit script on any error
set -e

# 1. Update system packages and install Python essentials
echo "[1/4] Updating system and installing python3, pip, and venv..."
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv

# 2. Create a Python virtual environment
echo "[2/4] Creating virtual environment 'venv'..."
if [ -d "venv" ]; then
    echo "Virtual environment 'venv' already exists. Skipping creation."
else
    python3 -m venv venv
fi

# 3. Activate the virtual environment and install requirements
echo "[3/4] Activating virtual environment and installing project requirements..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Deactivate the virtual environment for a clean exit
echo "[4/4] Deactivating virtual environment..."
deactivate

echo "
--- Setup Complete! ---"
echo "The 'venv' virtual environment is ready."
echo "To activate it, run: source venv/bin/activate"
echo "To run the application, use a command like: uvicorn app.main:app --host 0.0.0.0 --port 8000"
