# VS Code Setup Guide - AI Student Group Matcher

This guide will help you run the AI Student Group Matcher application in Visual Studio Code.

## Prerequisites

Before starting, make sure you have:
- **Visual Studio Code** installed ([Download here](https://code.visualstudio.com/))
- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **Git** installed (optional, for cloning)

## Step-by-Step Setup

### Step 1: Open Project in VS Code

**Option A: Open the Folder**
1. Open VS Code
2. Click `File` → `Open Folder`
3. Navigate to the `New-start` folder
4. Click `Select Folder`

**Option B: Using Terminal**
```bash
cd /path/to/New-start
code .
```

### Step 2: Install Python Extension

1. Click on the **Extensions** icon in the sidebar (or press `Ctrl+Shift+X`)
2. Search for "Python"
3. Install the official **Python** extension by Microsoft
4. Also install **Pylance** (usually comes with Python extension)

### Step 3: Create a Virtual Environment

**Why?** A virtual environment keeps your project dependencies isolated.

**In VS Code Terminal:**

1. Open the integrated terminal:
   - Press `` Ctrl+` `` (backtick)
   - Or go to `View` → `Terminal`

2. Create virtual environment:

**On Windows:**
```bash
python -m venv venv
```

**On Mac/Linux:**
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 4: Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask
- Flask-CORS
- Flask-SocketIO
- scikit-learn
- numpy
- pandas

**Wait for installation to complete** (may take 1-2 minutes)

### Step 5: Select Python Interpreter in VS Code

1. Press `Ctrl+Shift+P` (Command+Shift+P on Mac)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from your `venv` folder:
   - Should show something like `./venv/bin/python` or `.\venv\Scripts\python.exe`

### Step 6: Run the Application

**Method 1: Using Terminal (Recommended)**

In the VS Code terminal (with venv activated):

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
```

**Method 2: Using VS Code Debug**

1. Click on the **Run and Debug** icon in the sidebar (or press `Ctrl+Shift+D`)
2. Click "create a launch.json file"
3. Select "Python"
4. Select "Flask"
5. Press `F5` to start debugging

**Method 3: Using Play Button**

1. Open `app.py` in the editor
2. You'll see a **Play button** (▶) in the top-right corner
3. Click it to run the file

### Step 7: Open in Browser

1. Once the server is running, you'll see:
   ```
   * Running on http://127.0.0.1:5000
   ```

2. **Option A:** Hold `Ctrl` (or `Cmd` on Mac) and click the link in terminal

3. **Option B:** Open your browser and go to:
   ```
   http://localhost:5000
   ```

### Step 8: Use the Application

You should now see the AI Student Group Matcher interface!

**Try these features:**
1. Select a semester from the dropdown (3, 5, or 7)
2. Select a topic
3. Click on student cards to select them (4-5 students)
4. Click "Create Group" or try "AI Suggest Groups"
5. Check the "Groups" tab to see created groups
6. Try the "Group Chat" feature

## VS Code Features to Use

### 1. Split View for Editing

- Right-click on a file tab → `Split Right` or `Split Down`
- Edit HTML, CSS, and JS side-by-side

### 2. Live Server for Frontend (Optional)

If you want to test only the frontend:
1. Install "Live Server" extension
2. Right-click `static/index.html`
3. Select "Open with Live Server"

### 3. Python Debugging

Set breakpoints in `app.py`:
1. Click left of line number to add red dot (breakpoint)
2. Run in debug mode (`F5`)
3. Code will pause at breakpoint
4. Inspect variables in the left panel

### 4. Terminal Management

Open multiple terminals:
- Click `+` icon in terminal panel
- One for running the server
- One for git commands
- One for installing packages

### 5. Git Integration

VS Code has built-in Git:
- **Source Control** icon in sidebar (or `Ctrl+Shift+G`)
- See changes, commit, push/pull
- View file history

## Useful VS Code Shortcuts

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Open terminal | `` Ctrl+` `` | `` Cmd+` `` |
| Command palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Quick file open | `Ctrl+P` | `Cmd+P` |
| Find in files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Format document | `Shift+Alt+F` | `Shift+Option+F` |
| Multi-cursor | `Alt+Click` | `Option+Click` |
| Toggle sidebar | `Ctrl+B` | `Cmd+B` |

## Recommended VS Code Extensions

Install these for better development:

1. **Python** - Microsoft (Essential)
2. **Pylance** - Microsoft (Essential)
3. **SQLite Viewer** - alexcvzz (View database)
4. **Live Server** - Ritwick Dey (Frontend testing)
5. **Prettier** - Prettier (Code formatting)
6. **Auto Rename Tag** - Jun Han (HTML editing)
7. **Path Intellisense** - Christian Kohler (File paths)
8. **GitLens** - GitKraken (Git supercharged)

## Project File Structure in VS Code

```
New-start/
├── 📄 app.py                    # Main Flask server - Start here!
├── 📄 database.py               # Database operations
├── 📄 ai_matcher.py            # AI matching logic
├── 📄 schema.sql               # Database schema
├── 📄 students_data.csv        # Your student data
├── 📄 requirements.txt         # Python packages
├── 📄 README.md                # Documentation
├── 📄 VSCODE_SETUP.md          # This file
├── 📁 venv/                    # Virtual environment (created by you)
├── 📁 static/                  # Frontend files
│   ├── index.html             # Main page
│   ├── styles.css             # Styling
│   └── app.js                 # Frontend JavaScript
└── 📄 student_groups.db        # Database (auto-created)
```

## Common Issues & Solutions

### Issue 1: "Python not found"
**Solution:** Make sure Python is installed and added to PATH
```bash
python --version
```

### Issue 2: "pip not found"
**Solution:**
```bash
python -m pip --version
```

### Issue 3: Virtual environment not activating
**Solution on Windows:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
socketio.run(app, debug=True, port=5001)
```

### Issue 5: Module not found error
**Solution:** Make sure venv is activated and reinstall:
```bash
pip install -r requirements.txt
```

### Issue 6: Database error
**Solution:** Delete the database and restart:
```bash
rm student_groups.db  # Mac/Linux
del student_groups.db  # Windows
python app.py
```

## Stopping the Server

To stop the Flask server:
- Press `Ctrl+C` in the terminal
- Or click the trash icon in the terminal panel

## Modifying the Code

### Edit Student Data
1. Open `students_data.csv`
2. Edit in VS Code or Excel
3. Delete `student_groups.db`
4. Restart server (data will reload)

### Change UI Colors
1. Open `static/styles.css`
2. Find gradient colors (line 7-8):
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
3. Change to your preferred colors
4. Save and refresh browser

### Add New Topics
1. Open `schema.sql`
2. Add INSERT statement:
```sql
INSERT INTO topics (title, description, semester, category) VALUES
('Your New Topic', 'Description here', 3, 'Category');
```
3. Delete database and restart

### Modify AI Algorithm
1. Open `ai_matcher.py`
2. Edit the `evaluate_group_compatibility` method
3. Adjust weights and scoring

## Testing the Application

### Test Checklist:
- [ ] Server starts without errors
- [ ] Can view students by semester
- [ ] Can select students (cards turn purple)
- [ ] Can create manual group (4-5 students)
- [ ] AI suggestions work
- [ ] Can view created groups
- [ ] Chat functionality works
- [ ] Topics display correctly

## Next Steps

1. **Customize** the UI colors and branding
2. **Add student skills** to see better AI matching
3. **Create some test groups** to verify functionality
4. **Test the chat feature** with multiple browser tabs
5. **Add more topics** specific to your courses

## Getting Help

- Check `README.md` for detailed documentation
- Review Python errors in the terminal
- Use VS Code's built-in problem panel (`Ctrl+Shift+M`)
- Check browser console for frontend errors (F12)

## Happy Coding!

Your AI Student Group Matcher is now ready to use in VS Code. Enjoy building collaborative student groups!

---

**Quick Start Command Summary:**

```bash
# 1. Open VS Code in project folder
code .

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser
http://localhost:5000
```
