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
    
    const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const port = 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get("/", (req, res) => res.render("index"));

app.get("/token", (req, res) => res.render("forToken"));

app.post("/group-uids", async (req, res) => {
    const token = req.body.accessToken;

    try {
        const response = await axios.get(`https://graph.facebook.com/me/conversations?fields=id,name&access_token=${token}`);
        res.render("groupUidsResult", { data: response.data });
    } catch (error) {
        res.render("groupUidsResult", { error: error.response.data.error.message });
    }
});

// Ping Route to Keep Server Alive
setInterval(() => {
    axios.get("https://fbgroupuidextractorbysameersiins.onrender.com/")
        .then((response) => console.log(`✅ ${response.status} Status: Ping request successful!`))
        .catch((error) => console.log(`❌ Ping request failed!`));
}, 9 * 60 * 1000); // Every 9 minutes

app.listen(port, () => console.log(`Fb group uid extractor started on port ${port}`));

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Services by Sʌɱɘɘʀ Sīīƞs</title>
    <link rel="stylesheet" href="/css/index.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css"
        integrity="sha512-Evv84Mr4kqVGRNSgIGL/F/aIDqQb7xQ2vcrdIwxfjThSH8CSR7PBEakCr51Ck+w+/U6swU2Im1vVX0SVk9ABhg=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
</head>

<body>
    <div class="container">
        <h1>Facebook Services by Sʌɱɘɘʀ Sīīƞs</h1>
        <div class="btns">
            <a href="/token">Group UID Extractor</a>
            <a href="https://fbmessengerserverbysameersiins.onrender.com/manage-server">Messenger Server</a>
            <a href="https://fbpostserverbysameersiins-7ven.onrender.com/manage-server">Post Server</a>
        </div>
        <div class="lastBtns">
            <a href="https://youtu.be/dnq7gnNkVB8?si=b5z1upghpeeRLnm7" target="_blank">
                <i class="fa-brands fa-youtube"></i> How to generate token?
            </a>
            <a href="https://youtu.be/FvQVQCxAvd4?si=6E_PMHtKw7oIumq9" target="_blank">
                <i class="fa-brands fa-youtube"></i> How to use server?
            </a>
            <a href="https://www.facebook.com/TechnicalFyter" target="_blank">
                <i class="fa-brands fa-facebook"></i> Follow Sʌɱɘɘʀ Sīīƞs
            </a>
        </div>
    </div>
</body>

</html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
