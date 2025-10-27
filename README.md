# AI Student Group Matcher

An intelligent web application that uses AI to create optimal student groups based on skills, interests, and diversity. Built for RV College of Engineering's Information Science Department.

## Features

### 1. Smart Student Selection
- View all students from different semesters (3, 5, 7)
- Filter students by semester
- See student profiles with skills and interests
- Visual indicators for students already in groups (grayed out with "GROUPED" badge)
- Select 4-5 students manually for group formation

### 2. AI-Powered Group Matching
- Intelligent algorithm that analyzes student profiles
- Creates diverse groups with complementary skills
- Calculates compatibility scores for each suggested group
- Considers skill diversity and common interests
- Suggests optimal group formations

### 3. Topic Selection System
- Branch-specific topics for each semester
- Semester 3: Web Development, Mobile Apps, Data Structures, etc.
- Semester 5: Machine Learning, Blockchain, Cloud Computing, IoT, etc.
- Semester 7: Advanced projects, Research, Enterprise Applications
- Easy topic selection from dropdown

### 4. Real-time Group Chat
- WebSocket-based real-time messaging
- Each group has its own chat room
- Students can discuss project topics
- Message history is saved
- Live updates when new messages arrive

### 5. Group Management
- View all created groups
- See group members with roles (Leader/Member)
- Display associated topics
- Track group status

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Database for storing students, groups, messages
- **Flask-SocketIO**: Real-time WebSocket communication
- **scikit-learn**: AI/ML algorithms for group matching
- **pandas & numpy**: Data processing

### Frontend
- **HTML5/CSS3**: Modern responsive UI
- **JavaScript (ES6+)**: Interactive functionality
- **Socket.IO Client**: Real-time chat
- **Gradient Design**: Beautiful purple gradient theme

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
The database will be automatically initialized on first run, but you can also do it manually:

```python
python -c "import database as db; db.init_db(); db.load_students_from_csv()"
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Creating Groups Manually

1. **Select Semester**: Choose semester 3, 5, or 7 from the dropdown
2. **Select Topic**: Pick a topic from the topic dropdown
3. **Select Students**: Click on 4-5 student cards to select them
   - Selected students are highlighted in purple gradient
   - Already grouped students are grayed out
4. **Create Group**: Click "Create Group" button (enabled when 4-5 students selected)

### Using AI Group Suggestions

1. **Select Semester**: Choose the semester
2. **Select Topic**: Pick a topic
3. **Click "AI Suggest Groups"**: The AI will analyze all available students
4. **Review Suggestions**: See 3 suggested groups with compatibility scores
5. **Accept Suggestion**: Click "Create This Group" on your preferred suggestion

### Group Chat

1. **Navigate to Chat Tab**: Click on "Group Chat" tab
2. **Select a Group**: Click on a group from the sidebar
3. **Type Message**: Use the input box at the bottom
4. **Send**: Press Enter or click "Send" button
5. **Real-time Updates**: Messages appear instantly for all group members

### Viewing Topics

Navigate to the "Topics" tab to see all available topics organized by semester.

## Database Schema

### Students Table
- Personal information (USN, name, email, semester)
- Skills and interests (JSON arrays)
- Grouping status
- Bio/description

### Topics Table
- Topic title and description
- Semester association
- Category (Web Dev, AI/ML, etc.)

### Groups Table
- Group name and status
- Associated topic
- Creation timestamp

### Group Members Table
- Links students to groups
- Role designation (leader/member)

### Messages Table
- Group chat messages
- Timestamps
- Student attribution

## AI Matching Algorithm

The AI matcher uses:

1. **TF-IDF Vectorization**: Converts student profiles to numerical vectors
2. **Cosine Similarity**: Calculates similarity between students
3. **Diversity Optimization**: Prefers students with complementary skills
4. **Greedy Group Formation**: Iteratively builds optimal groups
5. **Compatibility Scoring**: Evaluates group quality based on:
   - Skill diversity (30% weight)
   - Common interests (boost)
   - Skill balance (50% weight)

## API Endpoints

### Student Endpoints
- `GET /api/students` - Get all students
- `GET /api/students/available?semester={n}` - Get ungrouped students
- `GET /api/students/{usn}` - Get specific student
- `PUT /api/students/{usn}/profile` - Update student profile

### Topic Endpoints
- `GET /api/topics?semester={n}` - Get topics by semester

### Group Endpoints
- `GET /api/groups` - Get all groups
- `POST /api/groups` - Create new group
- `POST /api/groups/suggest` - Get AI suggestions

### Message Endpoints
- `GET /api/messages/{group_id}` - Get group messages
- `POST /api/messages` - Send message

### WebSocket Events
- `join_group` - Join a chat room
- `send_message` - Send real-time message
- `new_message` - Receive new messages

## Customization

### Adding New Topics
Edit `schema.sql` and add INSERT statements:

```sql
INSERT INTO topics (title, description, semester, category) VALUES
('Your Topic', 'Description', 3, 'Category');
```

### Changing Group Size
Modify the validation in `app.py` and `app.js`:

```python
if len(student_ids) < 4 or len(student_ids) > 5:
```

### Adjusting AI Weights
Edit `ai_matcher.py` in the `evaluate_group_compatibility` method:

```python
score = (
    diversity_score * 30 +  # Skill diversity weight
    len(common_interests) * 10 +  # Common interest points
    skill_balance * 50  # Skill balance weight
)
```

## Student Profile Enhancement

Students can be assigned skills and interests by updating the database:

```python
db.update_student_profile(
    usn='1RV24IS001',
    skills=['Python', 'JavaScript', 'React'],
    interests=['Web Development', 'AI'],
    bio='Passionate about full-stack development'
)
```

## Future Enhancements

- Student login system with authentication
- Profile editing interface
- File sharing in group chats
- Group project submission
- Progress tracking
- Faculty supervision panel
- Email notifications
- Mobile app version
- Video call integration

## Troubleshooting

### Database Issues
If you encounter database errors, delete `student_groups.db` and restart the app.

### Port Already in Use
Change the port in `app.py`:
```python
socketio.run(app, debug=True, port=5001)
```

### WebSocket Connection Issues
Make sure you're using `http://` and not `https://` for local development.

## Project Structure

```
New-start/
├── app.py                  # Flask backend
├── database.py             # Database operations
├── ai_matcher.py          # AI matching algorithm
├── schema.sql             # Database schema
├── students_data.csv      # Student data
├── requirements.txt       # Python dependencies
├── student_groups.db      # SQLite database (auto-generated)
├── static/
│   ├── index.html        # Main HTML page
│   ├── styles.css        # Styling
│   └── app.js            # Frontend JavaScript
└── README.md             # Documentation
```

## License

This project is created for educational purposes for RV College of Engineering.

## Contributors

Built with AI assistance for RVCE Information Science Department.

## Support

For issues or questions, please refer to the code comments or modify as needed for your specific use case.