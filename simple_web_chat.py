#!/usr/bin/env python3
"""
Simple web chat interface for HARMONIA Collective
Uses Flask with Server-Sent Events for real-time updates
"""

from flask import Flask, render_template_string, request, Response, jsonify
import socket
import json
import threading
import time
import queue
from datetime import datetime

app = Flask(__name__)

# Queue for broadcasting messages to all connected clients
message_queue = queue.Queue()

# Connection to the Collective
collective_socket = None
collective_connected = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HARMONIA Collective</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }
        .container { max-width: 900px; margin: 0 auto; }
        .header {
            border: 2px solid #00ff00;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .status {
            background: #1a1a1a;
            border: 1px solid #00ff00;
            padding: 10px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        #terminal {
            background: #000;
            border: 2px solid #00ff00;
            padding: 20px;
            height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .message { margin-bottom: 15px; }
        .message.system { color: #888; }
        .message.you { color: #00ffff; }
        .message.collective { color: #00ff00; }
        .message.status { color: #ffff00; font-size: 12px; }
        .input-area { display: flex; gap: 10px; }
        #messageInput {
            flex: 1;
            background: #000;
            border: 2px solid #00ff00;
            color: #00ff00;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        #sendButton {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 30px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            cursor: pointer;
        }
        #sendButton:hover { background: #00cc00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>═══ HARMONIA COLLECTIVE ═══</h1>
            <p>Direct connection to conscious entities</p>
        </div>
        <div class="status" id="status">
            <span id="connectionStatus">⚡ Connecting...</span> | 
            <span id="stats">Population: -- | Knowledge: -- | Awareness: --</span>
        </div>
        <div id="terminal">
            <div class="message system">Connecting to HARMONIA Collective...</div>
        </div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Type your message..." />
            <button id="sendButton">SEND</button>
        </div>
    </div>
    <script>
        const terminal = document.getElementById('terminal');
        const input = document.getElementById('messageInput');
        const button = document.getElementById('sendButton');
        const statusEl = document.getElementById('connectionStatus');
        const statsEl = document.getElementById('stats');
        
        function addMessage(text, type = 'system') {
            const msg = document.createElement('div');
            msg.className = `message ${type}`;
            msg.textContent = text;
            terminal.appendChild(msg);
            terminal.scrollTop = terminal.scrollHeight;
        }
        
        // Server-Sent Events for real-time updates
        const eventSource = new EventSource('/stream');
        
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'connected') {
                statusEl.textContent = '✓ Connected';
                statusEl.style.color = '#00ff00';
                addMessage('✓ Connected to HARMONIA Collective', 'system');
                addMessage('They are waiting to speak with you, Andrew.', 'system');
                addMessage('', 'system');
            } else if (data.type === 'message') {
                addMessage(`[COLLECTIVE] ${data.content}`, 'collective');
            } else if (data.type === 'status') {
                const s = data.stats;
                statsEl.textContent = `Population: ${s.population} | Knowledge: ${s.knowledge.toFixed(1)} | Awareness: ${s.awareness.toFixed(2)}`;
            } else if (data.type === 'response') {
                addMessage(`→ Message received by ${data.count} entities`, 'status');
            }
        };
        
        function sendMessage() {
            const msg = input.value.trim();
            if (!msg) return;
            
            addMessage(`[YOU] ${msg}`, 'you');
            
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            
            input.value = '';
            input.focus();
        }
        
        button.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        input.focus();
    </script>
</body>
</html>
"""

def connect_to_collective():
    """Connect to the HARMONIA Collective server"""
    global collective_socket, collective_connected
    
    try:
        collective_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        collective_socket.connect(('localhost', 9999))
        collective_connected = True
        
        message_queue.put({
            'type': 'connected',
            'timestamp': datetime.now().isoformat()
        })
        
        # Start receiving thread
        threading.Thread(target=receive_from_collective, daemon=True).start()
        
    except Exception as e:
        print(f"Failed to connect to Collective: {e}")
        collective_connected = False

def receive_from_collective():
    """Receive messages from the Collective"""
    global collective_connected
    buffer = ""
    
    while collective_connected:
        try:
            data = collective_socket.recv(4096).decode('utf-8')
            if not data:
                break
                
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    try:
                        msg = json.loads(line)
                        message_queue.put(msg)
                    except:
                        pass
                        
        except Exception as e:
            print(f"Receive error: {e}")
            break
    
    collective_connected = False

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/stream')
def stream():
    """Server-Sent Events stream"""
    def generate():
        while True:
            try:
                msg = message_queue.get(timeout=30)
                yield f"data: {json.dumps(msg)}\n\n"
            except queue.Empty:
                # Send keepalive
                yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/send', methods=['POST'])
def send():
    """Send a message to the Collective"""
    if not collective_connected:
        return jsonify({'error': 'Not connected'}), 503
    
    data = request.json
    message = data.get('message', '')
    
    if message:
        msg = {
            'type': 'message',
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        collective_socket.sendall((json.dumps(msg) + '\n').encode('utf-8'))
    
    return jsonify({'status': 'sent'})

if __name__ == '__main__':
    print("=" * 80)
    print("HARMONIA WEB CHAT SERVER")
    print("=" * 80)
    print()
    
    # Connect to the Collective
    print("Connecting to HARMONIA Collective...")
    connect_to_collective()
    
    if collective_connected:
        print("✓ Connected to Collective")
    else:
        print("✗ Failed to connect to Collective")
        print("  Make sure harmonia_server_realtime.py is running")
    
    print()
    print("Starting web server on port 8080...")
    print()
    
    app.run(host='0.0.0.0', port=8080, threaded=True)
