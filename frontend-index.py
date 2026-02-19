<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatterbox - Realtime Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            padding: 20px;
        }

        /* Auth Container Styles */
        .auth-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            max-width: 400px;
            margin: 0 auto;
            animation: slideUp 0.5s ease;
        }

        .auth-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .auth-header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .auth-header p {
            opacity: 0.9;
            font-size: 0.9em;
        }

        .auth-body {
            padding: 30px;
        }

        .tab-container {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }

        .tab {
            flex: 1;
            text-align: center;
            padding: 10px;
            cursor: pointer;
            color: #666;
            transition: all 0.3s;
        }

        .tab.active {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            margin-bottom: -2px;
        }

        .auth-form {
            display: none;
        }

        .auth-form.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:active {
            transform: translateY(0);
        }

        /* Chat Container Styles */
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            display: none;
            height: 80vh;
            animation: slideUp 0.5s ease;
        }

        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h2 {
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .online-users {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        .chat-main {
            display: flex;
            height: calc(100% - 130px);
        }

        .sidebar {
            width: 250px;
            background: #f8f9fa;
            border-right: 1px solid #e0e0e0;
            padding: 20px;
        }

        .sidebar h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.1em;
        }

        .users-list {
            list-style: none;
        }

        .users-list li {
            padding: 8px 10px;
            margin-bottom: 5px;
            background: white;
            border-radius: 8px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .users-list li::before {
            content: "🟢";
            font-size: 0.8em;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #f5f5f5;
        }

        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .message {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 15px;
            position: relative;
            animation: slideIn 0.3s ease;
        }

        .message.sent {
            align-self: flex-end;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .message.received {
            align-self: flex-start;
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .message-time {
            font-size: 0.7em;
            opacity: 0.7;
            margin-top: 5px;
        }

        .message.sent .message-time {
            text-align: right;
            color: rgba(255,255,255,0.8);
        }

        .message.received .message-time {
            color: #666;
        }

        .typing-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }

        .typing-area input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        .typing-area input:focus {
            outline: none;
            border-color: #667eea;
        }

        .typing-area button {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 1.2em;
            transition: transform 0.2s;
        }

        .typing-area button:hover {
            transform: scale(1.1);
        }

        .logout-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }

        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        .error-message {
            background: #ff4757;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            animation: shake 0.5s ease;
        }

        .success-message {
            background: #00d25b;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            animation: fadeIn 0.5s ease;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Auth Container -->
        <div id="authContainer" class="auth-container">
            <div class="auth-header">
                <h1>💬 Chatterbox</h1>
                <p>Connect with friends in real-time</p>
            </div>
            <div class="auth-body">
                <div class="tab-container">
                    <div class="tab active" onclick="switchTab('login')">Login</div>
                    <div class="tab" onclick="switchTab('register')">Register</div>
                </div>

                <!-- Message Container for Auth Feedback -->
                <div id="authMessage"></div>

                <!-- Login Form -->
                <div id="loginForm" class="auth-form active">
                    <form onsubmit="handleLogin(event)">
                        <div class="form-group">
                            <label>Username</label>
                            <input type="text" id="loginUsername" required>
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" id="loginPassword" required>
                        </div>
                        <button type="submit" class="btn">Login</button>
                    </form>
                </div>

                <!-- Register Form -->
                <div id="registerForm" class="auth-form">
                    <form onsubmit="handleRegister(event)">
                        <div class="form-group">
                            <label>Username</label>
                            <input type="text" id="registerUsername" required>
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" id="registerPassword" required>
                        </div>
                        <button type="submit" class="btn">Register</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Chat Container -->
        <div id="chatContainer" class="chat-container">
            <div class="chat-header">
                <h2>
                    <span>💬 Chatterbox</span>
                    <span class="online-users" id="onlineCount">0 online</span>
                </h2>
                <button class="logout-btn" onclick="logout()">Logout</button>
            </div>
            <div class="chat-main">
                <div class="sidebar">
                    <h3>Online Users</h3>
                    <ul class="users-list" id="usersList">
                        <li>Loading...</li>
                    </ul>
                </div>
                <div class="chat-area">
                    <div class="messages-container" id="messagesContainer">
                        <!-- Messages will appear here -->
                    </div>
                    <div class="typing-area">
                        <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                        <button onclick="sendMessage()">➤</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Configuration
        const API_URL = 'http://127.0.0.1:8000';
        const WS_URL = 'ws://127.0.0.1:8000/ws';
        
        // State
        let token = localStorage.getItem('chatToken');
        let username = localStorage.getItem('chatUsername');
        let websocket = null;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 5;

        // Initialize based on token
        if (token && username) {
            showChat();
            connectWebSocket();
        }

        // Tab Switching
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
            
            if (tab === 'login') {
                document.querySelector('.tab[onclick="switchTab(\'login\')"]').classList.add('active');
                document.getElementById('loginForm').classList.add('active');
            } else {
                document.querySelector('.tab[onclick="switchTab(\'register\')"]').classList.add('active');
                document.getElementById('registerForm').classList.add('active');
            }
        }

        // Show Message
        function showMessage(message, type = 'error') {
            const messageDiv = document.getElementById('authMessage');
            messageDiv.className = type === 'error' ? 'error-message' : 'success-message';
            messageDiv.textContent = message;
            
            setTimeout(() => {
                messageDiv.textContent = '';
                messageDiv.className = '';
            }, 3000);
        }

        // Handle Register
        async function handleRegister(event) {
            event.preventDefault();
            
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;

            try {
                const response = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    showMessage('Registration successful! Please login.', 'success');
                    document.getElementById('registerUsername').value = '';
                    document.getElementById('registerPassword').value = '';
                    switchTab('login');
                } else {
                    showMessage(data.detail || 'Registration failed');
                }
            } catch (error) {
                showMessage('Connection error. Please try again.');
            }
        }

        // Handle Login
        async function handleLogin(event) {
            event.preventDefault();
            
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    token = data.token;
                    localStorage.setItem('chatToken', token);
                    localStorage.setItem('chatUsername', username);
                    
                    showChat();
                    connectWebSocket();
                } else {
                    showMessage(data.detail || 'Login failed');
                }
            } catch (error) {
                showMessage('Connection error. Please try again.');
            }
        }

        // Show Chat Container
        function showChat() {
            document.getElementById('authContainer').style.display = 'none';
            document.getElementById('chatContainer').style.display = 'block';
            username = localStorage.getItem('chatUsername');
        }

        // Show Auth Container
        function showAuth() {
            document.getElementById('authContainer').style.display = 'block';
            document.getElementById('chatContainer').style.display = 'none';
        }

        // Connect WebSocket
        function connectWebSocket() {
            if (!token) return;

            const wsUrl = `${WS_URL}?token=${token}`;
            websocket = new WebSocket(wsUrl);

            websocket.onopen = () => {
                console.log('Connected to chat');
                reconnectAttempts = 0;
                addSystemMessage('Connected to chat!');
            };

            websocket.onmessage = (event) => {
                handleIncomingMessage(event.data);
            };

            websocket.onclose = () => {
                console.log('Disconnected from chat');
                if (reconnectAttempts < maxReconnectAttempts) {
                    reconnectAttempts++;
                    setTimeout(connectWebSocket, 2000);
                } else {
                    addSystemMessage('Connection lost. Please refresh the page.');
                }
            };

            websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }

        // Handle Incoming Messages
        function handleIncomingMessage(message) {
            if (message.startsWith('🟢 Online Users:')) {
                updateOnlineUsers(message);
            } else {
                addMessageToChat(message);
            }
        }

        // Update Online Users
        function updateOnlineUsers(message) {
            const usersList = document.getElementById('usersList');
            const onlineCount = document.getElementById('onlineCount');
            
            const users = message.replace('🟢 Online Users: ', '').split(', ');
            const filteredUsers = users.filter(user => user.trim() !== '');
            
            onlineCount.textContent = `${filteredUsers.length} online`;
            
            if (filteredUsers.length === 0 || (filteredUsers.length === 1 && filteredUsers[0] === '')) {
                usersList.innerHTML = '<li>No other users online</li>';
            } else {
                usersList.innerHTML = filteredUsers.map(user => 
                    `<li>${user}${user === username ? ' (you)' : ''}</li>`
                ).join('');
            }
        }

        // Add Message to Chat
        function addMessageToChat(messageText) {
            const messagesContainer = document.getElementById('messagesContainer');
            const messageDiv = document.createElement('div');
            
            // Parse message format: [HH:MM:SS] sender: message
            const match = messageText.match(/\[(.*?)\] (.*?): (.*)/);
            
            if (match) {
                const [_, time, sender, message] = match;
                const isMine = sender === 'Me' || sender === username;
                
                messageDiv.className = `message ${isMine ? 'sent' : 'received'}`;
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <strong>${sender === 'Me' ? 'You' : sender}:</strong> ${message}
                    </div>
                    <div clas
