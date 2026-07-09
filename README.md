# RRTA Pharmaceutical — Admin Management System

A full-stack pharmacy management system built with Flask, MySQL, and vanilla JS, featuring role-based access control (RBAC) at the database level. Fully containerized with Docker and automated CI/CD via GitHub Actions.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MySQL (with native RBAC — separate DB users per role, not just app-level checks)
- **Frontend:** HTML/CSS/JS (no framework)
- **DevOps:** Docker, Docker Compose, GitHub Actions CI/CD

---

## Option 1: Run with Docker (Recommended)
No need to install Python or MySQL manually — everything spins up automatically.

### Prerequisites
- Docker Desktop installed and running

### Steps
```bash
git clone https://github.com/rayanjalil4367-alt/rrta-pharmacy-management-system.git
cd rrta-pharmacy-management-system
cp .env.example .env
```
Open `.env` and fill in your passwords, then:
```bash
docker-compose up --build
```
Then open: **http://localhost:5000**

That's it. Docker automatically:
- Starts the Flask app and MySQL database as separate containers
- Loads the full database schema and data on first run
- Connects everything together

---

## Option 2: Run Locally (Manual Setup)

### 1. Clone and configure environment
```bash
git clone https://github.com/rayanjalil4367-alt/rrta-pharmacy-management-system.git
cd rrta-pharmacy-management-system
cp .env.example .env
```
Open `.env` and fill in your real MySQL password and admin passwords.

### 2. Database Setup
In MySQL Workbench or terminal:
```sql
SOURCE pharmacymanagement.sql;
SOURCE rbac.sql;
```

### 3. Python Setup
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```
Then open: **http://localhost:5000**

---

## Roles & Permissions

| Role | Permissions |
|------|-------------|
| Admin | Full CRUD on all 9 tables |
| Pharmacist | Manage customers & sales; read medicines |
| Analyst | SELECT only on 6 tables |

Login credentials are set via your local `.env` file (see `.env.example`).

---

## CI/CD
Every push to `main` triggers a GitHub Actions workflow that automatically builds the Docker image and confirms the build passes.

---

## File Structure
rrta-pharmacy-management-system/
├── app.py                        ← Flask backend (all API routes)
├── requirements.txt
├── Dockerfile                    ← Containerizes the Flask app
├── docker-compose.yml            ← Orchestrates Flask + MySQL containers
├── .env.example                  ← Template for required environment variables
├── .github/workflows/ci.yml      ← GitHub Actions CI pipeline
├── rbac.sql                      ← MySQL RBAC (CREATE USER, GRANT, REVOKE)
├── pharmacymanagement.sql        ← DB schema + data
├── static/
│   ├── css/style.css
│   └── js/shared.js
└── templates/
├── login.html
├── dashboard.html
├── medicines.html
└── manage.html

---

## Security Notes
- All secrets loaded from environment variables via `python-dotenv` — never hardcoded
- Database-level RBAC: each role maps to a real MySQL user with table-specific `GRANT` privileges (see `rbac.sql`), not just application-layer checks
- `.env` is gitignored — real credentials never reach GitHub