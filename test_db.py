import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",       # or your server IP
        user="root",            # your mysql username
        password="123456",
        database="qr_attendence"       # your database name
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
