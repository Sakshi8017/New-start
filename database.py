import sqlite3
import json
import csv
from datetime import datetime

DATABASE = 'student_groups.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def load_students_from_csv():
    """Load students from CSV file into database"""
    conn = get_db()
    cursor = conn.cursor()

    with open('students_data.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            try:
                cursor.execute('''
                    INSERT INTO students (sl_no, usn, name, email, semester)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['sl_no'], row['usn'], row['name'], row['email'], row['semester']))
            except sqlite3.IntegrityError:
                # Skip duplicates
                continue

    conn.commit()
    conn.close()

def get_all_students():
    """Get all students"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY semester, name')
    students = [dict(row) for row in cursor.fetchall()]

    # Parse JSON fields
    for student in students:
        student['skills'] = json.loads(student['skills']) if student['skills'] else []
        student['interests'] = json.loads(student['interests']) if student['interests'] else []

    conn.close()
    return students

def get_students_by_semester(semester):
    """Get students by semester"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE semester = ? ORDER BY name', (semester,))
    students = [dict(row) for row in cursor.fetchall()]

    for student in students:
        student['skills'] = json.loads(student['skills']) if student['skills'] else []
        student['interests'] = json.loads(student['interests']) if student['interests'] else []

    conn.close()
    return students

def get_available_students(semester):
    """Get students who are not in a group"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM students
        WHERE semester = ? AND is_grouped = 0
        ORDER BY name
    ''', (semester,))
    students = [dict(row) for row in cursor.fetchall()]

    for student in students:
        student['skills'] = json.loads(student['skills']) if student['skills'] else []
        student['interests'] = json.loads(student['interests']) if student['interests'] else []

    conn.close()
    return students

def update_student_profile(usn, skills, interests, bio):
    """Update student profile with skills, interests, and bio"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE students
        SET skills = ?, interests = ?, bio = ?
        WHERE usn = ?
    ''', (json.dumps(skills), json.dumps(interests), bio, usn))

    conn.commit()
    conn.close()

def get_student_by_usn(usn):
    """Get student by USN"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE usn = ?', (usn,))
    row = cursor.fetchone()

    if row:
        student = dict(row)
        student['skills'] = json.loads(student['skills']) if student['skills'] else []
        student['interests'] = json.loads(student['interests']) if student['interests'] else []
    else:
        student = None

    conn.close()
    return student

def get_topics_by_semester(semester):
    """Get topics for a specific semester"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM topics WHERE semester = ?', (semester,))
    topics = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return topics

def create_group(name, topic_id, semester, student_ids):
    """Create a new group with members"""
    conn = get_db()
    cursor = conn.cursor()

    # Create group
    cursor.execute('''
        INSERT INTO groups (name, topic_id, semester)
        VALUES (?, ?, ?)
    ''', (name, topic_id, semester))

    group_id = cursor.lastrowid

    # Add members
    for i, student_id in enumerate(student_ids):
        role = 'leader' if i == 0 else 'member'
        cursor.execute('''
            INSERT INTO group_members (group_id, student_id, role)
            VALUES (?, ?, ?)
        ''', (group_id, student_id, role))

        # Mark student as grouped
        cursor.execute('''
            UPDATE students SET is_grouped = 1 WHERE id = ?
        ''', (student_id,))

    conn.commit()
    conn.close()
    return group_id

def get_all_groups():
    """Get all groups with their members and topic"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT g.*, t.title as topic_title, t.category as topic_category
        FROM groups g
        LEFT JOIN topics t ON g.topic_id = t.id
        ORDER BY g.created_at DESC
    ''')

    groups = []
    for row in cursor.fetchall():
        group = dict(row)

        # Get members
        cursor.execute('''
            SELECT s.*, gm.role
            FROM students s
            JOIN group_members gm ON s.id = gm.student_id
            WHERE gm.group_id = ?
        ''', (group['id'],))

        members = []
        for member_row in cursor.fetchall():
            member = dict(member_row)
            member['skills'] = json.loads(member['skills']) if member['skills'] else []
            member['interests'] = json.loads(member['interests']) if member['interests'] else []
            members.append(member)

        group['members'] = members
        groups.append(group)

    conn.close()
    return groups

def add_message(group_id, student_id, message):
    """Add a chat message to a group"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO messages (group_id, student_id, message)
        VALUES (?, ?, ?)
    ''', (group_id, student_id, message))

    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id

def get_messages(group_id, limit=100):
    """Get chat messages for a group"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT m.*, s.name as student_name, s.usn
        FROM messages m
        JOIN students s ON m.student_id = s.id
        WHERE m.group_id = ?
        ORDER BY m.created_at DESC
        LIMIT ?
    ''', (group_id, limit))

    messages = [dict(row) for row in cursor.fetchall()]
    messages.reverse()  # Show oldest first
    conn.close()
    return messages
