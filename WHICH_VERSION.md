# Which Version Should I Use?

You have **TWO versions** of the app. Here's which one to use:

---

## 🏠 SQLite Version (Local Database)

**Best for:** Learning, testing, quick start

### Files to Use:
```
app.py              ← Run this
database.py         ← Uses this
schema.sql          ← Database structure
student_groups.db   ← Created automatically
```

### To Run:
```bash
python app.py
```

### ✅ Pros:
- No setup needed
- Everything local
- No internet required
- Simpler to understand

### ❌ Cons:
- Database file can get lost
- Can't share with team
- Not good for production
- Single user only

---

## ☁️ Supabase Version (Cloud Database)

**Best for:** Production, deployment, team projects

### Files to Use:
```
app_supabase.py         ← Run this
database_supabase.py    ← Uses this
supabase_schema.sql     ← Run in Supabase
.env                    ← Your credentials
```

### To Run:
```bash
python app_supabase.py
```

### ✅ Pros:
- Cloud-hosted (free 500MB)
- Access from anywhere
- Team collaboration
- Production-ready
- Real-time updates
- Easy deployment
- Automatic backups

### ❌ Cons:
- Requires Supabase account
- Need internet connection
- 5-10 min setup time

---

## Quick Comparison

| Feature | SQLite | Supabase |
|---------|--------|----------|
| **Setup Time** | 0 min | 10 min |
| **Internet Needed** | ❌ No | ✅ Yes |
| **Cloud Database** | ❌ No | ✅ Yes |
| **Multi-user** | ❌ No | ✅ Yes |
| **Production Ready** | ❌ No | ✅ Yes |
| **Free** | ✅ Yes | ✅ Yes |
| **Easy Deployment** | ❌ Hard | ✅ Easy |
| **Data Safety** | ⚠️ Local only | ✅ Backed up |

---

## Recommended Path

### 🎯 For Quick Testing (Right Now):
```bash
# Just run this!
python app.py
```

### 🚀 For Actual Use (Next):
Follow `SUPABASE_QUICKSTART.md` (10 minutes)

---

## How to Switch

You can use BOTH versions on the same project!

**Switch to SQLite:**
```bash
python app.py
```

**Switch to Supabase:**
```bash
python app_supabase.py
```

They use different databases, so data doesn't mix.

---

## File Structure

```
New-start/
├── 🏠 SQLite Version
│   ├── app.py
│   ├── database.py
│   ├── schema.sql
│   └── student_groups.db (auto-created)
│
├── ☁️ Supabase Version
│   ├── app_supabase.py
│   ├── database_supabase.py
│   ├── supabase_schema.sql
│   └── .env (you create this)
│
├── 🤖 Shared Files (both use)
│   ├── ai_matcher.py
│   ├── students_data.csv
│   ├── requirements.txt
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── app.js
│
└── 📚 Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── VSCODE_SETUP.md
    ├── SUPABASE_SETUP.md
    ├── SUPABASE_QUICKSTART.md
    └── WHICH_VERSION.md (you are here!)
```

---

## My Recommendation

### If you're just exploring:
```bash
cd New-start
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app.py
```
→ Open http://localhost:5000

### If you want to deploy or use seriously:
Follow `SUPABASE_QUICKSTART.md` to set up Supabase

---

## Still Confused?

**Start with SQLite version:**
1. It works immediately
2. No account needed
3. No setup

**Then upgrade to Supabase when:**
- You want to deploy online
- You want team collaboration
- You need data safety
- You're ready for production

---

## Need Help?

- **SQLite version:** Read `QUICKSTART.md`
- **Supabase version:** Read `SUPABASE_QUICKSTART.md`
- **VS Code setup:** Read `VSCODE_SETUP.md`
- **Full details:** Read `README.md` or `SUPABASE_SETUP.md`

---

**Choose one and start building amazing student groups!** 🎓✨
