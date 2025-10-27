-- Supabase PostgreSQL Schema for AI Student Group Matcher
-- Run this in Supabase SQL Editor

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    sl_no INTEGER,
    usn TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    semester INTEGER NOT NULL,
    skills JSONB DEFAULT '[]'::jsonb,
    interests JSONB DEFAULT '[]'::jsonb,
    bio TEXT,
    is_grouped BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Topics Table
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    semester INTEGER NOT NULL,
    branch TEXT DEFAULT 'IS',
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Groups Table
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    topic_id INTEGER REFERENCES topics(id),
    semester INTEGER,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Group Members Table
CREATE TABLE IF NOT EXISTS group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, student_id)
);

-- Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_students_semester ON students(semester);
CREATE INDEX IF NOT EXISTS idx_students_is_grouped ON students(is_grouped);
CREATE INDEX IF NOT EXISTS idx_topics_semester ON topics(semester);
CREATE INDEX IF NOT EXISTS idx_groups_semester ON groups(semester);
CREATE INDEX IF NOT EXISTS idx_group_members_group_id ON group_members(group_id);
CREATE INDEX IF NOT EXISTS idx_group_members_student_id ON group_members(student_id);
CREATE INDEX IF NOT EXISTS idx_messages_group_id ON messages(group_id);

-- Insert Sample Topics
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
('Enterprise Application', 'Build a large-scale enterprise software system', 7, 'Software Engineering')
ON CONFLICT DO NOTHING;
