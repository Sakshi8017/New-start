from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
import database as db
from ai_matcher import StudentMatcher
import os

app = Flask(__name__, static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize AI matcher
matcher = StudentMatcher()

# Initialize database on first run
if not os.path.exists('student_groups.db'):
    db.init_db()
    db.load_students_from_csv()
    print("Database initialized and students loaded!")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students or filter by semester"""
    semester = request.args.get('semester', type=int)
    if semester:
        students = db.get_students_by_semester(semester)
    else:
        students = db.get_all_students()
    return jsonify(students)

@app.route('/api/students/available', methods=['GET'])
def get_available_students():
    """Get students who are not in a group"""
    semester = request.args.get('semester', type=int, default=3)
    students = db.get_available_students(semester)
    return jsonify(students)

@app.route('/api/students/<usn>', methods=['GET'])
def get_student(usn):
    """Get a specific student by USN"""
    student = db.get_student_by_usn(usn)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students/<usn>/profile', methods=['PUT'])
def update_student_profile(usn):
    """Update student profile (skills, interests, bio)"""
    data = request.json
    skills = data.get('skills', [])
    interests = data.get('interests', [])
    bio = data.get('bio', '')

    db.update_student_profile(usn, skills, interests, bio)
    return jsonify({'success': True, 'message': 'Profile updated successfully'})

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get topics by semester"""
    semester = request.args.get('semester', type=int, default=3)
    topics = db.get_topics_by_semester(semester)
    return jsonify(topics)

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """Get all groups"""
    groups = db.get_all_groups()
    return jsonify(groups)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    data = request.json
    name = data.get('name')
    topic_id = data.get('topic_id')
    semester = data.get('semester')
    student_ids = data.get('student_ids', [])

    if len(student_ids) < 4 or len(student_ids) > 5:
        return jsonify({'error': 'Group must have 4-5 students'}), 400

    group_id = db.create_group(name, topic_id, semester, student_ids)
    return jsonify({'success': True, 'group_id': group_id})

@app.route('/api/groups/suggest', methods=['POST'])
def suggest_groups():
    """AI-powered group suggestions"""
    data = request.json
    semester = data.get('semester', 3)
    group_size = data.get('group_size', 5)
    num_groups = data.get('num_groups', None)

    # Get available students
    students = db.get_available_students(semester)

    if len(students) < group_size:
        return jsonify({'error': 'Not enough students available'}), 400

    # Use AI matcher to suggest groups
    suggested_groups = matcher.suggest_groups(students, group_size, num_groups)

    # Calculate compatibility scores
    for group in suggested_groups:
        group['compatibility_score'] = matcher.evaluate_group_compatibility(group['members'])

    return jsonify(suggested_groups)

@app.route('/api/messages/<int:group_id>', methods=['GET'])
def get_group_messages(group_id):
    """Get messages for a group"""
    limit = request.args.get('limit', type=int, default=100)
    messages = db.get_messages(group_id, limit)
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    """Send a message to a group"""
    data = request.json
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    message = data.get('message')

    message_id = db.add_message(group_id, student_id, message)

    # Emit to all clients in the group room
    socketio.emit('new_message', {
        'id': message_id,
        'group_id': group_id,
        'student_id': student_id,
        'message': message
    }, room=f'group_{group_id}')

    return jsonify({'success': True, 'message_id': message_id})

# WebSocket events for real-time chat
@socketio.on('join_group')
def on_join_group(data):
    """Join a group chat room"""
    group_id = data.get('group_id')
    room = f'group_{group_id}'
    join_room(room)
    emit('joined', {'group_id': group_id})

@socketio.on('send_message')
def on_send_message(data):
    """Handle real-time message sending"""
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    message = data.get('message')

    # Save to database
    message_id = db.add_message(group_id, student_id, message)

    # Get student info
    student = db.get_student_by_usn(data.get('usn', ''))
    student_name = student['name'] if student else 'Unknown'

    # Broadcast to room
    emit('new_message', {
        'id': message_id,
        'group_id': group_id,
        'student_id': student_id,
        'student_name': student_name,
        'message': message,
        'created_at': str(db.datetime.datetime.now())
    }, room=f'group_{group_id}')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
