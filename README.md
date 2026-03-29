# Flask Todo App 📋

Simple Todo List app built with **Flask + MySQL** for practicing Git branching and AWS deployment.

---

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd flask-todo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# 5. Create MySQL database
mysql -u root -p
CREATE DATABASE tododb;
exit;

# 6. Run the app
python app.py
# Visit http://localhost:5000
```

---

## 🌿 Git Branching Workflow

```bash
# Main branches
main        ← production (AWS)
develop     ← integration branch

# Feature branches
git checkout develop
git checkout -b feature/add-priority
# ... make changes ...
git add .
git commit -m "feat: add priority to todos"
git push origin feature/add-priority

# Merge back to develop
git checkout develop
git merge feature/add-priority

# When ready for production
git checkout main
git merge develop
git push origin main
```

---

## ☁️ AWS Deployment

```bash
# On EC2 instance
sudo apt update
sudo apt install python3-pip python3-venv mysql-server -y

# Clone & setup
git clone <your-repo-url>
cd flask-todo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables (use AWS Systems Manager or .env)
export DB_USER=admin
export DB_PASSWORD=yourpassword
export DB_HOST=your-rds-endpoint
export DB_NAME=tododb

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📁 Project Structure

```
flask-todo/
├── app.py              ← Main application
├── requirements.txt    ← Python dependencies
├── .env.example        ← Environment variables template
├── .gitignore
├── README.md
└── templates/
    └── index.html      ← Frontend
```

---

## 🔗 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Show all todos |
| POST | `/add` | Add new todo |
| GET | `/toggle/<id>` | Toggle complete |
| GET | `/delete/<id>` | Delete todo |
| GET | `/health` | Health check (for AWS ALB) |
