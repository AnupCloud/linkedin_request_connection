#!/bin/bash

# LinkedIn Automation - Streamlit App Launcher
# This script activates the virtual environment and runs the Streamlit app

echo "🔗 Starting LinkedIn Automation Web App..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
streamlit run app.py
