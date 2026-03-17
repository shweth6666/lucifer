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
    
    print("--- Subjects ---")
    cur.execute("SELECT * FROM subjects")
    subjects = cur.fetchall()
    for s in subjects:
        print(s)
        
    print("\n--- Faculty ---")
    cur.execute("SELECT id, name, username FROM users WHERE role='faculty'")
    faculty = cur.fetchall()
    for f in faculty:
        print(f)
        
    print("\n--- Timetable Count ---")
    cur.execute("SELECT COUNT(*) as count FROM timetable")
    print(cur.fetchone())
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
