"""IR Flows agency website. Run with python app.py."""
import os
import re
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
DATABASE = Path(os.environ.get('IRFLOWS_DATABASE', 'instance/inquiries.sqlite3'))

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/team')
def team():
    return render_template('content.html', page='team')

@app.get('/blog')
def blog():
    return render_template('content.html', page='blog')

@app.post('/api/inquiries')
def inquiry():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify(error='Please submit a valid inquiry.'), 400
    fields = {key: str(data.get(key, '')).strip() for key in ('name', 'email', 'company', 'service', 'message')}
    if data.get('website'):
        return jsonify(message='Your inquiry has been received.'), 200
    if not fields['name'] or len(fields['name']) > 120:
        return jsonify(error='Please enter your name (up to 120 characters).'), 400
    if len(fields['email']) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', fields['email']):
        return jsonify(error='Please enter a valid email address.'), 400
    if len(fields['message']) < 10 or len(fields['message']) > 4000:
        return jsonify(error='Tell us a little about your project (10–4,000 characters).'), 400
    if len(fields['company']) > 160 or fields['service'] not in ('Workflow automation', 'AI assistants', 'CRM & integrations', 'Not sure yet'):
        return jsonify(error='Please check your company and service details.'), 400
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE) as db:
        db.execute('CREATE TABLE IF NOT EXISTS inquiries (id INTEGER PRIMARY KEY, name TEXT, email TEXT, company TEXT, service TEXT, message TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
        db.execute('INSERT INTO inquiries (name, email, company, service, message) VALUES (?, ?, ?, ?, ?)', tuple(fields.values()))
    return jsonify(message='Your inquiry has been received. Thank you for sharing your project.'), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
