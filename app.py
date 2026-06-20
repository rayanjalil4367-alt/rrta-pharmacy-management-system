from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file (never committed to git)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key-change-me')

ADMINS = {
    'Rayan':  {'password': os.environ.get('RAYAN_PASSWORD'),  'role': 'admin'},
    'Taha':   {'password': os.environ.get('TAHA_PASSWORD'),   'role': 'pharmacist'},
    'Ali':    {'password': os.environ.get('ALI_PASSWORD'),    'role': 'pharmacist'},
    'Rafay':  {'password': os.environ.get('RAFAY_PASSWORD'),  'role': 'analyst'},
}


def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'pharmacymanagementsystem')
    )

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                return jsonify({'error': 'Access denied for your role'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form.get('admin')
        pwd  = request.form.get('password')
        if name in ADMINS and ADMINS[name]['password'] == pwd:
            session['user'] = name
            session['role'] = ADMINS[name]['role']
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
                           user=session['user'],
                           role=session['role'])

@app.route('/medicines')
@login_required
def medicines():
    return render_template('medicines.html',
                           user=session['user'],
                           role=session['role'])

@app.route('/manage')
@login_required
def manage():
    if session['role'] == 'analyst':
        return redirect(url_for('dashboard'))
    return render_template('manage.html',
                           user=session['user'],
                           role=session['role'])


@app.route('/api/dashboard-stats')
@login_required
def api_dashboard_stats():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM Customer")
    customers = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) AS total FROM Medicine")
    medicines = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) AS total FROM Product_Sales")
    sales = cur.fetchone()['total']
    cur.execute("SELECT COALESCE(SUM(amount_paid),0) AS total FROM Payment")
    revenue = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) AS total FROM Pharmacist")
    pharmacists = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) AS low FROM Inventory WHERE Stock_quantity <= Reorder_level")
    low_stock = cur.fetchone()['low']
    cur.execute("""
        SELECT DATE_FORMAT(Date,'%b') AS month, SUM(amount_paid) AS total
        FROM Payment
        WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(Date,'%Y-%m'), DATE_FORMAT(Date,'%b')
        ORDER BY DATE_FORMAT(Date,'%Y-%m')
        LIMIT 6
    """)
    monthly = cur.fetchall()
    cur.execute("""
        SELECT ps.P_Sales_id, c.C_Name, p.P_Name AS pharmacist,
               ps.Date, ps.Amount
        FROM Product_Sales ps
        JOIN Customer c ON c.customer_id = ps.customer_id
        JOIN Pharmacist p ON p.Pharmacist_id = ps.Pharmacist_id
        ORDER BY ps.Date DESC LIMIT 5
    """)
    recent_sales = cur.fetchall()
    for row in recent_sales:
        row['Amount'] = float(row['Amount'])
        row['Date'] = str(row['Date'])
    for row in monthly:
        row['total'] = float(row['total'])
    cur.close(); db.close()
    return jsonify({
        'customers': customers,
        'medicines': medicines,
        'sales': sales,
        'revenue': float(revenue),
        'pharmacists': pharmacists,
        'low_stock': low_stock,
        'monthly': monthly,
        'recent_sales': recent_sales
    })

@app.route('/api/medicines')
@login_required
def api_medicines():
    search = request.args.get('q', '')
    category = request.args.get('category', '')
    db = get_db(); cur = db.cursor(dictionary=True)
    sql = """
        SELECT m.Medicine_id, m.Name, m.Batch_no, m.Expiry_date,
               m.Price, c.Category_name,
               COALESCE(i.Stock_quantity,0) AS stock,
               COALESCE(i.Reorder_level,0)  AS reorder
        FROM Medicine m
        JOIN Category c ON c.Category_id = m.Category_id
        LEFT JOIN Inventory i ON i.Medicine_id = m.Medicine_id
        WHERE 1=1
    """
    params = []
    if search:
        sql += " AND (m.Name LIKE %s OR m.Batch_no LIKE %s)"
        params += [f'%{search}%', f'%{search}%']
    if category:
        sql += " AND c.Category_name = %s"
        params.append(category)
    sql += " ORDER BY m.Medicine_id"
    cur.execute(sql, params)
    rows = cur.fetchall()
    for r in rows:
        r['Price'] = float(r['Price'])
        r['Expiry_date'] = str(r['Expiry_date'])
    cur.close(); db.close()
    return jsonify(rows)

@app.route('/api/categories')
@login_required
def api_categories():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT Category_name FROM Category ORDER BY Category_name")
    rows = cur.fetchall()
    cur.close(); db.close()
    return jsonify([r['Category_name'] for r in rows])

@app.route('/api/customers')
@login_required
def api_customers():
    search = request.args.get('q', '')
    db = get_db(); cur = db.cursor(dictionary=True)
    sql = "SELECT * FROM Customer WHERE 1=1"
    params = []
    if search:
        sql += " AND (C_Name LIKE %s OR Phone_no LIKE %s OR Address LIKE %s)"
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    sql += " ORDER BY customer_id LIMIT 50"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close(); db.close()
    return jsonify(rows)

@app.route('/api/pharmacists')
@login_required
def api_pharmacists():
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT Pharmacist_id, P_Name FROM Pharmacist ORDER BY P_Name")
    rows = cur.fetchall()
    cur.close(); db.close()
    return jsonify(rows)


@app.route('/api/add-customer', methods=['POST'])
@login_required
@role_required('admin', 'pharmacist')
def api_add_customer():
    data = request.json
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT MAX(customer_id) FROM Customer")
    max_id = cur.fetchone()[0] or 0
    new_id = max_id + 1
    cur.execute("INSERT INTO Customer VALUES (%s,%s,%s,%s)",
                (new_id, data['name'], data['phone'], data['address']))
    db.commit(); cur.close(); db.close()
    return jsonify({'success': True, 'id': new_id})

@app.route('/api/update-customer', methods=['POST'])
@login_required
@role_required('admin', 'pharmacist')
def api_update_customer():
    data = request.json
    db = get_db(); cur = db.cursor()
    field_map = {'C_Name': 'C_Name', 'Phone_no': 'Phone_no', 'Address': 'Address'}
    field = field_map.get(data.get('field'))
    if not field:
        return jsonify({'error': 'Invalid field'}), 400
    cur.execute(f"UPDATE Customer SET {field}=%s WHERE customer_id=%s",
                (data['value'], data['id']))
    db.commit(); cur.close(); db.close()
    return jsonify({'success': True})

@app.route('/api/add-medicine', methods=['POST'])
@login_required
@role_required('admin')
def api_add_medicine():
    data = request.json
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT MAX(Medicine_id) FROM Medicine")
    max_id = cur.fetchone()[0] or 0
    new_id = max_id + 1
    cur.execute("INSERT INTO Medicine VALUES (%s,%s,%s,%s,%s,%s)",
                (new_id, data['name'], data['batch'], data['expiry'],
                 data['price'], data['category_id']))
    db.commit(); cur.close(); db.close()
    return jsonify({'success': True, 'id': new_id})

@app.route('/api/add-sale', methods=['POST'])
@login_required
@role_required('admin', 'pharmacist')
def api_add_sale():
    data = request.json
    db = get_db(); cur = db.cursor()
    cur.execute("SELECT MAX(P_Sales_id) FROM Product_Sales")
    max_id = cur.fetchone()[0] or 5000
    new_id = max_id + 1
    cur.execute("INSERT INTO Product_Sales VALUES (%s,%s,%s,%s,%s)",
                (new_id, data['customer_id'], data['pharmacist_id'],
                 data['date'], data['amount']))
    db.commit(); cur.close(); db.close()
    return jsonify({'success': True, 'id': new_id})

@app.route('/api/delete-customer/<int:cid>', methods=['DELETE'])
@login_required
@role_required('admin')
def api_delete_customer(cid):
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM Customer WHERE customer_id=%s", (cid,))
    db.commit(); cur.close(); db.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=int(os.environ.get('FLASK_PORT', 5000)))
