from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# --- MODULE 1: AI CODE AUDITOR ---
def analyze_code(code):
    findings = []
    # Patterns to detect common hacks in code
    rules = {
        "🔴 SQL Injection Risk": r"SELECT.*FROM.*WHERE.*=.*['\"] \+ .*",
        "🟠 XSS Vulnerability": r"(innerHTML|document\.write|eval\()",
        "🚫 Hardcoded Secret/Key": r"(api_key|secret|password)\s*=\s*['\"].*?['\"]",
        "⚠️ Insecure OS Command": r"(os\.system|subprocess\.call)\("
    }
    for issue, pattern in rules.items():
        if re.search(pattern, code, re.IGNORECASE):
            findings.append(issue)
    return findings if findings else ["✅ Code logic looks secure."]

# --- MODULE 2: BOT-SLAYER ---
@app.route('/detect-bot', methods=['POST'])
def detect_bot():
    data = request.json
    movements = data.get('movements', [])
    # Logic: If no mouse movement is recorded, it's a script.
    if len(movements) < 10:
        return jsonify({"status": "BOT DETECTED! 🤖", "color": "red", "details": "No Mouse Entropy Found."})
    else:
        return jsonify({"status": "HUMAN VERIFIED 👤", "color": "green", "details": "Natural Behavior Pattern Confirmed."})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit():
    code = request.form.get('code_input')
    results = analyze_code(code)
    return render_template('index.html', audit_results=results, original_code=code)

if __name__ == '__main__':
    app.run(debug=True)