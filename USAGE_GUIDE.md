# LinkedIn Automation - Usage Guide

## Credentials Configuration

Your LinkedIn credentials are stored in the `.env` file and automatically loaded by the system.

**Current Configuration:**
- Email: `kanup3535@gmail.com`
- Password: Loaded from `.env` file

## How It Works

The system uses three main tools that work together:

1. **LinkedInLoginTool** - Logs into LinkedIn using credentials from `.env`
   - Automatically loads `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` from environment
   - Uses Selenium to navigate to LinkedIn and perform login
   - Returns success confirmation

2. **LinkedInSearchTool** - Searches for people on LinkedIn
   - Takes a person's name as input
   - Searches LinkedIn and navigates to the first matching profile
   - Returns profile details and URL

3. **LinkedInMessageTool** - Sends messages to LinkedIn profiles
   - Checks if messaging is available on the current profile
   - Sends a message if the person is a connection
   - Reports if messaging is not available

## Running the Automation

### Basic Usage

To run the automation with a specific person:

```bash
python src/linkedin_msg/main.py
```

The default configuration searches for "John Doe". To change the person:

Edit `src/linkedin_msg/main.py` and modify the `inputs` dictionary:

```python
inputs = {
    'person_name': 'Your Target Name'
}
```

### The Process Flow

1. **Login**: System reads credentials from `.env` and logs into LinkedIn
2. **Search**: Searches for the specified person name
3. **Message**: Attempts to send a message (only works if you're connected)

## Verification

To verify your credentials are loaded correctly:

```bash
python verify_credentials.py
```

This will show:
- ✓ If credentials are properly loaded
- Masked password for security
- Email address

## Important Notes

- **Security**: Never commit your `.env` file to version control
- **Rate Limiting**: LinkedIn may rate-limit or block automated access
- **Connections**: You can only message people you're connected with
- **Browser**: The automation will open a Chrome browser window
- **Timing**: The script includes delays to avoid detection

## File Structure

```
.env                              # Your credentials (not in git)
src/linkedin_msg/
  ├── main.py                     # Entry point
  ├── crew.py                     # Crew configuration
  ├── tools/
  │   └── linkedin_automation_tool.py  # Login, Search, Message tools
  └── config/
      ├── agents.yaml             # Agent configuration
      └── tasks.yaml              # Task descriptions
```

## Troubleshooting

If login fails:
1. Check credentials in `.env` are correct
2. LinkedIn may require 2FA or CAPTCHA verification
3. Try logging in manually first to verify account isn't locked
4. Check Chrome browser is installed

If search fails:
1. Ensure you're logged in first
2. Try a more specific name
3. Check the person exists on LinkedIn

If messaging fails:
1. Verify you're connected with the person
2. Some profiles have messaging restrictions
3. Check if you need to send a connection request first
