# LinkedIn Connection Request Automation - Complete Guide

## 🎉 New Feature Added: Connection Requests with Notes!

Your LinkedIn automation now supports:
1. ✅ **Login** with credentials from `.env`
2. ✅ **Search** for any person by name
3. ✅ **Send Connection Requests** with personalized notes
4. ✅ **Send Messages** (if already connected)

---

## How the Workflow Works

### Workflow Steps:

1. **Login Task**
   - Automatically logs in using `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` from `.env`

2. **Search Task**
   - Searches for the person by name
   - Navigates to their profile

3. **Connection Request Task** ⭐ NEW!
   - Checks if "Connect" button is available
   - If available: Sends connection request with your custom note
   - If already connected: Skips and reports existing connection

4. **Message Task**
   - If already connected: Sends a message
   - If not connected: Reports messaging not available

---

## How to Use

### Step 1: Edit `main.py`

Open `src/linkedin_msg/main.py` and update the `inputs`:

```python
inputs = {
    'person_name': 'First Last',  # Replace with actual name
    'connection_note': 'Your personalized connection request message here'
}
```

### Example 1: Connect with a Recruiter

```python
inputs = {
    'person_name': 'Sarah Johnson',
    'connection_note': 'Hi Sarah! I saw your post about AI opportunities and would love to connect. I have 5 years of experience in machine learning and am very interested in learning more about your company\'s work in this space.'
}
```

### Example 2: Connect with Someone from a Conference

```python
inputs = {
    'person_name': 'Michael Chen',
    'connection_note': 'Hi Michael! It was great meeting you at the Tech Summit last week. I\'d love to stay in touch and continue our conversation about cloud architecture. Looking forward to connecting!'
}
```

### Example 3: Network Expansion

```python
inputs = {
    'person_name': 'Emily Rodriguez',
    'connection_note': 'Hi Emily! I came across your profile and was impressed by your work in data science. I\'m also passionate about this field and would love to expand my professional network. Hope to connect!'
}
```

---

## Running the Automation

### Basic Command:

```bash
python src/linkedin_msg/main.py
```

### What Happens:

1. **Chrome browser opens** (you'll see the automation in action)
2. **Logs into LinkedIn** with your credentials
3. **Searches** for the person
4. **Sends connection request** with your note
5. **Browser closes** automatically

---

## Connection Request Tips

### ✅ Good Connection Notes:
- Be personalized and specific
- Mention why you want to connect
- Keep it professional and friendly
- 2-3 sentences is ideal
- Reference something specific (mutual interest, company, post, event)

### ❌ Avoid:
- Generic messages ("I'd like to add you to my network")
- Too long (LinkedIn has a 300-character limit)
- Sales pitches in initial connection
- Typos or poor grammar

---

## Example Connection Note Templates

### Template 1: Fellow Professional
```
Hi [Name]! I came across your profile and was impressed by your experience in [field]. I'm also working in [related area] and would love to expand my professional network with like-minded professionals. Looking forward to connecting!
```

### Template 2: Recruiter/Hiring Manager
```
Hi [Name]! I noticed you're hiring for [position] at [company]. I have [X years] of experience in [skill] and am very interested in opportunities at [company]. I'd love to connect and learn more about your team!
```

### Template 3: Industry Leader
```
Hi [Name]! I've been following your work on [topic/company] and find it inspiring. I'm passionate about [related field] and would value the opportunity to connect and learn from your insights.
```

### Template 4: Event Connection
```
Hi [Name]! Great meeting you at [event name]! I enjoyed our discussion about [topic]. Would love to stay connected and continue the conversation.
```

---

## Testing with a Real Profile

### Step-by-Step Test:

1. **Find a real LinkedIn profile** to test with
2. **Copy their name exactly** as it appears on LinkedIn
3. **Edit `main.py`**:
   ```python
   inputs = {
       'person_name': 'Exact Name From LinkedIn',
       'connection_note': 'Your personalized note here'
   }
   ```
4. **Run the automation**:
   ```bash
   python src/linkedin_msg/main.py
   ```
5. **Watch the browser** - you'll see it:
   - Login
   - Search for the person
   - Navigate to their profile
   - Click "Connect"
   - Add your note
   - Send the request

---

## Troubleshooting

### Issue: "No search results found"

**Possible causes:**
- Name spelling is incorrect
- Person doesn't have a LinkedIn profile
- Profile has strict privacy settings
- Name is very common (try adding company or title)

**Solutions:**
- Verify exact name spelling on LinkedIn
- Try adding middle initial
- Use their LinkedIn profile URL instead
- Search with company name: `'person_name': 'John Smith Microsoft'`

### Issue: "Connect button not available"

**Possible causes:**
- Already connected
- Pending connection request
- Profile doesn't allow connection requests

**Solution:**
- Check your LinkedIn connections manually
- May need to wait if there's a pending request

### Issue: "Connection request without note"

**Possible causes:**
- LinkedIn sometimes doesn't show "Add a note" option
- Depends on account type and connection level

**Note:**
The system will still attempt to send the request, but the note may not be included. This is a LinkedIn limitation.

---

## Files Modified

The following files were updated to support connection requests:

1. **`src/linkedin_msg/tools/linkedin_automation_tool.py`**
   - Added `LinkedInConnectTool` class
   - Added `LinkedInConnectInput` schema

2. **`src/linkedin_msg/crew.py`**
   - Added `LinkedInConnectTool` to agent tools
   - Added `linkedin_connect_task` method

3. **`src/linkedin_msg/config/tasks.yaml`**
   - Added `linkedin_connect_task` configuration

4. **`src/linkedin_msg/main.py`**
   - Added `connection_note` to inputs

---

## Important Notes

⚠️ **LinkedIn Rate Limits:**
- Don't send too many connection requests in a short time
- LinkedIn may flag your account for suspicious activity
- Use responsibly and space out your requests

⚠️ **Weekly Connection Limit:**
- LinkedIn limits connection requests (typically 100-200 per week)
- Exceeding this may result in a temporary restriction

⚠️ **Best Practices:**
- Only connect with people you have a genuine reason to connect with
- Personalize each note
- Don't use automation for spam or unsolicited marketing
- Follow LinkedIn's terms of service

---

## Success Indicators

### ✅ Successful Connection Request:
```
Tool Output:
Successfully sent connection request with note: 'Your message here'
```

### ✅ Already Connected:
```
Tool Output:
Connect button not available. The person may already be a connection.
```

### ⚠️ Profile Not Found:
```
Tool Output:
No search results found for '[Name]'
```

---

## Next Steps

1. **Test with a real profile** you want to connect with
2. **Personalize your connection note** for that person
3. **Run the automation** and watch it work
4. **Check your LinkedIn** to verify the connection request was sent

---

## Support

If you encounter issues:
1. Check that the person's name is spelled correctly
2. Verify the person has a LinkedIn profile
3. Make sure your `.env` credentials are correct
4. Check the browser window for any LinkedIn security challenges (CAPTCHA, 2FA)

Happy networking! 🎉
