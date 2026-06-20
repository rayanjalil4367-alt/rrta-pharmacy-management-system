# RRTA Pharmaceutical — Admin Management System

A full-stack pharmacy management system built with Flask, MySQL, and vanilla JS, featuring role-based access control (RBAC) at the database level.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MySQL (with native RBAC — separate DB users per role, not just app-level checks)
- **Frontend:** HTML/CSS/JS (no framework)

## Setup & Run Guide

### 1. Clone and configure environment
```bash
git clone https://github.com/rayanjalil4367-alt/rrta-pharmacy-management.git
cd rrta-pharmacy-management
cp .env.example .env
```
Open `.env` and fill in your real MySQL password and choose your own admin login passwords.

### 2. Database Setup
In MySQL Workbench or terminal:
```sql
SOURCE pharmacymanagement.sql;   -- creates DB + inserts all data
SOURCE rbac.sql;                  -- creates all 4 MySQL users + grants
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

| Role        | Permissions |
|-------------|-------------|
| Admin       | Full CRUD on all 9 tables |
| Pharmacist  | Manage customers & sales; read medicines |
| Analyst     | SELECT only on 6 tables |

Login credentials are set via your local `.env` file (see `.env.example` for the variable names). This keeps real passwords out of git history.

---

## File Structure
```
rrta_pharma/
├── app.py                   ← Flask backend (all API routes)
├── requirements.txt
├── .env.example             ← Template for required environment variables
├── rbac.sql                 ← MySQL RBAC (CREATE USER, GRANT, REVOKE, FLUSH)
├── pharmacymanagement.sql   ← Original DB schema + data
├── static/
│   ├── css/style.css        ← Shared stylesheet
│   └── js/shared.js         ← Shared JS (canvas, toast, API helper)
└── templates/
    ├── login.html           ← Admin login with role selector
    ├── dashboard.html       ← KPI dashboard + charts + inventory
    ├── medicines.html       ← Medicine catalogue (search + filter)
    └── manage.html          ← Add/Update/Delete records + RBAC SQL view
```

## Pages Overview
- **/** → redirects to login or dashboard
- **/login** → select admin, enter password
- **/dashboard** → KPIs, monthly revenue chart, recent sales, inventory snapshot
- **/medicines** → full medicine catalogue with grid/table view, search, category & stock filters
- **/manage** → add customer, view/edit/delete customers, add sale, add medicine (admin only), RBAC SQL panel

## Security Notes
- All secrets (DB password, admin passwords, Flask secret key) are loaded from environment variables via `python-dotenv`, never hardcoded.
- Database-level RBAC: each role maps to a real MySQL user with table-specific `GRANT` privileges (see `rbac.sql`), not just application-layer checks.
