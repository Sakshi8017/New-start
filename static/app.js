// Global state
let currentSemester = 3;
let selectedStudents = [];
let allStudents = [];
let currentGroup = null;
let socket = null;

// Initialize Socket.IO
function initSocket() {
    socket = io('http://localhost:5000');

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('new_message', (data) => {
        if (currentGroup && data.group_id === currentGroup.id) {
            appendMessage(data);
        }
    });
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initSocket();
    setupTabs();
    setupEventListeners();
    loadStudents();
    loadTopics();
    loadGroups();
});

// Tab switching
function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');

            // Load data when switching tabs
            if (tabName === 'groups') {
                loadGroups();
            } else if (tabName === 'chat') {
                loadChatGroups();
            }
        });
    });
}

// Event listeners
function setupEventListeners() {
    document.getElementById('semester-filter').addEventListener('change', (e) => {
        currentSemester = parseInt(e.target.value);
        loadStudents();
        loadTopicsBySemester(currentSemester);
    });

    document.getElementById('ai-suggest-btn').addEventListener('click', showAISuggestions);
    document.getElementById('create-group-btn').addEventListener('click', createManualGroup);

    // Modal close buttons
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.modal').style.display = 'none';
        });
    });

    // Chat input
    document.getElementById('send-btn').addEventListener('click', sendChatMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
}

// Load students
async function loadStudents() {
    try {
        const response = await fetch(`/api/students/available?semester=${currentSemester}`);
        allStudents = await response.json();
        displayStudents(allStudents);
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

// Display students
function displayStudents(students) {
    const grid = document.getElementById('students-grid');
    grid.innerHTML = '';

    students.forEach(student => {
        const card = document.createElement('div');
        card.className = 'student-card';
        if (student.is_grouped) {
            card.classList.add('grouped');
        }

        card.innerHTML = `
            <h3>${student.name}</h3>
            <div class="usn">${student.usn}</div>
            <div class="email">${student.email}</div>
            ${student.skills && student.skills.length > 0 ? `
                <div class="skills">
                    ${student.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
            ` : ''}
        `;

        if (!student.is_grouped) {
            card.addEventListener('click', () => toggleStudentSelection(student, card));
        }

        grid.appendChild(card);
    });
}

// Toggle student selection
function toggleStudentSelection(student, cardElement) {
    const index = selectedStudents.findIndex(s => s.id === student.id);

    if (index > -1) {
        // Deselect
        selectedStudents.splice(index, 1);
        cardElement.classList.remove('selected');
    } else {
        // Select (max 5)
        if (selectedStudents.length < 5) {
            selectedStudents.push(student);
            cardElement.classList.add('selected');
        } else {
            alert('Maximum 5 students can be selected for a group');
            return;
        }
    }

    updateSelectedPanel();
}

// Update selected students panel
function updateSelectedPanel() {
    const countEl = document.getElementById('selected-count');
    const listEl = document.getElementById('selected-list');
    const createBtn = document.getElementById('create-group-btn');

    countEl.textContent = selectedStudents.length;
    listEl.innerHTML = '';

    selectedStudents.forEach(student => {
        const item = document.createElement('div');
        item.className = 'selected-item';
        item.innerHTML = `
            <span>${student.name}</span>
            <button class="remove-btn" onclick="removeFromSelection(${student.id})">×</button>
        `;
        listEl.appendChild(item);
    });

    // Enable create button if 4-5 students selected
    createBtn.disabled = selectedStudents.length < 4 || selectedStudents.length > 5;
}

// Remove from selection
function removeFromSelection(studentId) {
    const index = selectedStudents.findIndex(s => s.id === studentId);
    if (index > -1) {
        selectedStudents.splice(index, 1);

        // Update UI
        const cards = document.querySelectorAll('.student-card');
        cards.forEach(card => {
            const cardStudent = allStudents.find(s =>
                card.querySelector('.usn').textContent === s.usn
            );
            if (cardStudent && cardStudent.id === studentId) {
                card.classList.remove('selected');
            }
        });

        updateSelectedPanel();
    }
}

// Load topics
async function loadTopics() {
    const semesters = [3, 5, 7];

    for (const sem of semesters) {
        try {
            const response = await fetch(`/api/topics?semester=${sem}`);
            const topics = await response.json();
            displayTopics(topics, sem);
        } catch (error) {
            console.error(`Error loading topics for semester ${sem}:`, error);
        }
    }

    // Also load topics for current semester in dropdown
    loadTopicsBySemester(currentSemester);
}

// Display topics
function displayTopics(topics, semester) {
    const container = document.getElementById(`topics-sem${semester}`);
    container.innerHTML = '';

    topics.forEach(topic => {
        const card = document.createElement('div');
        card.className = 'topic-card';
        card.innerHTML = `
            <span class="category">${topic.category || 'General'}</span>
            <h4>${topic.title}</h4>
            <p>${topic.description}</p>
        `;
        container.appendChild(card);
    });
}

// Load topics for dropdown
async function loadTopicsBySemester(semester) {
    try {
        const response = await fetch(`/api/topics?semester=${semester}`);
        const topics = await response.json();

        const select = document.getElementById('topic-select');
        select.innerHTML = '<option value="">Choose a topic...</option>';

        topics.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = `${topic.title} (${topic.category})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading topics:', error);
    }
}

// AI Suggestions
async function showAISuggestions() {
    const topicId = document.getElementById('topic-select').value;

    if (!topicId) {
        alert('Please select a topic first');
        return;
    }

    try {
        const response = await fetch('/api/groups/suggest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                semester: currentSemester,
                group_size: 5,
                num_groups: 3
            })
        });

        const suggestions = await response.json();
        displaySuggestions(suggestions, topicId);
    } catch (error) {
        console.error('Error getting suggestions:', error);
        alert('Error generating suggestions');
    }
}

// Display AI suggestions
function displaySuggestions(suggestions, topicId) {
    const modal = document.getElementById('suggestions-modal');
    const container = document.getElementById('suggestions-container');

    container.innerHTML = '';

    suggestions.forEach((group, index) => {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'suggestion-group';

        groupDiv.innerHTML = `
            <h4>
                Suggested Group ${index + 1}
                <span class="compatibility-score">Score: ${Math.round(group.compatibility_score)}</span>
            </h4>
            <div class="group-members">
                ${group.members.map((member, idx) => `
                    <div class="member-item ${idx === 0 ? 'leader' : ''}">
                        <div class="name">${member.name}</div>
                        <div class="role">${idx === 0 ? 'Leader' : 'Member'}</div>
                        <div class="usn">${member.usn}</div>
                    </div>
                `).join('')}
            </div>
            <button class="accept-suggestion-btn" onclick="acceptSuggestion(${index}, ${topicId})">
                Create This Group
            </button>
        `;

        container.appendChild(groupDiv);
    });

    modal.style.display = 'block';

    // Store suggestions globally
    window.currentSuggestions = suggestions;
}

// Accept AI suggestion
async function acceptSuggestion(index, topicId) {
    const group = window.currentSuggestions[index];
    const studentIds = group.members.map(m => m.id);

    try {
        const response = await fetch('/api/groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: `Group ${Date.now()}`,
                topic_id: topicId,
                semester: currentSemester,
                student_ids: studentIds
            })
        });

        const result = await response.json();

        if (result.success) {
            alert('Group created successfully!');
            document.getElementById('suggestions-modal').style.display = 'none';
            loadStudents();
            loadGroups();
        }
    } catch (error) {
        console.error('Error creating group:', error);
        alert('Error creating group');
    }
}

// Create manual group
async function createManualGroup() {
    const topicId = document.getElementById('topic-select').value;

    if (!topicId) {
        alert('Please select a topic first');
        return;
    }

    if (selectedStudents.length < 4 || selectedStudents.length > 5) {
        alert('Please select 4-5 students');
        return;
    }

    const studentIds = selectedStudents.map(s => s.id);

    try {
        const response = await fetch('/api/groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: `Group ${Date.now()}`,
                topic_id: topicId,
                semester: currentSemester,
                student_ids: studentIds
            })
        });

        const result = await response.json();

        if (result.success) {
            alert('Group created successfully!');
            selectedStudents = [];
            updateSelectedPanel();
            loadStudents();
            loadGroups();
        }
    } catch (error) {
        console.error('Error creating group:', error);
        alert('Error creating group');
    }
}

// Load groups
async function loadGroups() {
    try {
        const response = await fetch('/api/groups');
        const groups = await response.json();
        displayGroups(groups);
    } catch (error) {
        console.error('Error loading groups:', error);
    }
}

// Display groups
function displayGroups(groups) {
    const container = document.getElementById('groups-container');
    container.innerHTML = '';

    if (groups.length === 0) {
        container.innerHTML = '<p>No groups created yet.</p>';
        return;
    }

    groups.forEach(group => {
        const card = document.createElement('div');
        card.className = 'group-card';

        card.innerHTML = `
            <div class="group-header">
                <h3>${group.name || 'Unnamed Group'}</h3>
                <span class="group-topic">${group.topic_title || 'No Topic'}</span>
            </div>
            <div class="group-members">
                ${group.members.map(member => `
                    <div class="member-item ${member.role === 'leader' ? 'leader' : ''}">
                        <div class="name">${member.name}</div>
                        <div class="role">${member.role === 'leader' ? 'Leader' : 'Member'}</div>
                        <div class="usn">${member.usn}</div>
                    </div>
                `).join('')}
            </div>
        `;

        container.appendChild(card);
    });
}

// Load chat groups
async function loadChatGroups() {
    try {
        const response = await fetch('/api/groups');
        const groups = await response.json();

        const container = document.getElementById('chat-groups-list');
        container.innerHTML = '';

        groups.forEach(group => {
            const item = document.createElement('div');
            item.className = 'chat-group-item';
            item.innerHTML = `
                <strong>${group.name || 'Unnamed Group'}</strong>
                <div style="font-size: 0.9em; color: #666;">${group.topic_title}</div>
            `;

            item.addEventListener('click', () => openGroupChat(group));
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading chat groups:', error);
    }
}

// Open group chat
async function openGroupChat(group) {
    currentGroup = group;

    // Update UI
    document.querySelectorAll('.chat-group-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');

    // Update header
    document.getElementById('chat-header').innerHTML = `
        <h3>${group.name}</h3>
        <div style="font-size: 0.9em;">${group.topic_title}</div>
    `;

    // Show input
    document.getElementById('chat-input-container').style.display = 'flex';

    // Join room
    socket.emit('join_group', { group_id: group.id });

    // Load messages
    try {
        const response = await fetch(`/api/messages/${group.id}`);
        const messages = await response.json();

        const container = document.getElementById('chat-messages');
        container.innerHTML = '';

        messages.forEach(msg => appendMessage(msg));
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Append message to chat
function appendMessage(msg) {
    const container = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    messageDiv.innerHTML = `
        <div class="sender">${msg.student_name || 'Unknown'}</div>
        <div class="text">${msg.message}</div>
        <div class="time">${new Date(msg.created_at).toLocaleString()}</div>
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// Send chat message
function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message || !currentGroup) return;

    // For demo, using first student in group as sender
    const studentId = currentGroup.members[0].id;
    const usn = currentGroup.members[0].usn;

    socket.emit('send_message', {
        group_id: currentGroup.id,
        student_id: studentId,
        usn: usn,
        message: message
    });

    input.value = '';
}
