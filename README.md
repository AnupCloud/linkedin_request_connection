# 🔗 LinkedIn Automation Crew

An intelligent LinkedIn automation tool powered by CrewAI that automatically sends personalized connection requests. This version uses an asynchronous architecture for improved performance and supports both single and batch processing through a command-line interface or a user-friendly Streamlit web app.

![LinkedIn Automation](https://img.shields.io/badge/LinkedIn-Automation-blue?style=for-the-badge&logo=linkedin)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit)
![Async](https://img.shields.io/badge/Async-Optimized-purple?style=for-the-badge)

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Setup](#-setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- 🔐 **Secure Credential Management**: Store credentials safely in a local `.env` file.
- 🚀 **Asynchronous Execution**: Fast, non-blocking operations for efficient automation.
-  batch **Batch Processing**: Send connection requests to multiple people concurrently.
- 🌐 **Streamlit Web UI**: Easy-to-use interface to configure and run the automation.
- 🤖 **AI-Powered**: Uses CrewAI for intelligent, multi-step task automation.
- 📝 **Personalized Notes**: Customize connection messages for single or batch runs.
- 🎯 **Smart Profile Search**: Automatically finds profiles by name and selects the first result.

---

## 📦 Prerequisites

- **Python 3.10 or higher**
- **`uv` package manager** ([Installation guide](https://github.com/astral-sh/uv))
- **Google Chrome Browser**
- **An LLM API Key** (e.g., Anthropic, OpenAI, Gemini)

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd linkedin_msg
```

### 2. Create and Activate Virtual Environment

This project uses `uv` for fast dependency management.

```bash
# Create the virtual environment
uv venv

# Activate the environment
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages from pyproject.toml
uv pip install -e .
```

### 4. Configure Environment Variables

Copy the example `.env` file and fill in your details.

```bash
cp .env.example .env
```

Now, open the `.env` file and add your credentials:

```env
# LLM API Key (e.g., Anthropic)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# LinkedIn Credentials (Required)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password_here

# --- For Single Person Mode ---
PERSON_NAME=John Smith
CONNECTION_NOTE=Hi John, would love to connect!

# --- For Batch Mode ---
BATCH_MODE=false
PERSON_NAMES="Jane Doe,Bob Smith"
CONNECTION_NOTES="Hi Jane, let's connect!|Hi Bob, great profile!"
```

---

## 📖 Usage

You can run the automation via the recommended Streamlit Web UI or the command line.

### 🚀 Method 1: Streamlit Web UI (Recommended)

The web UI provides the easiest way to manage credentials, configure targets, and run the automation.

**To start the app:**

```bash
streamlit run app.py
```

This will open the dashboard in your browser. From there, you can:
1.  Go to the **Credentials** tab to save your LinkedIn and API keys.
2.  Go to the **Quick Start** tab to enter a person's name and connection note.
3.  Click **Run Automation** to start the process.

### 💻 Method 2: Command Line Interface

The CLI uses the asynchronous `main_async.py` script for fast execution.

#### A) Single Person Mode

1.  Ensure `BATCH_MODE` is set to `false` in your `.env` file.
2.  Set the `PERSON_NAME` and `CONNECTION_NOTE` variables.
3.  Run the script:

```bash
python -m src.linkedin_msg.main_async
```

#### B) Batch Mode

1.  Set `BATCH_MODE=true` in your `.env` file.
2.  Add names to `PERSON_NAMES`, separated by commas (`,`).
3.  Add corresponding notes to `CONNECTION_NOTES`, separated by pipes (`|`).
4.  Run the script:

```bash
python -m src.linkedin_msg.main_async
```

The script will process all connection requests concurrently, providing a summary at the end.

---

## 📁 Project Structure

```
linkedin_msg/
│
├── app.py                  # Streamlit web application
├── .env                    # Your environment variables
├── .env.example            # Example environment variables
├── pyproject.toml          # Project dependencies and metadata
├── README.md               # This file
│
└── src/
    └── linkedin_msg/
        ├── main.py         # (DEPRECATED) Synchronous script
        ├── main_async.py   # Asynchronous script for CLI runs
        ├── crew.py         # CrewAI agent and task definitions
        ├── tools/          # Custom tools for browser automation
        └── config/         # YAML configs for agents and tasks
```

---

## 🔧 Troubleshooting

- **Login Failed**: Double-check your `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` in the `.env` file. This tool does not support 2FA.
- **ChromeDriver Error**: Ensure Google Chrome is installed. The `webdriver-manager` should handle the driver automatically. If not, try `uv pip install --upgrade webdriver-manager`.
- **No Search Results**: Make sure the `PERSON_NAME` is spelled correctly. Try using a more specific name (e.g., "John Smith at Microsoft").

⚠️ **Disclaimer**: Use this tool responsibly and in accordance with LinkedIn's Terms of Service. The authors are not responsible for any account restrictions.