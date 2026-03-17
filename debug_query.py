import mysql.connector
import os

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "qr_attendence",
    "port": 3306
}

try:
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cur = conn.cursor(dictionary=True)
    
    # Simulate get_student_timetable_full for flemick66 (id 2 or 7, based on students.csv import)
    # Let's find flemick66's actual ID first
    cur.execute("SELECT id, branch, semester FROM users WHERE username='flemick66'")
    user = cur.fetchone()
    print(f"User: {user}")
    
    if user:
        student_id = user['id']
        branch = user['branch']
        semester = user['semester']
        
        # Exact query from app.py
        query = """
            SELECT t.*, s.name as subject_name, u.name as faculty_name
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.id
            LEFT JOIN users u ON t.faculty_id = u.id
            WHERE UPPER(t.branch) = UPPER(%s) AND UPPER(t.semester) = UPPER(%s)
        """
        cur.execute(query, (branch, semester))
        rows = cur.fetchall()
        print(f"Total Rows Found: {len(rows)}")
        if rows:
            print("First row:", rows[0])
            
        # Check if there are any case differences or spaces
        cur.execute("SELECT DISTINCT branch, semester FROM timetable")
        print(f"Timetable distinct: {cur.fetchall()}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
