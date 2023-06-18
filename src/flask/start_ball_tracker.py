from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/run_ball_tracker')
def run_script():
    subprocess.call(['python3', '/home/csander180/Desktop/Ball_Tracking/ball_tracking.py'])
    return 'Script executed', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)