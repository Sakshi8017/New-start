# Supabase Quick Start - 10 Minutes to Cloud Database

## Super Fast Setup

### 1️⃣ Create Supabase Project (2 min)

1. Go to [supabase.com](https://supabase.com) → Sign up
2. **New Project** → Name it `student-matcher`
3. Choose **Free** plan → Create
4. Wait for setup to complete ⏳

---

### 2️⃣ Run the Schema (1 min)

1. Click **SQL Editor** (left sidebar)
2. Click **New Query**
3. Copy & paste ALL code from `supabase_schema.sql`
4. Click **Run** ▶️
5. Should see: ✅ Success!

---

### 3️⃣ Get Your Keys (1 min)

1. Click **⚙️ Settings** → **API**
2. Copy these TWO values:

```
Project URL: https://xxxxx.supabase.co
anon key: eyJhbGciOiJIUz...
```

---

### 4️⃣ Create `.env` File (1 min)

In your project folder, create a file named `.env`:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUz...
```

Paste YOUR actual values!

---

### 5️⃣ Install & Run (5 min)

```bash
# Navigate to project
cd New-start

# Activate venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt

# Load students
python -c "import database_supabase as db; db.load_students_from_csv()"

# Run app
python app_supabase.py
```

---

### 6️⃣ Open Browser

Go to: **http://localhost:5000**

**Done!** 🎉 Your app is now running with cloud database!

---

## What You Get

✅ **415 students** loaded in cloud
✅ **AI matching** algorithm
✅ **Real-time chat** functionality
✅ **No local database** needed
✅ **Access from anywhere**
✅ **Free Supabase tier** (500MB)

---

## Quick Checks

### ✅ Is it working?

You should see:
```
Testing Supabase connection...
✅ Successfully connected to Supabase!
* Running on http://127.0.0.1:5000
```

### ❌ Connection failed?

Check:
- Is `.env` in the right folder? (same as `app_supabase.py`)
- Did you paste YOUR keys (not the example)?
- Is your internet working?
- Did you run the schema SQL?

---

## View Your Data

1. Go to Supabase dashboard
2. Click **Table Editor**
3. Click **students** → See all 415 students!
4. Click **topics** → See all project topics!

---

## Next: Test Features

1. **Select semester** from dropdown
2. **Pick a topic**
3. **Click "AI Suggest Groups"**
4. **Create a group**
5. **Try the chat!**

---

## Files You Need

| File | What it does |
|------|-------------|
| `app_supabase.py` | Main server (cloud version) |
| `database_supabase.py` | Database code (cloud) |
| `.env` | Your secret keys |
| `supabase_schema.sql` | Database structure |

---

## Switch Between SQLite and Supabase

**Use SQLite (local):**
```bash
python app.py
```

**Use Supabase (cloud):**
```bash
python app_supabase.py
```

Both work! Use Supabase for production.

---

## Troubleshooting

### "Module supabase not found"
```bash
pip install supabase python-dotenv psycopg2-binary
```

### "SUPABASE_URL not found"
Make sure `.env` file exists:
```bash
ls .env  # Should exist
cat .env # Should show your keys
```

### Students not loading
```bash
# Try again
python -c "import database_supabase as db; db.load_students_from_csv()"
```

---

## Ready to Deploy?

Your app is now cloud-ready! Deploy to:
- Vercel (easiest)
- Railway
- Render
- Heroku

Same Supabase database works everywhere! 🚀

---

**Need detailed help?** Read `SUPABASE_SETUP.md`

**Enjoy your cloud-powered group matcher!** ☁️
