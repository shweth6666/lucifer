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
    
    print("--- User Data (flemick66) ---")
    cur.execute("SELECT username, branch, semester FROM users WHERE username='flemick66'")
    user = cur.fetchone()
    print(user)
    
    print("\n--- Timetable Sample (Monday) ---")
    cur.execute("SELECT branch, semester, day_of_week, start_time FROM timetable LIMIT 1")
    row = cur.fetchone()
    print(row)
    
    print("\n--- Checking for Wednesday specifically ---")
    cur.execute("SELECT COUNT(*) as count FROM timetable WHERE day_of_week='Wednesday'")
    print(cur.fetchone())
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
