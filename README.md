# 🔗 LinkedIn Automation Tool

An intelligent LinkedIn automation tool powered by CrewAI that automatically sends personalized connection requests. Features include smart profile search, AI-powered automation, and a user-friendly Streamlit web interface.

![LinkedIn Automation](https://img.shields.io/badge/LinkedIn-Automation-blue?style=for-the-badge&logo=linkedin)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit)

---

## 📋 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Security](#-security)

---

## ✨ Features

- 🔐 **Secure Credential Management**: Store credentials safely in `.env` file
- 🔍 **Smart Profile Search**: Automatically finds profiles by name
- 🎯 **First Result Selection**: Always selects the FIRST person from search results
- 📝 **Personalized Notes**: Send custom connection messages
- 🤖 **AI-Powered**: Uses CrewAI for intelligent automation
- 🌐 **Web Interface**: User-friendly Streamlit dashboard
- 📊 **Real-time Logging**: See exactly what's happening at each step
- 🔄 **Dynamic Configuration**: Change target person via .env file

---

## 🔄 How It Works

The automation follows a 4-step process:

```
1. LOGIN → Logs into LinkedIn using your credentials from .env file
2. SEARCH → Searches for the exact person name you specified
3. SELECT → Automatically selects the FIRST person in search results
4. CONNECT → Sends connection request with your personalized note
```

---

## 📦 Prerequisites

- **Python 3.10 or higher**
- **Google Chrome Browser**
- **Git**
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))

---

## 🚀 Installation

### Step 1: Clone the Repository

\`\`\`bash
git clone <repository-url>
cd linkedin_msg
\`\`\`

### Step 2: Create Virtual Environment

**macOS/Linux:**
\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
\`\`\`

**Windows:**
\`\`\`bash
python -m venv .venv
.venv\Scripts\activate
\`\`\`

### Step 3: Install Dependencies

\`\`\`bash
pip install -e .
\`\`\`

This installs:
- `crewai[tools]` - AI automation framework
- `selenium` - Browser automation
- `python-dotenv` - Environment variables
- `streamlit` - Web application framework

---

## ⚙️ Configuration

### Create `.env` File

Create a `.env` file in the project root:

\`\`\`env
# Anthropic API Key (Required for CrewAI)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# LinkedIn Credentials (Required)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password_here

# LinkedIn Automation Settings (Required)
PERSON_NAME=John Smith
CONNECTION_NOTE=Hi! I came across your profile and would love to connect. I'm interested in your work and would like to expand my professional network. Looking forward to connecting with you!
\`\`\`

---

## 📖 Usage

### 1. Web Interface (Streamlit) - RECOMMENDED

#### Start the Web Application

\`\`\`bash
streamlit run app.py
\`\`\`

This opens your browser at `http://localhost:8501`

#### Using the Web Interface

1. **Quick Start Tab**
   - Enter the person's name
   - Write your connection note
   - Click "💾 Save Configuration"

2. **Run the Automation**
   - Click "🚀 Run Automation"
   - Watch real-time progress
   - See success confirmation

3. **Credentials Tab**
   - Enter LinkedIn email and password
   - Click "💾 Save Credentials"

![Streamlit Interface](./screenshots/streamlit_app/01_app_homepage.png)

---

### 2. Command Line

\`\`\`bash
python src/linkedin_msg/main.py
\`\`\`

#### What You'll See

\`\`\`
[DEBUG] Searching for: John Smith
[INFO] ✓ Found search results for 'John Smith'
[INFO] → Selecting FIRST person from search results...
[INFO] ✓ SELECTED FIRST RESULT: John Smith
[DEBUG] ✓ Found Connect button
[INFO] ✓ Clicked Connect button
[DEBUG] ✓ Found 'Add a note' button
[INFO] ✓ Typed personalized note
[DEBUG] ✓ Found Send button
[INFO] ✓ Clicked Send button
[INFO] ══════════════════════════════════════════
[INFO] ✓ CONNECTION REQUEST SENT SUCCESSFULLY!
[INFO] ══════════════════════════════════════════
\`\`\`

---

## 📸 Screenshots

### Setup Process

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![Clone](./screenshots/setup/01_clone_repository.png) | Clone the repository |
| 2 | ![Install](./screenshots/setup/02_install_dependencies.png) | Install dependencies |
| 3 | ![Configure](./screenshots/setup/03_env_configuration.png) | Configure .env file |
| 4 | ![Verify](./screenshots/setup/04_verify_installation.png) | Verify installation |

### Automation Process

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![Login](./screenshots/automation_process/01_linkedin_login.png) | LinkedIn login |
| 2 | ![Search](./screenshots/automation_process/02_search_person.png) | Search for person |
| 3 | ![Select](./screenshots/automation_process/03_first_result_selected.png) | First result selected |
| 4 | ![Connect](./screenshots/automation_process/04_connect_button_found.png) | Connect button found |
| 5 | ![Note](./screenshots/automation_process/05_add_note_dialog.png) | Add note dialog |
| 6 | ![Send](./screenshots/automation_process/06_connection_request_sent.png) | Request sent |
| 7 | ![Success](./screenshots/automation_process/07_success_confirmation.png) | Success confirmation |

### Streamlit Web Application

| Screen | Screenshot | Description |
|--------|------------|-------------|
| Homepage | ![Home](./screenshots/streamlit_app/01_app_homepage.png) | Main dashboard |
| Configuration | ![Config](./screenshots/streamlit_app/02_configuration_tab.png) | Enter details |
| Credentials | ![Creds](./screenshots/streamlit_app/03_credentials_tab.png) | Manage credentials |
| Running | ![Run](./screenshots/streamlit_app/04_running_automation.png) | Automation progress |
| Success | ![Success](./screenshots/streamlit_app/05_success_screen.png) | Success screen |

---

## 📁 Project Structure

\`\`\`
linkedin_msg/
│
├── app.py                          # Streamlit web application
├── .env                            # Environment variables
├── README.md                       # This file
│
├── src/
│   └── linkedin_msg/
│       ├── main.py                 # Main entry point
│       ├── crew.py                 # CrewAI configuration
│       ├── tools/
│       │   └── linkedin_automation_tool.py
│       └── config/
│           ├── agents.yaml
│           └── tasks.yaml
│
├── screenshots/                    # Documentation screenshots
│   ├── setup/
│   ├── automation_process/
│   └── streamlit_app/
│
└── docs/                          # Additional docs
\`\`\`

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "No search results found"

**Solutions**:
- Verify name spelling
- Search on LinkedIn manually first
- Use more specific name (e.g., "John Smith Microsoft")

#### 2. "Connect button not available"

**Solutions**:
- May already be connected
- Check for pending request
- Profile may have restrictions

#### 3. "Login failed"

**Solutions**:
- Verify credentials in `.env`
- Check if 2FA is enabled (not supported)
- Ensure not logged in elsewhere

#### 4. "ChromeDriver error"

**Solutions**:
\`\`\`bash
pip install --upgrade webdriver-manager
\`\`\`

---

## 💡 Best Practices

### Targeting the Right Person

✅ **DO:**
- Use full names: "John Smith"
- Add context: "John Smith Microsoft"
- Verify person exists first
- Check FIRST result is correct

❌ **DON'T:**
- Use partial names
- Assume automation finds right person

### Writing Connection Notes

✅ **DO:**
- Be specific
- Mention common interests
- Keep under 300 characters
- Be professional

❌ **DON'T:**
- Use generic messages
- Make it too long
- Include promotional content

### Usage Frequency

⚠️ **Recommended**:
- 5-10 requests per day
- Take breaks between batches
- Respect LinkedIn limits

---

## 🔒 Security

### Credential Safety

1. **Never commit `.env` file**
   \`\`\`bash
   echo ".env" >> .gitignore
   \`\`\`

2. **Rotate credentials regularly**

3. **Use environment-specific files**

### LinkedIn Terms of Service

⚠️ **Disclaimer**: Use responsibly and in accordance with LinkedIn's Terms of Service. The authors are not responsible for account restrictions.

---

## 📞 Support

For issues:
1. Check Troubleshooting section
2. Review existing issues
3. Create new issue with details

---

<div align="center">

**Made with ❤️ using CrewAI & Streamlit**

LinkedIn Automation Tool v1.0

</div>
