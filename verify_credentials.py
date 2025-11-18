#!/usr/bin/env python
"""
Verify that LinkedIn credentials are loaded correctly from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def verify_credentials():
    """Check if LinkedIn credentials are properly loaded"""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    print("=" * 50)
    print("LinkedIn Credentials Verification")
    print("=" * 50)

    if email:
        print(f"✓ LINKEDIN_EMAIL loaded: {email}")
    else:
        print("✗ LINKEDIN_EMAIL not found!")

    if password:
        # Mask password for security
        masked_password = password[:2] + "*" * (len(password) - 4) + password[-2:]
        print(f"✓ LINKEDIN_PASSWORD loaded: {masked_password}")
    else:
        print("✗ LINKEDIN_PASSWORD not found!")

    print("=" * 50)

    if email and password:
        print("\n✓ All credentials are properly loaded!")
        print("You can now run the LinkedIn automation with:")
        print("  python src/linkedin_msg/main.py")
        return True
    else:
        print("\n✗ Credentials are missing! Please check your .env file.")
        return False

if __name__ == "__main__":
    verify_credentials()
