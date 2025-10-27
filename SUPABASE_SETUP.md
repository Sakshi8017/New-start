# Supabase Setup Guide - AI Student Group Matcher

This guide will help you set up the application with Supabase (cloud PostgreSQL database).

## Why Supabase?

- ✅ **Free tier** with 500MB database
- ✅ **Cloud-hosted** - no local database needed
- ✅ **Real-time** capabilities
- ✅ **Easy to deploy** and share
- ✅ **PostgreSQL** - powerful and scalable

---

## Step 1: Create Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or email
4. Verify your email

---

## Step 2: Create a New Project

1. Click **"New Project"**
2. Choose your organization (or create one)
3. Fill in project details:
   - **Name**: `student-group-matcher` (or any name)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to you (e.g., `US West`)
   - **Pricing Plan**: Select **Free**
4. Click **"Create new project"**
5. Wait 2-3 minutes for setup to complete

---

## Step 3: Get Your API Keys

1. In your Supabase project dashboard
2. Click on **⚙️ Settings** (bottom left)
3. Click on **API**
4. You'll see two important values:

   **Project URL** (looks like):
   ```
   https://abcdefghijklmn.supabase.co
   ```

   **anon/public key** (looks like):
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS...
   ```

5. **Keep this tab open** - you'll need these values!

---

## Step 4: Run the SQL Schema

1. In Supabase dashboard, click on **SQL Editor** (left sidebar)
2. Click **"New Query"**
3. Open the file `supabase_schema.sql` from your project
4. **Copy ALL the SQL code** from that file
5. **Paste it** into the Supabase SQL editor
6. Click **"Run"** (or press Ctrl+Enter)
7. You should see: ✅ **"Success. No rows returned"**

This creates all the tables (students, groups, topics, messages, etc.)

---

## Step 5: Configure Your Local Project

### 5.1 Create `.env` file

In your project folder, create a file named `.env` (no extension):

**Mac/Linux:**
```bash
touch .env
```

**Windows:**
- Right-click in VS Code explorer → New File → name it `.env`

### 5.2 Add Your Credentials

Open `.env` and paste:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Replace** with YOUR actual values from Step 3!

**Important:**
- Use the **Project URL** (not the Postgres connection string)
- Use the **anon/public key** (not the service_role key)

### 5.3 Save the file

Make sure `.env` is in the root of your project folder (same level as `app_supabase.py`)

---

## Step 6: Install Dependencies

Open terminal in VS Code (`` Ctrl+` ``) and run:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install new packages
pip install -r requirements.txt
```

---

## Step 7: Load Student Data

Now load your 415 students into Supabase:

### Option A: Using the API endpoint

1. Start the server:
   ```bash
   python app_supabase.py
   ```

2. Open another terminal and run:
   ```bash
   curl -X POST http://localhost:5000/api/load-students
   ```

### Option B: Using Python directly

```bash
python -c "import database_supabase as db; db.load_students_from_csv()"
```

You should see:
```
Inserted batch 1: 100 students
Inserted batch 2: 100 students
...
Successfully loaded 415 students!
```

---

## Step 8: Run the Application

```bash
python app_supabase.py
```

You should see:
```
Testing Supabase connection...
✅ Successfully connected to Supabase!
✅ Supabase connection successful!
* Running on http://127.0.0.1:5000
```

---

## Step 9: Open in Browser

Go to: **http://localhost:5000**

You should see all 415 students loaded!

---

## Step 10: Verify Data in Supabase

1. Go back to Supabase dashboard
2. Click **Table Editor** (left sidebar)
3. Click on **students** table
4. You should see all 415 students!

---

## Project Structure (Supabase Version)

```
New-start/
├── app_supabase.py          # ⭐ Main Flask app (Supabase version)
├── database_supabase.py     # ⭐ Database operations (Supabase)
├── supabase_schema.sql      # ⭐ PostgreSQL schema
├── .env                     # ⭐ Your credentials (create this)
├── .env.example             # Example .env file
├── ai_matcher.py            # AI matching algorithm
├── requirements.txt         # Updated with Supabase packages
├── students_data.csv        # Your 415 students
├── static/                  # Frontend files
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

---

## Advantages of Supabase Version

### ✅ Cloud-Based
- No local database file
- Access from anywhere
- Share with team easily

### ✅ Real-Time Updates
- Changes sync instantly
- Multiple users can use simultaneously

### ✅ Better Performance
- PostgreSQL is more powerful than SQLite
- Better for production use

### ✅ Easy Deployment
- Deploy to Vercel, Heroku, Railway easily
- No database file to manage

### ✅ Data Persistence
- Data is safe in the cloud
- Automatic backups

---

## Viewing Your Data

### In Supabase Dashboard

1. **Table Editor** - View/edit data in spreadsheet format
2. **SQL Editor** - Run custom queries
3. **API Docs** - Auto-generated API documentation
4. **Database** → **Backups** - Schedule backups

### Example Queries to Try

In SQL Editor, try these:

```sql
-- Count students by semester
SELECT semester, COUNT(*) as count
FROM students
GROUP BY semester
ORDER BY semester;

-- View all groups with members
SELECT
  g.name as group_name,
  t.title as topic,
  COUNT(gm.id) as member_count
FROM groups g
LEFT JOIN topics t ON g.topic_id = t.id
LEFT JOIN group_members gm ON g.id = gm.group_id
GROUP BY g.id, g.name, t.title;

-- Students not in any group
SELECT semester, COUNT(*) as available
FROM students
WHERE is_grouped = false
GROUP BY semester;
```

---

## Common Issues & Solutions

### Issue 1: "SUPABASE_URL not found"

**Problem:** `.env` file not loaded

**Solution:**
```bash
# Make sure .env is in project root
ls -la .env  # Mac/Linux
dir .env     # Windows

# Check the file contains your credentials
cat .env     # Mac/Linux
type .env    # Windows
```

### Issue 2: "Failed to connect to Supabase"

**Problem:** Wrong credentials or network issue

**Solution:**
- Double-check your SUPABASE_URL and SUPABASE_KEY in `.env`
- Make sure you used the **anon/public key**, not service_role
- Check your internet connection
- Verify project is not paused in Supabase dashboard

### Issue 3: "Table students does not exist"

**Problem:** Schema not created

**Solution:**
- Go back to Supabase SQL Editor
- Run the entire `supabase_schema.sql` file again

### Issue 4: "Module 'supabase' not found"

**Problem:** Packages not installed

**Solution:**
```bash
# Activate venv first
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

### Issue 5: Students not loading

**Problem:** CSV file path or permission issue

**Solution:**
```bash
# Make sure you're in project directory
pwd  # Mac/Linux - should show /path/to/New-start
cd   # Windows - should show path to New-start

# Check CSV exists
ls students_data.csv

# Try loading manually
python -c "import database_supabase as db; db.load_students_from_csv()"
```

---

## Security Best Practices

### ✅ DO:
- Keep `.env` file secret
- Add `.env` to `.gitignore`
- Use the **anon/public key** for client-side
- Use **RLS (Row Level Security)** in Supabase for production

### ❌ DON'T:
- Commit `.env` to Git
- Share your API keys publicly
- Use service_role key in frontend

---

## Upgrading from SQLite Version

If you were using the SQLite version (`app.py`), here's what changed:

| SQLite Version | Supabase Version |
|----------------|------------------|
| `app.py` | `app_supabase.py` |
| `database.py` | `database_supabase.py` |
| `schema.sql` | `supabase_schema.sql` |
| `student_groups.db` | Cloud PostgreSQL |
| No `.env` needed | `.env` required |

You can keep both versions and switch between them!

---

## Testing the Application

### Test Checklist:

- [ ] Server starts successfully
- [ ] ✅ "Successfully connected to Supabase!" message appears
- [ ] Can view students by semester
- [ ] Can select students (cards turn purple)
- [ ] Can create groups (manual or AI)
- [ ] Groups appear in "Groups" tab
- [ ] Chat works in "Group Chat" tab
- [ ] Topics load correctly
- [ ] Data persists after server restart

---

## Deployment Options

Now that you're using Supabase, you can easily deploy to:

1. **Vercel** - Free, automatic deployments
2. **Railway** - Easy Python deployment
3. **Heroku** - Classic PaaS
4. **Render** - Modern cloud platform
5. **PythonAnywhere** - Python-specific hosting

Supabase stays the same regardless of where you deploy!

---

## Next Steps

1. ✅ Verify all 415 students are loaded
2. ✅ Test creating some groups
3. ✅ Try the AI suggestions feature
4. ✅ Test the chat functionality
5. 🚀 Consider deploying to production

---

## Getting Help

**Supabase Issues:**
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)

**Project Issues:**
- Check `SUPABASE_SETUP.md` (this file)
- Review error messages in terminal
- Check browser console (F12)

---

## Supabase Dashboard Tips

### Useful Features:

1. **Logs** - See all database queries in real-time
2. **Database** → **Roles** - Manage permissions
3. **API** - Test API endpoints directly
4. **Storage** - Add file upload later
5. **Auth** - Add user authentication later

---

## Quick Command Reference

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Load students
python -c "import database_supabase as db; db.load_students_from_csv()"

# Run app
python app_supabase.py

# Test connection
python -c "import database_supabase as db; db.test_connection()"
```

---

## Success! 🎉

You now have a cloud-powered AI Student Group Matcher with:
- ☁️ Cloud PostgreSQL database
- 🤖 AI-powered matching
- 💬 Real-time chat
- 🌐 Ready for production deployment

**Enjoy building amazing student groups!**
