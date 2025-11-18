#!/usr/bin/env python
"""
Quick test of the LinkedIn Login Tool to verify credentials are loaded correctly
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.linkedin_msg.tools.linkedin_automation_tool import LinkedInLoginTool

def test_login():
    """Test the LinkedIn login tool"""
    print("=" * 60)
    print("Testing LinkedIn Login Tool")
    print("=" * 60)

    # Create tool instance
    login_tool = LinkedInLoginTool()

    print("\n1. Tool created successfully")
    print(f"   Name: {login_tool.name}")
    print(f"   Description: {login_tool.description}")

    print("\n2. Attempting login with credentials from .env file...")
    print("   (Browser window will open - this is normal)")

    # Run the tool with empty parameters (it will load from .env)
    result = login_tool._run(email="", password="")

    print("\n3. Login Result:")
    print(f"   {result}")

    print("\n" + "=" * 60)

    if "Successfully logged into LinkedIn" in result:
        print("✓ LOGIN TEST PASSED!")
        return True
    elif "requires additional verification" in result:
        print("⚠ LOGIN REQUIRES MANUAL VERIFICATION")
        print("  This is normal - LinkedIn may show CAPTCHA or 2FA")
        print("  Please check the browser window and complete verification")
        return False
    else:
        print("✗ LOGIN TEST FAILED!")
        return False

if __name__ == "__main__":
    test_login()
