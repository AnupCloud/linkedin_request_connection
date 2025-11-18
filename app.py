#!/usr/bin/env python
"""
LinkedIn Automation Streamlit Web Application
This provides a user-friendly web interface for the LinkedIn automation tool.
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv, set_key
import subprocess
import threading

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set page config
st.set_page_config(
    page_title="LinkedIn Automation Tool",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #0077B5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #0077B5;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem 2rem;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔗 LinkedIn Automation Tool</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg", width=200)
    st.markdown("### About")
    st.info("""
    This tool automates LinkedIn connection requests with personalized notes.

    **Features:**
    - 🔐 Secure credential management
    - 🔍 Smart profile search
    - 📝 Personalized connection notes
    - 🤖 AI-powered automation
    """)

    st.markdown("### How It Works")
    st.markdown("""
    1. **Login**: Uses your LinkedIn credentials
    2. **Search**: Finds the person by name
    3. **Select**: Chooses FIRST result
    4. **Connect**: Sends connection request with note
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## ⚙️ Configuration")

    # Create tabs
    tab1, tab2 = st.tabs(["🎯 Quick Start", "🔐 Credentials"])

    with tab1:
        st.markdown("### LinkedIn Connection Request")

        # Load current values
        current_person = os.getenv('PERSON_NAME', '')
        current_note = os.getenv('CONNECTION_NOTE', '')

        # Person name input
        person_name = st.text_input(
            "👤 Person Name",
            value=current_person,
            placeholder="e.g., John Smith",
            help="Enter the full name of the person you want to connect with"
        )

        # Connection note input
        connection_note = st.text_area(
            "📝 Connection Note",
            value=current_note,
            height=150,
            placeholder="Hi! I came across your profile and would love to connect...",
            help="Write a personalized message explaining why you want to connect"
        )

        # Character counter
        note_length = len(connection_note)
        max_length = 300
        if note_length > max_length:
            st.warning(f"⚠️ Note is {note_length} characters. LinkedIn recommends keeping it under {max_length}.")
        else:
            st.caption(f"📊 {note_length} / {max_length} characters")

        # Save configuration button
        col_save, col_run = st.columns(2)

        with col_save:
            if st.button("💾 Save Configuration", use_container_width=True):
                if person_name and connection_note:
                    # Update .env file
                    env_path = os.path.join(os.path.dirname(__file__), '.env')
                    set_key(env_path, 'PERSON_NAME', person_name)
                    set_key(env_path, 'CONNECTION_NOTE', connection_note)
                    st.success("✅ Configuration saved!")
                else:
                    st.error("❌ Please fill in both fields")

        with col_run:
            if st.button("🚀 Run Automation", use_container_width=True, type="primary"):
                if person_name and connection_note:
                    # Save to .env file
                    env_path = os.path.join(os.path.dirname(__file__), '.env')
                    set_key(env_path, 'PERSON_NAME', person_name)
                    set_key(env_path, 'CONNECTION_NOTE', connection_note)

                    # Show what we're running with
                    st.info(f"🎯 **Searching for:** {person_name}")

                    with st.spinner("🔄 Running automation... This may take 30-60 seconds"):
                        try:
                            # Prepare environment variables - create a fresh env dict
                            # This ensures the subprocess uses the updated values
                            env = os.environ.copy()
                            env['PERSON_NAME'] = person_name
                            env['CONNECTION_NOTE'] = connection_note

                            # Run the automation with updated environment
                            result = subprocess.run(
                                [sys.executable, "src/linkedin_msg/main.py"],
                                capture_output=True,
                                text=True,
                                timeout=300,
                                env=env  # Pass the updated environment
                            )

                            if "CONNECTION REQUEST SENT SUCCESSFULLY" in result.stdout:
                                st.balloons()
                                st.markdown(f"""
                                <div class="success-box">
                                    <h3>✅ Success!</h3>
                                    <p>Connection request sent to <strong>{person_name}</strong></p>
                                    <p>Your personalized note has been delivered!</p>
                                </div>
                                """, unsafe_allow_html=True)

                                # Show execution details in expander
                                with st.expander("📋 Execution Details"):
                                    st.code(result.stdout, language="text")
                            else:
                                st.error("❌ Automation completed but connection request status unclear")
                                with st.expander("📋 Full Output"):
                                    st.code(result.stdout, language="text")
                                if result.stderr:
                                    st.code(result.stderr, language="text")

                        except subprocess.TimeoutExpired:
                            st.error("⏱️ Automation timed out. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("❌ Please fill in both Person Name and Connection Note")

    with tab2:
        st.markdown("### LinkedIn Credentials")
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Security Notice:</strong> Your credentials are stored in the .env file and never shared.
        </div>
        """, unsafe_allow_html=True)

        # Load credentials
        current_email = os.getenv('LINKEDIN_EMAIL', '')
        current_password = os.getenv('LINKEDIN_PASSWORD', '')

        email = st.text_input(
            "📧 LinkedIn Email",
            value=current_email,
            type="default",
            help="Your LinkedIn login email"
        )

        password = st.text_input(
            "🔒 LinkedIn Password",
            value=current_password if current_password else "",
            type="password",
            help="Your LinkedIn password (stored securely in .env file)"
        )

        if st.button("💾 Save Credentials", use_container_width=True):
            if email and password:
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                set_key(env_path, 'LINKEDIN_EMAIL', email)
                set_key(env_path, 'LINKEDIN_PASSWORD', password)
                st.success("✅ Credentials saved securely!")
            else:
                st.error("❌ Please provide both email and password")

with col2:
    st.markdown("## 📊 Status")

    # Check configuration status
    email_status = "✅" if os.getenv('LINKEDIN_EMAIL') else "❌"
    password_status = "✅" if os.getenv('LINKEDIN_PASSWORD') else "❌"
    person_status = "✅" if os.getenv('PERSON_NAME') else "❌"
    note_status = "✅" if os.getenv('CONNECTION_NOTE') else "❌"

    st.markdown(f"""
    ### Configuration Status

    - {email_status} LinkedIn Email
    - {password_status} LinkedIn Password
    - {person_status} Person Name
    - {note_status} Connection Note
    """)

    # API Keys status
    st.markdown("### API Keys")
    anthropic_status = "✅" if os.getenv('ANTHROPIC_API_KEY') else "❌"
    st.markdown(f"- {anthropic_status} Anthropic API Key")

    # Quick tips
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - **Be Specific**: Use full names for better search results
    - **Personalize**: Mention common interests or connections
    - **Be Professional**: Keep your tone friendly yet professional
    - **First Result**: The tool selects the FIRST person in search results
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Made with ❤️ using CrewAI & Streamlit | LinkedIn Automation Tool v1.0</p>
    <p style="font-size: 0.8rem;">⚠️ Use responsibly and in accordance with LinkedIn's Terms of Service</p>
</div>
""", unsafe_allow_html=True)
