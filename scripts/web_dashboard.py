#!/usr/bin/env python3
"""
WEB DASHBOARD - View Your AI's Progress in Browser

Access from ANY device:
- Your Mac
- Your phone
- Any computer

Zero stress on your computer - just view in browser!
"""

from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
from src.api.ai_apis import AIAPIs
import json
from datetime import datetime

app = Flask(__name__)

# HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Self-Learning AI Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #0a0e27;
            color: #e0e0e0;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        h1 { margin: 0; font-size: 2.5em; }
        .subtitle { opacity: 0.9; margin-top: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #1a1f3a;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #2a2f4a;
        }
        .stat-label {
            color: #8b93b0;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .chat-section {
            background: #1a1f3a;
            border-radius: 10px;
            padding: 25px;
            border: 1px solid #2a2f4a;
        }
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 15px;
            background: #0f1426;
            border-radius: 8px;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 8px;
        }
        .user-message {
            background: #2a2f4a;
            margin-left: 20%;
        }
        .ai-message {
            background: #1a3a5a;
            margin-right: 20%;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #2a2f4a;
            background: #0f1426;
            color: #e0e0e0;
            font-size: 1em;
        }
        button {
            padding: 12px 30px;
            border-radius: 8px;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            cursor: pointer;
            font-size: 1em;
        }
        button:hover {
            opacity: 0.9;
        }
        .progress-log {
            background: #1a1f3a;
            border-radius: 10px;
            padding: 25px;
            margin-top: 30px;
            border: 1px solid #2a2f4a;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-entry {
            padding: 8px;
            border-bottom: 1px solid #2a2f4a;
            font-family: monospace;
            font-size: 0.9em;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4ade80;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Self-Learning AI Dashboard</h1>
        <div class="subtitle">
            <span class="status-indicator"></span>
            Your AI is learning continuously in the cloud
        </div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">Total Knowledge</div>
            <div class="stat-value" id="knowledge-count">Loading...</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Learning Status</div>
            <div class="stat-value" style="font-size: 1.5em;">Active ✅</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Last Update</div>
            <div class="stat-value" style="font-size: 1.2em;" id="last-update">Just now</div>
        </div>
    </div>

    <div class="chat-section">
        <h2>💬 Chat with Your AI</h2>
        <div class="chat-messages" id="chat-messages"></div>
        <div class="input-group">
            <input type="text" id="user-input" placeholder="Ask your AI anything..."
                   onkeypress="if(event.key=='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <div class="progress-log">
        <h3>📊 Recent Learning Activity</h3>
        <div id="activity-log">
            <div class="log-entry">System initialized - Ready to learn</div>
        </div>
    </div>

    <script>
        // Update stats
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                document.getElementById('knowledge-count').textContent =
                    data.knowledge_count.toLocaleString();
                document.getElementById('last-update').textContent =
                    new Date().toLocaleTimeString();
            } catch (e) {
                console.error('Error updating stats:', e);
            }
        }

        // Send message to AI
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            input.value = '';

            // Show thinking
            const thinkingId = addMessage('Thinking...', 'ai');

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();

                // Replace thinking with actual response
                document.getElementById(thinkingId).textContent = data.response;
            } catch (e) {
                document.getElementById(thinkingId).textContent =
                    'Error: ' + e.message;
            }
        }

        function addMessage(text, type) {
            const messages = document.getElementById('chat-messages');
            const msgDiv = document.createElement('div');
            const id = 'msg-' + Date.now();
            msgDiv.id = id;
            msgDiv.className = 'message ' + type + '-message';
            msgDiv.textContent = text;
            messages.appendChild(msgDiv);
            messages.scrollTop = messages.scrollHeight;
            return id;
        }

        // Auto-update stats every 5 seconds
        updateStats();
        setInterval(updateStats, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def get_stats():
    """Get current AI statistics"""
    try:
        memory = VectorMemory()
        knowledge_count = memory.collection.count()

        return jsonify({
            'knowledge_count': knowledge_count,
            'status': 'active',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with the AI"""
    try:
        data = request.json
        message = data.get('message', '')

        # Initialize AI
        memory = VectorMemory()
        apis = AIAPIs()

        # Search for relevant knowledge
        relevant = memory.search(message, n_results=3)
        context = "\n".join([r['text'][:200] for r in relevant]) if relevant else ""

        # Generate response with Groq
        system_prompt = f"""You are a continuously learning AI with {memory.collection.count():,} knowledge items.

Relevant knowledge:
{context}

Provide a thoughtful, intelligent response."""

        response = apis.clients['groq'].chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        ai_response = response.choices[0].message.content

        # Store conversation
        memory.add_knowledge(
            text=f"User: {message}\nAI: {ai_response}",
            source="web_chat",
            metadata={"type": "conversation", "timestamp": datetime.now().isoformat()}
        )

        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌐 WEB DASHBOARD STARTING")
    print("="*80)
    print("\nYour AI dashboard is now running!")
    print("\n📱 Access from ANY device:")
    print("   - Local: http://localhost:5000")
    print("   - In Codespace: Click the 'Ports' tab and open port 5000")
    print("   - Your phone: Use the Codespace forwarded URL")
    print("\n" + "="*80 + "\n")

    # Run on all interfaces so it's accessible from anywhere
    app.run(host='0.0.0.0', port=5000, debug=False)
