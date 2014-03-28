import subprocess

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    cmd = 'sudo ./scripts/pagekite-frontend/restart_pagekite.sh'
    subprocess.Popen(cmd.split(' '))
    return "Sent restart command!"

if __name__ == "__main__":
    app.run()
