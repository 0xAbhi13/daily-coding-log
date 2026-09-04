from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'subhadra-secret-key-2024'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

ADMIN_USERNAME = 'Subhadra'
ADMIN_PASSWORD = 'Subhadra@1234'

PROJECTS = [
    {
        'id': 1,
        'name': 'Subhadra Phase 1',
        'location': 'MIDC, Baramati',
        'description': 'An exclusive residential complex blending timeless architecture with modern luxury. Featuring 48 premium apartments across twin towers, Subhadra Residency redefines upscale urban living with meticulously crafted interiors, lush landscaped courts, and world-class amenities.',
        'year': 2020,
        'image': 'images/project-1.png',
        'category': 'Residential',
        'highlights': [
            'Twin 12-floor towers',
            '48 premium apartments',
            'Rooftop infinity pool',
            '24/7 concierge service',
        ]
    },
    {
        'id': 2,
        'name': 'Subhadra Phase 2',
        'location': 'Rui, Baramati',
        'description': 'A breathtaking villa development set against the serene backdrop of Maharashtra\'s heritage coast. Six standalone villas with private pools, bespoke interiors, and expansive ocean views — each a statement of refined living for the discerning few.',
        'year': 2023,
        'image': 'images/project-2.png',
        'category': 'Residential',
        'highlights': [
            '6 standalone villas',
            'Private pools',
            'Ocean-view terraces',
            'Smart home automation',
        ]
    },
    {
        'id': 3,
        'name': 'Subhadra Phase 3',
        'location': 'Dashrathnagar, MIDC, Baramati',
        'description': 'A landmark commercial tower that commands the city skyline. Designed for enterprise-grade tenants, the Elite Commercial Hub offers 20 floors of premium Grade-A office spaces with state-of-the-art infrastructure, panoramic views, and an iconic façade.',
        'year': 2026,
        'image': 'images/project-3.jpeg',
        'category': 'Residential',
        'highlights': [
            'Apartment Building with 5 floors',
            'Grade-A offices',
            '24/7 security and maintenance',
            'lift access to all floors',
        ]
    },
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS)


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, phone, email, message]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400

        conn = get_db()
        conn.execute(
            'INSERT INTO contacts (name, phone, email, message) VALUES (?, ?, ?, ?)',
            (name, phone, email, message)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Thank you! We will be in touch shortly.'})

    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = get_db()
    contacts = conn.execute(
        'SELECT * FROM contacts ORDER BY created_at DESC'
    ).fetchall()
    total = conn.execute('SELECT COUNT(*) FROM contacts').fetchone()[0]
    conn.close()

    return render_template('admin.html', contacts=contacts, total=total, projects=PROJECTS)


if __name__ == '__main__':
    init_db()
    print('\n  Subhadra Construction is running!')
    print('  Open http://localhost:5000 in your browser\n')
    app.run(debug=True, port=5000)
