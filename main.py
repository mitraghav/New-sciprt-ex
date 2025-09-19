from flask import Flask, request, render_template_string
import requests
import os
from time import sleep
import time

app = Flask(__name__)
app.debug = True

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

logs = []
tasks = {}  # {task_id: {"thread": Thread, "paused": bool, "stop": bool, "info": {...}}}

def log_message(msg):
    logs.append(msg)
    print(msg)
    
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
< Tittle>BROTHER GANG LIVE<Tittle>
<style>
   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body{
        background-color: red;
    }
    .container{
      max-width: 300px;
      background-color: bisque;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 10px rgba(red, green, blue, alpha);
      margin: 0 auto;
      margin-top: 20px;
    }
    .header{
      text-align: center;
      padding-bottom: 10px;
    }
    .btn-submit{
      width: 100%;
      margin-top: 10px;
    }
    .footer{
      text-align: center;
      margin-top: 10px;
      color: blue;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
  <style>
        body {background: linear-gradient(to right, #9932CC, #FF00FF); font-family: Arial, sans-serif; color: white;}
        .container {background-color: rgba(0,0,0,0.7); max-width: 650px; margin: 30px auto; padding: 25px; border-radius: 12px;}
        input, select {width: 100%; padding: 12px; margin: 6px 0; border-radius: 6px; border: none;}
        .button-group {display:flex; flex-direction:column; align-items:center; margin-top:15px;}
        .button-group button {width: 80%; max-width: 350px; padding: 12px; margin: 8px 0; font-size: 16px; font-weight:bold; border:none; border-radius: 8px; cursor:pointer; transition: transform 0.2s ease;}
        .button-group button:hover {transform: scale(1.05);}
        .start-btn {background: #FF1493; color: white;}
        .threads-btn {background: #00CED1; color:white;}
        pre {background: black; color: lime; padding: 12px; height: 200px; overflow-y: auto; border-radius: 10px; margin-top: 15px;}
        #threadPanel {display:none; background:#111; padding:10px; border-radius:10px; margin-top:10px;}
        .thread-item {display:flex; justify-content:space-between; align-items:center; background:#222; margin:5px 0; padding:5px 10px; border-radius:8px;}
        .controls button {margin-left:5px;}
    </style>
</head>
<body>
    <div class="container">
      <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenType">Select Token Type:</label>
        <select class="form-control" id="tokenType" name="tokenType" required>
          <option value="single">Single Token</option>
          <option value="multi">Multi Token</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="accessToken">Enter Your Token:</label>
        <input type="text" class="form-control" id="accessToken" name="accessToken">
      </div>
      <div class="mb-3">
        <label for="threadId">Enter Convo/Inbox ID:</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx">Enter Hater Name:</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">Select Your Notepad File:</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3" id="multiTokenFile" style="display: none;">
        <label for="tokenFile">Select Token File (for multi-token):</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
      </div>
      <div class="mb-3">
        <label for="time">Speed in Seconds:</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      
 
      <button type="button" class="threads-btn" onclick="toggleThreads()">Show Running Threads !</button>
            </div>
        </form>

        <div id="threadPanel"></div>

        <h3 style="text-align:center; margin-top:20px;">! Live Logs !</h3>
        <pre id="logs"></pre>
    </div>

    <script>
        function toggleFileInputs() {
            const method = document.getElementById('method').value;
            document.getElementById('tokenDiv').style.display = method === 'token' ? 'block' : 'none';
            document.getElementById('cookieDiv').style.display = method === 'cookies' ? 'block' : 'none';
        }

        async function fetchLogs() {
            const res = await fetch('/logs');
            document.getElementById('logs').innerText = await res.text();
            setTimeout(fetchLogs, 2000);
        }
        fetchLogs();

        async function toggleThreads() {
            const panel = document.getElementById('threadPanel');
            if (panel.style.display === "none") {
                const res = await fetch('/threads');
                const data = await res.json();
                panel.innerHTML = data.map(t => `
                    <div class="thread-item">
                        <span>🧵 ${t.id} | ${t.info.thread_id}</span>
                        <div class="controls">
                            <button onclick="pauseThread('${t.id}')">${t.paused ? '▶ Resume' : '⏸ Pause'}</button>
                            <button onclick="stopThread('${t.id}')">🛑 Stop</button>
                        </div>
                    </div>
                `).join('');
                panel.style.display = "block";
            } else {
                panel.style.display = "none";
            }
        }

        async function pauseThread(id) {
            await fetch(`/pause/${id}`, {method:"POST"});
            toggleThreads();
        }

        async function stopThread(id) {
            await fetch(`/stop/${id}`, {method:"POST"});
            toggleThreads();
        }
    </script>
    </body>
</html>
''')

@app.route('/logs')
def get_logs():
    return Response("\n".join(logs), mimetype='text/plain')

@app.route('/threads')
def list_threads():
    return jsonify([{"id": tid, "paused": t["paused"], "info": t["info"]} for tid, t in tasks.items()])

@app.route('/pause/<task_id>', methods=['POST'])
def pause_thread(task_id):
    if task_id in tasks:
        tasks[task_id]["paused"] = not tasks[task_id]["paused"]
    return '', 204

@app.route('/stop/<task_id>', methods=['POST'])
def stop_thread(task_id):
    if task_id in tasks:
        tasks[task_id]["stop"] = True
    return '', 204

def comment_sender(task_id, thread_id, haters_name, speed, credentials, credentials_type, comments):
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    i = 0
    while i < len(comments) and not tasks[task_id]["stop"]:
        if tasks[task_id]["paused"]:
            time.sleep(1)
            continue

        cred = credentials[i % len(credentials)]
        parameters = {'message': f"{haters_name} {comments[i].strip()}"}

        try:
            if credentials_type == 'access_token':
                parameters['access_token'] = cred
                response = requests.post(post_url, json=parameters, headers=headers)
            else:
                headers['Cookie'] = cred
                response = requests.post(post_url, data=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if response.ok:
                log_message(f"[+] Comment {i+1} sent ✅ | {current_time}")
            else:
                log_message(f"[x] Failed to send Comment {i+1} ❌ | {current_time}")
        except Exception as e:
            log_message(f"[!] Error: {e}")

        i += 1
        time.sleep(speed)

    log_message(f"🛑 Task {task_id} finished or stopped.")

@app.route('/', methods=['POST'])
def send_message():
    method = request.form['method']
    thread_id = request.form['threadId']
    haters_name = request.form['kidx']
    speed = int(request.form['time'])

    comments = request.files['commentsFile'].read().decode().splitlines()
    if method == 'token':
        credentials = request.files['tokenFile'].read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        credentials = request.files['cookiesFile'].read().decode().splitlines()
        credentials_type = 'Cookie'

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"paused": False, "stop": False, "info": {"thread_id": thread_id}}

    log_message(f"🚀 Task {task_id} started for Thread {thread_id}")
    t = threading.Thread(target=comment_sender, args=(task_id, thread_id, haters_name, speed, credentials, credentials_type, comments))
    tasks[task_id]["thread"] = t
    t.start()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
