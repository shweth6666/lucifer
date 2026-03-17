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
    
    print("--- Subjects Table ---")
    cur.execute("SELECT * FROM subjects")
    for s in cur.fetchall():
        print(s)
        
    print("\n--- Timetable with Subject Join Test ---")
    cur.execute("""
        SELECT t.day_of_week, s.name as subject_name
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.id
        WHERE UPPER(t.branch) = 'CSE' AND UPPER(t.semester) = 'S6'
        LIMIT 5
    """)
    for row in cur.fetchall():
        print(row)
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
