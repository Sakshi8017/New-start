# Quick Start Guide - 5 Minutes to Running

## Super Quick Setup (Copy & Paste)

### 1. Open Terminal in VS Code
Press `` Ctrl+` `` (backtick key, usually below ESC)

### 2. Copy and paste these commands one by one:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3. Open Browser
Go to: **http://localhost:5000**

## That's it!

You should now see the AI Student Group Matcher running.

---

## First Time Using It?

### Try This Flow:

1. **Select Semester 3** from dropdown
2. **Select a Topic** (e.g., "Web Development Project")
3. **Click "AI Suggest Groups"**
4. **Review the 3 suggested groups** with compatibility scores
5. **Click "Create This Group"** on one you like
6. **Go to "Groups" tab** to see your created group
7. **Go to "Group Chat" tab** and select the group to start chatting!

### Or Create Manually:

1. **Select Semester 3**
2. **Select a Topic**
3. **Click 5 student cards** (they turn purple when selected)
4. **Click "Create Group"**
5. Done! Check the "Groups" tab

---

## Visual Guide

```
VS Code Layout:
┌─────────────────────────────────────────────┐
│  File  Edit  View  Terminal  Help           │
├──────┬──────────────────────────────────────┤
│ 📁   │  app.py (your main file)             │
│ app  │                                       │
│ data │  Click ▶️ (Play button) to run       │
│ stat │                                       │
│ venv │  or use Terminal below ↓             │
│      │                                       │
│      │                                       │
├──────┴──────────────────────────────────────┤
│ TERMINAL (Ctrl+`)                            │
│ (venv) $ python app.py                       │
│ * Running on http://127.0.0.1:5000          │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Troubleshooting

### Problem: "python not found"
**Fix:** Try `python3` instead of `python`

### Problem: Permission denied (Windows)
**Fix:** Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Port 5000 in use
**Fix:** Change port in app.py to 5001 or 8000

### Problem: Packages not installing
**Fix:** Make sure venv is activated (you should see `(venv)` in terminal)

---

## Stop the Server
Press `Ctrl+C` in the terminal

## Restart the Server
```bash
python app.py
```

---

## What Files Do What?

| File | Purpose | When to Edit |
|------|---------|-------------|
| `app.py` | Main server | Change features, API |
| `database.py` | Database code | Change data operations |
| `ai_matcher.py` | AI algorithm | Adjust matching logic |
| `static/index.html` | Web page | Change layout |
| `static/styles.css` | Styling | Change colors, fonts |
| `static/app.js` | Frontend logic | Change UI behavior |
| `students_data.csv` | Your students | Update student list |
| `schema.sql` | Database structure | Add new topics |

---

## Need More Help?

Read the full guide: `VSCODE_SETUP.md`
Read the docs: `README.md`

**Enjoy your AI Student Group Matcher! 🚀**
