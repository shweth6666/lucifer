import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "123456"),
        database=os.getenv("MYSQL_DATABASE", "qr_attendence"),
        port=int(os.getenv("MYSQL_PORT", 3306))
    )

    print("Connected successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")

    for row in cursor:
        print(row)

except mysql.connector.Error as err:
    print("Error:", err)

finally:
    if 'conn' in locals() and conn.is_connected():
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        conn.close()
        print("Connection closed")
