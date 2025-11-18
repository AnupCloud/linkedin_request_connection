# Quick Start - Dynamic LinkedIn Automation

## ✅ Your System is Already Dynamic!

The name is **NOT hardcoded**. It uses whatever you put in `main.py`.

---

## 📝 Current Setup (main.py line 25-28)

```python
inputs = {
    'person_name': 'Aditya Kinare',  # ← Change this to ANY name!
    'connection_note': 'Hi Aditya! I came across...'  # ← Your custom message
}
```

---

## 🚀 How It Works

### What Happens When You Run:

```bash
python src/linkedin_msg/main.py
```

**Step 1: Login**
- Uses credentials from `.env`
- Logs into LinkedIn

**Step 2: Search**
- Searches for EXACT name: `'Aditya Kinare'`
- URL: `linkedin.com/search/results/people/?keywords=Aditya%20Kinare`

**Step 3: Select FIRST Result**
- Clicks the **FIRST person** in search results
- You'll see in logs:
  ```
  [INFO] ✓ SELECTED FIRST RESULT: [Name of first person]
  [INFO] ✓ Profile URL: [their profile]
  ```

**Step 4: Send Connection Request**
- Clicks "Connect" button
- Adds your personalized note
- Sends the request

---

## 🔄 To Use Different Names

### Just Edit Line 26 in main.py:

**Example 1: Search for Satya Nadella**
```python
inputs = {
    'person_name': 'Satya Nadella',  # ← Changed!
    'connection_note': 'Hi Satya! Your custom message here'
}
```

**Example 2: Search for Elon Musk**
```python
inputs = {
    'person_name': 'Elon Musk',  # ← Changed!
    'connection_note': 'Hi Elon! Your custom message here'
}
```

**Example 3: Back to Aditya Kinare**
```python
inputs = {
    'person_name': 'Aditya Kinare',  # ← Changed!
    'connection_note': 'Hi Aditya! Your custom message here'
}
```

---

## 📊 What You'll See

When you run the script, you'll see detailed logs showing EXACTLY who was selected:

```
[DEBUG] Searching for: Aditya Kinare
[INFO] ✓ Found search results for 'Aditya Kinare'
[INFO] → Selecting FIRST person from search results...
[INFO] ✓ FIRST result profile URL: https://www.linkedin.com/in/profile-url
[INFO] → Clicking on this profile...
[INFO] ══════════════════════════════════════════
[INFO] ✓ SELECTED FIRST RESULT: John Doe
[INFO] ✓ Profile URL: https://www.linkedin.com/in/johndoe
[INFO] ══════════════════════════════════════════

Tool Output:
Found FIRST profile in search results: John Doe
This is the person who will receive your connection request.
```

---

## 🎯 The System Behavior

| What You Type | What Happens |
|---------------|--------------|
| `'Aditya Kinare'` | Searches "Aditya Kinare" → Selects FIRST result → Sends request |
| `'Satya Nadella'` | Searches "Satya Nadella" → Selects FIRST result → Sends request |
| `'ANY NAME'` | Searches "ANY NAME" → Selects FIRST result → Sends request |

**Always selects the FIRST person that appears in LinkedIn search results.**

---

## ⚠️ Important Notes

### 1. It's NOT Random
The system searches for the EXACT name you provide and always selects the FIRST result. This is consistent and predictable.

### 2. To Get the Right Person
Make your search more specific:

**Generic (might get wrong person):**
```python
'person_name': 'Aditya Kinare'
```

**Specific (more likely correct person):**
```python
'person_name': 'Aditya Kinare Microsoft'
# or
'person_name': 'Aditya Kinare Mumbai'
# or
'person_name': 'Aditya Kinare Software Engineer'
```

### 3. Verify First
Before using automation:
1. Go to LinkedIn manually
2. Search for "Aditya Kinare"
3. Is the FIRST result the person you want?
4. If yes → use automation
5. If no → make search more specific

---

## ✅ Test Right Now

1. **Open**: `src/linkedin_msg/main.py`
2. **Edit line 26**: Change to any name you want
3. **Run**: `python src/linkedin_msg/main.py`
4. **Watch the logs**: See exactly who was selected

---

## 🔍 Example Test

Let's test with Satya Nadella (we know he exists):

1. Edit `main.py`:
```python
inputs = {
    'person_name': 'Satya Nadella',
    'connection_note': 'Test message'
}
```

2. Run:
```bash
python src/linkedin_msg/main.py
```

3. You'll see:
```
[INFO] ✓ SELECTED FIRST RESULT: Satya Nadella
[INFO] ✓ Profile URL: https://www.linkedin.com/in/satyanadella
```

4. This proves the system works!

5. Now change back to "Aditya Kinare" and run again.

---

## 💡 Pro Tip

If "Aditya Kinare" search returns no results or wrong person:

1. Search LinkedIn manually for "Aditya Kinare"
2. Look at the FIRST result
3. Is that the person you want?
   - ✅ Yes → That's who will get the request
   - ❌ No → Add more details to search (company, location, etc.)

---

**Bottom Line**:
- ✅ System is DYNAMIC (uses whatever name you provide)
- ✅ Always selects FIRST search result
- ✅ Name is controlled by YOU in `main.py` line 26
- ✅ Logs show EXACTLY who was selected
- ✅ You can change the name anytime by editing `main.py`

**Just edit line 26 and run!** 🚀
