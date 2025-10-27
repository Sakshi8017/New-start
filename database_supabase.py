import os
import json
import csv
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in your .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_students_from_csv():
    """Load students from CSV file into Supabase"""
    try:
        with open('students_data.csv', 'r') as f:
            csv_reader = csv.DictReader(f)
            students_data = []

            for row in csv_reader:
                student = {
                    'sl_no': int(row['sl_no']),
                    'usn': row['usn'],
                    'name': row['name'],
                    'email': row['email'],
                    'semester': int(row['semester']),
                    'skills': [],
                    'interests': [],
                    'bio': None,
                    'is_grouped': False
                }
                students_data.append(student)

            # Insert in batches to avoid timeout
            batch_size = 100
            for i in range(0, len(students_data), batch_size):
                batch = students_data[i:i+batch_size]
                response = supabase.table('students').upsert(batch, on_conflict='usn').execute()
                print(f"Inserted batch {i//batch_size + 1}: {len(batch)} students")

            print(f"Successfully loaded {len(students_data)} students!")
            return True

    except Exception as e:
        print(f"Error loading students: {str(e)}")
        return False

def get_all_students():
    """Get all students"""
    try:
        response = supabase.table('students').select('*').order('semester,name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting students: {str(e)}")
        return []

def get_students_by_semester(semester):
    """Get students by semester"""
    try:
        response = supabase.table('students').select('*').eq('semester', semester).order('name').execute()
        return response.data
    except Exception as e:
        print(f"Error getting students by semester: {str(e)}")
        return []

def get_available_students(semester):
    """Get students who are not in a group"""
    try:
        response = supabase.table('students')\
            .select('*')\
            .eq('semester', semester)\
            .eq('is_grouped', False)\
            .order('name')\
            .execute()
        return response.data
    except Exception as e:
        print(f"Error getting available students: {str(e)}")
        return []

def update_student_profile(usn, skills, interests, bio):
    """Update student profile with skills, interests, and bio"""
    try:
        response = supabase.table('students')\
            .update({
                'skills': skills,
                'interests': interests,
                'bio': bio
            })\
            .eq('usn', usn)\
            .execute()
        return True
    except Exception as e:
        print(f"Error updating student profile: {str(e)}")
        return False

def get_student_by_usn(usn):
    """Get student by USN"""
    try:
        response = supabase.table('students').select('*').eq('usn', usn).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting student: {str(e)}")
        return None

def get_student_by_id(student_id):
    """Get student by ID"""
    try:
        response = supabase.table('students').select('*').eq('id', student_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting student: {str(e)}")
        return None

def get_topics_by_semester(semester):
    """Get topics for a specific semester"""
    try:
        response = supabase.table('topics').select('*').eq('semester', semester).execute()
        return response.data
    except Exception as e:
        print(f"Error getting topics: {str(e)}")
        return []

def create_group(name, topic_id, semester, student_ids):
    """Create a new group with members"""
    try:
        # Create group
        group_data = {
            'name': name,
            'topic_id': topic_id,
            'semester': semester
        }
        group_response = supabase.table('groups').insert(group_data).execute()

        if not group_response.data:
            return None

        group_id = group_response.data[0]['id']

        # Add members
        members_data = []
        for i, student_id in enumerate(student_ids):
            role = 'leader' if i == 0 else 'member'
            members_data.append({
                'group_id': group_id,
                'student_id': student_id,
                'role': role
            })

        supabase.table('group_members').insert(members_data).execute()

        # Mark students as grouped
        for student_id in student_ids:
            supabase.table('students').update({'is_grouped': True}).eq('id', student_id).execute()

        return group_id

    except Exception as e:
        print(f"Error creating group: {str(e)}")
        return None

def get_all_groups():
    """Get all groups with their members and topic"""
    try:
        # Get all groups with topic info
        groups_response = supabase.table('groups')\
            .select('*, topics(title, category)')\
            .order('created_at', desc=True)\
            .execute()

        groups = []
        for group in groups_response.data:
            # Get members for this group
            members_response = supabase.table('group_members')\
                .select('*, students(*)')\
                .eq('group_id', group['id'])\
                .execute()

            # Flatten the student data
            members = []
            for member in members_response.data:
                student = member['students']
                student['role'] = member['role']
                members.append(student)

            # Format group data
            group_data = {
                'id': group['id'],
                'name': group['name'],
                'semester': group['semester'],
                'status': group['status'],
                'created_at': group['created_at'],
                'topic_title': group['topics']['title'] if group.get('topics') else None,
                'topic_category': group['topics']['category'] if group.get('topics') else None,
                'members': members
            }
            groups.append(group_data)

        return groups

    except Exception as e:
        print(f"Error getting groups: {str(e)}")
        return []

def add_message(group_id, student_id, message):
    """Add a chat message to a group"""
    try:
        message_data = {
            'group_id': group_id,
            'student_id': student_id,
            'message': message
        }
        response = supabase.table('messages').insert(message_data).execute()

        if response.data:
            return response.data[0]['id']
        return None

    except Exception as e:
        print(f"Error adding message: {str(e)}")
        return None

def get_messages(group_id, limit=100):
    """Get chat messages for a group"""
    try:
        response = supabase.table('messages')\
            .select('*, students(name, usn)')\
            .eq('group_id', group_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()

        # Format messages
        messages = []
        for msg in reversed(response.data):  # Reverse to show oldest first
            message = {
                'id': msg['id'],
                'group_id': msg['group_id'],
                'student_id': msg['student_id'],
                'message': msg['message'],
                'created_at': msg['created_at'],
                'student_name': msg['students']['name'],
                'usn': msg['students']['usn']
            }
            messages.append(message)

        return messages

    except Exception as e:
        print(f"Error getting messages: {str(e)}")
        return []

# Test connection
def test_connection():
    """Test Supabase connection"""
    try:
        response = supabase.table('students').select('count').execute()
        print("✅ Successfully connected to Supabase!")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        return False
