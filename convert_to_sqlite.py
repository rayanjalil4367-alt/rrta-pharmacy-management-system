"""
convert_to_sqlite.py
---------------------
Converts your MySQL pharmacymanagement.sql dump into a SQLite database file
that you can upload to Kaggle for the NL2SQL project.

HOW TO USE:
1. Put this script in the SAME folder as your pharmacymanagement.sql file
2. Open a terminal in that folder
3. Run:  python convert_to_sqlite.py
4. It will create a file called pharmacymanagement.sqlite in the same folder
5. Upload that .sqlite file to Kaggle as a Dataset (instructions given separately)

WHAT IT DOES:
- Removes MySQL-only commands SQLite doesn't understand (CREATE DATABASE, USE)
- Converts AUTO_INCREMENT -> works automatically as INTEGER PRIMARY KEY in SQLite
- Removes ENGINE=InnoDB (not a SQLite concept)
- Creates all your tables and inserts all your data into a real SQLite database
"""

import sqlite3
import re
import os

SOURCE_FILE = "pharmacymanagement.sql"
OUTPUT_FILE = "pharmacymanagement.sqlite"

def clean_sql_for_sqlite(sql_text):
    # Remove CREATE DATABASE and USE statements (SQLite doesn't have these)
    sql_text = re.sub(r'CREATE DATABASE.*?;', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'USE\s+\w+\s*;', '', sql_text, flags=re.IGNORECASE)

    # Remove ENGINE=InnoDB and similar MySQL table options if present
    sql_text = re.sub(r'ENGINE\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'DEFAULT CHARSET\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)

    # AUTO_INCREMENT -> SQLite auto-increments any INTEGER PRIMARY KEY automatically,
    # so we just remove the keyword (SQLite doesn't need it for basic use)
    sql_text = re.sub(r'\s+AUTO_INCREMENT', '', sql_text, flags=re.IGNORECASE)

    # Remove any trailing analysis/demo queries (SELECT/UPDATE/DELETE/transactions)
    # that are not part of the core schema+data — we only want CREATE TABLE and INSERT
    # This keeps the SQLite file clean and focused on structure + data
    statements = sql_text.split(';')
    keep_statements = []
    for stmt in statements:
        stripped = stmt.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        if upper.startswith('CREATE TABLE') or upper.startswith('INSERT INTO'):
            keep_statements.append(stmt)
    return keep_statements


def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"ERROR: Could not find '{SOURCE_FILE}' in this folder.")
        print("Make sure this script is in the same folder as your pharmacymanagement.sql file.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        sql_text = f.read()

    statements = clean_sql_for_sqlite(sql_text)

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)  # start fresh each time

    conn = sqlite3.connect(OUTPUT_FILE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    success_count = 0
    error_count = 0

    for stmt in statements:
        try:
            cur.execute(stmt)
            success_count += 1
        except sqlite3.Error as e:
            error_count += 1
            print(f"Skipped a statement due to error: {e}")
            print(f"Statement was: {stmt[:100]}...")

    conn.commit()

    # Verify: list tables and row counts
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]

    print("\n--- CONVERSION COMPLETE ---")
    print(f"Successful statements: {success_count}")
    print(f"Failed statements: {error_count}")
    print(f"\nTables created: {tables}")

    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        count = cur.fetchone()[0]
        print(f"  {table}: {count} rows")

    conn.close()
    print(f"\nDone! Your SQLite database is saved as: {OUTPUT_FILE}")
    print("Next step: upload this file to Kaggle as a Dataset.")


if __name__ == "__main__":
    main()
