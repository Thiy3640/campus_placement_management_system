"""
Campus Placement Management System — Database Layer
SQLite database initialization, schema creation, and seed data.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'placement.db')


def get_db():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database schema and seed data."""
    conn = get_db()
    cursor = conn.cursor()

    # ── Schema Creation ──────────────────────────────────────────────

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS STUDENT (
            roll_no       TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            dob           TEXT,
            gender        TEXT,
            phone         TEXT,
            email         TEXT,
            dept          TEXT,
            cgpa          REAL,
            tenth_pct     REAL,
            twelfth_pct   REAL,
            core_skills   TEXT,
            placement_status TEXT DEFAULT 'Unplaced',
            current_highest_ctc REAL DEFAULT 0.00
        );

        CREATE TABLE IF NOT EXISTS COMPANY (
            comp_id       TEXT PRIMARY KEY,
            comp_name     TEXT NOT NULL,
            industry_type TEXT,
            hr_name       TEXT,
            hr_email      TEXT,
            hr_phone      TEXT
        );

        CREATE TABLE IF NOT EXISTS JOB (
            job_id        TEXT PRIMARY KEY,
            comp_id       TEXT NOT NULL,
            job_title     TEXT,
            job_desc      TEXT,
            min_cgpa      REAL,
            ctc           REAL,
            eligible_depts TEXT,
            interview_date TEXT,
            FOREIGN KEY (comp_id) REFERENCES COMPANY(comp_id)
        );

        CREATE TABLE IF NOT EXISTS APPLICATION (
            app_id        TEXT PRIMARY KEY,
            roll_no       TEXT NOT NULL,
            job_id        TEXT NOT NULL,
            app_date      TEXT,
            app_status    TEXT DEFAULT 'Pending',
            FOREIGN KEY (roll_no) REFERENCES STUDENT(roll_no),
            FOREIGN KEY (job_id)  REFERENCES JOB(job_id)
        );
    """)

    # ── Seed Data (only if tables are empty) ─────────────────────────

    count = cursor.execute("SELECT COUNT(*) FROM STUDENT").fetchone()[0]
    if count == 0:
        # Students
        students = [
            ('23103001', 'Aarav Sharma',    '2002-03-15', 'Male',   '9876543001', 'aarav.s@institute.ac.in',   'CSE', 9.12, 95.4, 92.1, 'Python, Java, SQL',       'Placed', 8.00),
            ('23103002', 'Diya Patel',      '2002-07-22', 'Female', '9876543002', 'diya.p@institute.ac.in',    'CSE', 8.75, 91.2, 88.5, 'C++, Python, Web Dev',    'Unplaced', 0.00),
            ('23103003', 'Rohan Kumar',     '2001-11-10', 'Male',   '9876543003', 'rohan.k@institute.ac.in',   'ECE', 7.60, 82.0, 79.8, 'C++, MATLAB',             'Unplaced', 0.00),
            ('23103004', 'Sneha Reddy',     '2002-01-05', 'Female', '9876543004', 'sneha.r@institute.ac.in',   'CSE', 8.90, 93.5, 90.2, 'Java, Python, SQL',       'Placed', 6.50),
            ('23103005', 'Kabir Singh',     '2002-06-18', 'Male',   '9876543005', 'kabir.s@institute.ac.in',   'ME',  7.20, 78.5, 75.0, 'AutoCAD, SolidWorks',     'Unplaced', 0.00),
            ('23103006', 'Ananya Gupta',    '2001-09-30', 'Female', '9876543006', 'ananya.g@institute.ac.in',  'CSE', 9.45, 97.0, 95.5, 'Python, Java, C++, SQL',  'Placed', 12.00),
            ('23103007', 'Vikram Nair',     '2002-04-12', 'Male',   '9876543007', 'vikram.n@institute.ac.in',  'ECE', 8.30, 88.0, 85.2, 'Python, MATLAB, C',       'Unplaced', 0.00),
            ('23103008', 'Priya Menon',     '2002-02-28', 'Female', '9876543008', 'priya.m@institute.ac.in',   'CE',  8.10, 86.5, 83.7, 'AutoCAD, Python',         'Unplaced', 0.00),
            ('23103009', 'Arjun Das',       '2001-12-20', 'Male',   '9876543009', 'arjun.d@institute.ac.in',   'CSE', 8.55, 90.0, 87.3, 'Java, SQL, Web Dev',      'Unplaced', 0.00),
            ('23103010', 'Meera Iyer',      '2002-05-08', 'Female', '9876543010', 'meera.i@institute.ac.in',   'ECE', 7.85, 84.0, 81.5, 'C++, MATLAB, Python',     'Unplaced', 0.00),
            ('23103027', 'Chingu Robertson','2002-08-14', 'Male',   '9876543027', 'chingu.r@institute.ac.in',  'CSE', 8.80, 92.0, 89.5, 'Python, Java, C++, SQL',  'Placed', 7.50),
        ]
        cursor.executemany(
            "INSERT INTO STUDENT VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            students
        )

        # Companies
        companies = [
            ('COMP001', 'TechNova Solutions',  'IT',               'Ravi Mehta',    'ravi.m@technova.com',    '011-23456789'),
            ('COMP002', 'FinEdge Analytics',   'Finance',          'Sana Khan',     'sana.k@finedge.com',     '022-34567890'),
            ('COMP003', 'CoreBuild Industries', 'Core Engineering', 'Deepak Joshi',  'deepak.j@corebuild.com', '033-45678901'),
            ('COMP004', 'CloudPeak Labs',      'IT',               'Aisha Verma',   'aisha.v@cloudpeak.com',  '044-56789012'),
            ('COMP005', 'Stratton Consulting',  'Consulting',      'Nikhil Rao',    'nikhil.r@stratton.com',  '055-67890123'),
        ]
        cursor.executemany(
            "INSERT INTO COMPANY VALUES (?,?,?,?,?,?)",
            companies
        )

        # Jobs
        jobs = [
            ('JOB001', 'COMP001', 'Software Development Engineer', 'Build scalable microservices',   8.00, 12.00, 'CSE,ECE',     '2026-02-15'),
            ('JOB002', 'COMP001', 'Data Analyst',                  'Analyze business data',          7.50,  8.00, 'CSE,ECE,ME',  '2026-02-20'),
            ('JOB003', 'COMP002', 'Quantitative Analyst',          'Financial modeling',             8.50, 15.00, 'CSE',         '2026-03-01'),
            ('JOB004', 'COMP003', 'Design Engineer',               'Mechanical design and analysis', 7.00,  6.50, 'ME,CE',       '2026-03-10'),
            ('JOB005', 'COMP004', 'Cloud Engineer',                'AWS/GCP infrastructure',         8.00, 10.50, 'CSE,ECE',     '2026-03-15'),
            ('JOB006', 'COMP004', 'Backend Developer',             'Python/Go microservices',        7.50,  9.00, 'CSE',         '2026-03-20'),
            ('JOB007', 'COMP005', 'Business Analyst',              'Strategy consulting',            7.00,  7.50, 'CSE,ECE,ME,CE','2026-04-01'),
            ('JOB008', 'COMP002', 'Risk Analyst',                  'Credit risk modeling',           8.00, 11.00, 'CSE,ECE',     '2026-04-05'),
        ]
        cursor.executemany(
            "INSERT INTO JOB VALUES (?,?,?,?,?,?,?,?)",
            jobs
        )

        # Applications
        applications = [
            ('APP001', '23103001', 'JOB001', '2026-01-20', 'Accepted'),
            ('APP002', '23103004', 'JOB004', '2026-01-25', 'Accepted'),
            ('APP003', '23103006', 'JOB001', '2026-01-20', 'Accepted'),
            ('APP004', '23103006', 'JOB003', '2026-02-10', 'Accepted'),
            ('APP005', '23103002', 'JOB002', '2026-02-01', 'Interviewing'),
            ('APP006', '23103003', 'JOB007', '2026-02-15', 'Pending'),
            ('APP007', '23103009', 'JOB006', '2026-02-20', 'Offered'),
            ('APP008', '23103027', 'JOB002', '2026-01-22', 'Accepted'),
            ('APP009', '23103007', 'JOB005', '2026-03-01', 'Pending'),
            ('APP010', '23103005', 'JOB004', '2026-03-05', 'Interviewing'),
        ]
        cursor.executemany(
            "INSERT INTO APPLICATION VALUES (?,?,?,?,?)",
            applications
        )

    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at {os.path.abspath(DB_PATH)}")


if __name__ == '__main__':
    init_db()
