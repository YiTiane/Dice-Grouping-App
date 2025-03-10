from flask import Flask, render_template, request, redirect, url_for, flash
import random
import os
import time
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

COOLDOWN_DAYS = 7
COOLDOWN_FILE = "cooldown.txt"
RESULTS_FILE = "results.json"

def get_cooldown():
    if os.path.exists(COOLDOWN_FILE):
        with open(COOLDOWN_FILE, "r") as f:
            timestamp = f.read().strip()
            if timestamp:
                last_time = datetime.fromtimestamp(float(timestamp))
                if datetime.now() - last_time < timedelta(days=COOLDOWN_DAYS):
                    return False, (last_time + timedelta(days=COOLDOWN_DAYS) - datetime.now())
    return True, None

def set_cooldown():
    with open(COOLDOWN_FILE, "w") as f:
        f.write(str(time.time()))

def save_results(results, groups):
    with open(RESULTS_FILE, "w") as f:
        json.dump({"results": results, "groups": groups}, f)

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            return json.load(f)
    return {"results": None, "groups": None}

@app.route('/', methods=['GET', 'POST'])
def index():
    can_generate, cooldown_remaining = get_cooldown()
    stored_data = load_results()
    results, groups = stored_data.get("results"), stored_data.get("groups")

    if request.method == 'POST' and can_generate:
        names = request.form.get("names").split(',')
        names = [name.strip() for name in names if name.strip()]

        if len(names) < 2:
            flash('请输入至少两个名字！', 'danger')
            return redirect(url_for('index'))

        results = []
        for name in names:
            rolls = [random.randint(1, 6) for _ in range(30)]
            avg = sum(rolls) / len(rolls)
            results.append((name, avg, rolls))

        results.sort(key=lambda x: x[1])
        groups = [results[i:i+2] for i in range(0, len(results), 2)]

        set_cooldown()
        save_results(results, groups)
        can_generate, cooldown_remaining = get_cooldown()

    return render_template('index.html', can_generate=can_generate, cooldown_remaining=cooldown_remaining, results=results, groups=groups)

if __name__ == '__main__':
    app.run(debug=True)
