from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import time

app = Flask(__name__)

DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'tododb')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')  # high / medium / low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_tables():
    retries = 5
    while retries > 0:
        try:
            with app.app_context():
                db.create_all()
            print("Database tables created successfully!")
            break
        except Exception as e:
            retries -= 1
            print(f"DB not ready, retrying... ({retries} left): {e}")
            time.sleep(3)

create_tables()

@app.route('/')
def index():
    filter_priority = request.args.get('priority', 'all')
    if filter_priority == 'all':
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
    else:
        todos = Todo.query.filter_by(priority=filter_priority).order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos, filter_priority=filter_priority)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'medium')
    if title:
        todo = Todo(title=title, priority=priority)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
