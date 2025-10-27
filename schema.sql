-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sl_no INTEGER,
    usn TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    semester INTEGER NOT NULL,
    skills TEXT,  -- JSON array of skills
    interests TEXT,  -- JSON array of interests
    bio TEXT,
    is_grouped BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Topics Table (Branch/Semester specific topics)
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    semester INTEGER NOT NULL,
    branch TEXT DEFAULT 'IS',  -- Information Science
    category TEXT,  -- e.g., Web Development, AI/ML, Mobile Dev, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Groups Table
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    topic_id INTEGER,
    semester INTEGER,
    status TEXT DEFAULT 'active',  -- active, completed, disbanded
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id)
);

-- Group Members Table (Junction table)
CREATE TABLE IF NOT EXISTS group_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    role TEXT DEFAULT 'member',  -- leader, member
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE(group_id, student_id)
);

-- Chat Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Student Skills Table (for better querying)
CREATE TABLE IF NOT EXISTS student_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    proficiency TEXT DEFAULT 'intermediate',  -- beginner, intermediate, advanced
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Student Interests Table
CREATE TABLE IF NOT EXISTS student_interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    interest_name TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Sample Topics for different semesters
INSERT INTO topics (title, description, semester, category) VALUES
-- Semester 3 Topics
('Web Development Project', 'Build a full-stack web application using modern frameworks', 3, 'Web Development'),
('Mobile App Development', 'Create a mobile application for Android/iOS', 3, 'Mobile Development'),
('Data Structures Implementation', 'Implement and analyze complex data structures', 3, 'Algorithms'),
('Database Management System', 'Design and implement a database system', 3, 'Database'),
('AI Chatbot Development', 'Build an AI-powered chatbot', 3, 'Artificial Intelligence'),

-- Semester 5 Topics
('Machine Learning Project', 'Develop a machine learning model for real-world problem', 5, 'AI/ML'),
('Blockchain Application', 'Build a decentralized application using blockchain', 5, 'Blockchain'),
('Cloud Computing Project', 'Deploy scalable applications on cloud platforms', 5, 'Cloud Computing'),
('IoT System Design', 'Create an Internet of Things system', 5, 'IoT'),
('Cybersecurity Tool', 'Develop a security analysis or penetration testing tool', 5, 'Cybersecurity'),
('Computer Vision Application', 'Build an application using computer vision', 5, 'AI/ML'),

-- Semester 7 Topics
('Final Year Project - AI/ML', 'Advanced machine learning or deep learning project', 7, 'AI/ML'),
('Final Year Project - Web3', 'Blockchain and decentralized application development', 7, 'Blockchain'),
('Final Year Project - Cloud Native', 'Microservices and cloud-native architecture', 7, 'Cloud Computing'),
('Final Year Project - DevOps', 'CI/CD pipeline and infrastructure automation', 7, 'DevOps'),
('Research Paper Implementation', 'Implement a research paper in computer science', 7, 'Research'),
('Enterprise Application', 'Build a large-scale enterprise software system', 7, 'Software Engineering');
