import mysql.connector
import os

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "qr_attendence",
    "port": 3306
}

def seed_timetable():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cur = conn.cursor(dictionary=True)

        branch = "CSE"
        semester = "S6"

        # 1. Add all subjects from the timetable image
        subjects_to_add = [
            ("CST302", "COMPILER DESIGN"),
            ("CST304", "COMPUTER GRAPHICS AND IMAGE PROCESSING"),
            ("CST306", "ALGORITHM ANALYSIS AND DESIGN"),
            ("CST322", "DATA ANALYTICS"),
            ("HUT300", "INDUSTRIAL ECONOMICS AND FOREIGN TRADE"),
            ("CST308", "COMPREHENSIVE COURSE WORK"),
            ("CSL 332", "NETWORKING LAB"),
            ("CSD334", "MINIPROJECT"),
            ("BREAK", "Interval"),
            ("LUNCH", "Lunch Break")
        ]

        for code, name in subjects_to_add:
            cur.execute("SELECT id FROM subjects WHERE code=%s", (code,))
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO subjects (code, name, branch, semester) VALUES (%s, %s, %s, %s)",
                    (code, name, branch, semester)
                )
        conn.commit()

        # 2. Get mappings for subjects and faculty
        cur.execute("SELECT id, name, code FROM subjects")
        subj_map = {row['name']: row['id'] for row in cur.fetchall()}
        
        # Mapping abbreviations/shorthand to full names used in DB
        name_map = {
            "CD": "COMPILER DESIGN",
            "RS": "ranjith",
            "CG": "COMPUTER GRAPHICS AND IMAGE PROCESSING",
            "CJ": "cinu",
            "AAD": "ALGORITHM ANALYSIS AND DESIGN",
            "SKI": "sisira",
            "DA": "DATA ANALYTICS",
            "AAK": "anjitha",
            "IEFT": "INDUSTRIAL ECONOMICS AND FOREIGN TRADE",
            "LK": "lekha",
            "COMPRE": "COMPREHENSIVE COURSE WORK",
            "VM": "visakh",
            "N/W LAB": "NETWORKING LAB",
            "MINI PROJECT": "MINIPROJECT",
            "INTERVAL": "Interval",
            "LUNCH": "Lunch Break"
        }

        cur.execute("SELECT id, username FROM users WHERE role='faculty'")
        faculty_map = {row['username'].lower(): row['id'] for row in cur.fetchall()}

        # 3. Time slots
        slots = {
            1: ("09:00", "10:00"),
            2: ("10:00", "11:00"),
            "BREAK1": ("11:00", "11:10"),
            3: ("11:10", "12:10"),
            "LUNCH": ("12:10", "12:50"),
            4: ("12:50", "13:50"),
            "BREAK2": ("13:50", "14:00"),
            5: ("14:00", "15:00"),
            6: ("15:00", "16:00")
        }

        # 4. Timetable data [Day, Hour, SubName(Short), FacultyUsername(Short)]
        timetable_data = [
            # Monday
            ("Monday", 1, "IEFT", "LK"), ("Monday", 2, "CD", "RS"), ("Monday", "BREAK1", "INTERVAL", None),
            ("Monday", 3, "AAD", "SKI"), ("Monday", "LUNCH", "LUNCH", None),
            ("Monday", 4, "DA", "AAK"), ("Monday", "BREAK2", "INTERVAL", None),
            ("Monday", 5, "COMPRE", "VM"), ("Monday", 6, "CG", "CJ"),
            
            # Tuesday
            ("Tuesday", 1, "AAD", "SKI"), ("Tuesday", 2, "CG", "CJ"), ("Tuesday", "BREAK1", "INTERVAL", None),
            ("Tuesday", 3, "DA", "AAK"), ("Tuesday", "LUNCH", "LUNCH", None),
            ("Tuesday", 4, "N/W LAB", "SKI"), ("Tuesday", "BREAK2", "INTERVAL", None),
            ("Tuesday", 5, "N/W LAB", "SKI"), ("Tuesday", 6, "N/W LAB", "SKI"),

            # Wednesday
            ("Wednesday", 1, "CD", "RS"), ("Wednesday", 2, "CG", "CJ"), ("Wednesday", "BREAK1", "INTERVAL", None),
            ("Wednesday", 3, "AAD", "SKI"), ("Wednesday", "LUNCH", "LUNCH", None),
            ("Wednesday", 4, "IEFT", "LK"), ("Wednesday", "BREAK2", "INTERVAL", None),
            ("Wednesday", 5, "CD", "RS"), ("Wednesday", 6, "MINI PROJECT", "AAK"),

            # Thursday
            ("Thursday", 1, "CG", "CJ"), ("Thursday", 2, "AAD", "SKI"), ("Thursday", "BREAK1", "INTERVAL", None),
            ("Thursday", 3, "IEFT", "LK"), ("Thursday", "LUNCH", "LUNCH", None),
            ("Thursday", 4, "CD", "RS"), ("Thursday", "BREAK2", "INTERVAL", None),
            ("Thursday", 5, "CG", "CJ"), ("Thursday", 6, "AAD", "SKI"),

            # Friday
            ("Friday", 1, "CD", "RS"), ("Friday", 2, "COMPRE", "VM"), ("Friday", "BREAK1", "INTERVAL", None),
            ("Friday", 3, "DA", "AAK"), ("Friday", "LUNCH", "LUNCH", None),
            ("Friday", 4, "MINI PROJECT", "AAK"), ("Friday", "BREAK2", "INTERVAL", None),
            ("Friday", 5, "MINI PROJECT", "AAK"), ("Friday", 6, "MINI PROJECT", "AAK"),

            # Saturday
            ("Saturday", 1, "CG", "CJ"), ("Saturday", 2, "IEFT", "LK"), ("Saturday", "BREAK1", "INTERVAL", None),
            ("Saturday", 3, "CD", "RS"), ("Saturday", "LUNCH", "LUNCH", None),
            ("Saturday", 4, "CD", "RS"), ("Saturday", "BREAK2", "INTERVAL", None),
            ("Saturday", 5, "DA", "AAK"), ("Saturday", 6, "AAD", "SKI")
        ]

        cur.execute("DELETE FROM timetable") # Clear existing MySQL timetable
        
        count = 0
        for day, hr, sub_abbr, fac_abbr in timetable_data:
            full_sub_name = name_map.get(sub_abbr.upper())
            s_id = subj_map.get(full_sub_name)
            
            f_id = None
            if fac_abbr:
                f_username = name_map.get(fac_abbr.upper())
                f_id = faculty_map.get(f_username)
            
            if s_id:
                start, end = slots[hr]
                cur.execute("""
                    INSERT INTO timetable (faculty_id, subject_id, day_of_week, start_time, end_time, branch, semester)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (f_id, s_id, day, start, end, branch, semester))
                count += 1
            else:
                print(f"Skipping {day} {hr}: Subject {sub_abbr} -> {full_sub_name} (ID: {s_id}) not found")

        conn.commit()
        conn.close()
        print(f"Successfully loaded {count} periods (including breaks) into the timetable.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    seed_timetable()
