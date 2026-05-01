"""
Report routes — Placement reports and analytical queries from Step 13.
"""

from flask import Blueprint, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/api/reports/placement-status', methods=['GET'])
def placement_status_report():
    """Placement Status Report with offer details."""
    db = get_db()
    placed = db.execute("""
        SELECT S.roll_no, S.name, S.dept, J.job_title, J.ctc, C.comp_name
        FROM STUDENT S
        JOIN APPLICATION A ON S.roll_no = A.roll_no
        JOIN JOB J ON A.job_id = J.job_id
        JOIN COMPANY C ON J.comp_id = C.comp_id
        WHERE A.app_status = 'Accepted'
        ORDER BY S.name
    """).fetchall()

    total_students = db.execute("SELECT COUNT(*) FROM STUDENT").fetchone()[0]
    placed_count = db.execute("SELECT COUNT(*) FROM STUDENT WHERE placement_status = 'Placed'").fetchone()[0]
    total_offers = db.execute("SELECT COUNT(*) FROM APPLICATION WHERE app_status = 'Accepted'").fetchone()[0]

    db.close()
    return jsonify({
        'total_students': total_students,
        'placed_count': placed_count,
        'unplaced_count': total_students - placed_count,
        'total_offers': total_offers,
        'placement_percentage': round((placed_count / total_students * 100), 1) if total_students > 0 else 0,
        'placed_students': [dict(r) for r in placed]
    })


@reports_bp.route('/api/reports/unplaced-eligible', methods=['GET'])
def unplaced_eligible():
    """QUERY 3: Alphabetical listing of unplaced students with CGPA >= 8.0."""
    db = get_db()
    rows = db.execute("""
        SELECT roll_no, name, dept, cgpa
        FROM STUDENT
        WHERE placement_status = 'Unplaced' AND cgpa >= 8.00
        ORDER BY name ASC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@reports_bp.route('/api/reports/company-job-counts', methods=['GET'])
def company_job_counts():
    """QUERY 4: Company IDs with the number of jobs each has offered."""
    db = get_db()
    rows = db.execute("""
        SELECT C.comp_id, C.comp_name, COUNT(*) as job_count
        FROM JOB J
        JOIN COMPANY C ON J.comp_id = C.comp_id
        GROUP BY C.comp_id, C.comp_name
        ORDER BY job_count DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@reports_bp.route('/api/reports/ctc-upgrade-eligibility', methods=['GET'])
def ctc_upgrade_eligibility():
    """CTC Upgrade Eligibility Report — placed students eligible for Dream Offers."""
    db = get_db()
    rows = db.execute("""
        SELECT S.roll_no, S.name, S.dept, S.current_highest_ctc,
               J.job_id, J.job_title, J.ctc as new_ctc, C.comp_name
        FROM STUDENT S, JOB J, COMPANY C
        WHERE S.placement_status = 'Placed'
        AND J.comp_id = C.comp_id
        AND J.min_cgpa <= S.cgpa
        AND J.ctc >= (S.current_highest_ctc + 2.50)
        ORDER BY S.name, J.ctc DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@reports_bp.route('/api/reports/dashboard', methods=['GET'])
def dashboard():
    """Dashboard statistics."""
    db = get_db()
    total_students = db.execute("SELECT COUNT(*) FROM STUDENT").fetchone()[0]
    placed = db.execute("SELECT COUNT(*) FROM STUDENT WHERE placement_status = 'Placed'").fetchone()[0]
    companies = db.execute("SELECT COUNT(*) FROM COMPANY").fetchone()[0]
    jobs = db.execute("SELECT COUNT(*) FROM JOB").fetchone()[0]
    applications = db.execute("SELECT COUNT(*) FROM APPLICATION").fetchone()[0]
    avg_ctc = db.execute("SELECT AVG(ctc) FROM JOB").fetchone()[0] or 0
    highest_ctc = db.execute("SELECT MAX(ctc) FROM JOB").fetchone()[0] or 0
    pending = db.execute("SELECT COUNT(*) FROM APPLICATION WHERE app_status = 'Pending'").fetchone()[0]
    db.close()

    return jsonify({
        'total_students': total_students,
        'placed_students': placed,
        'unplaced_students': total_students - placed,
        'placement_rate': round((placed / total_students * 100), 1) if total_students > 0 else 0,
        'total_companies': companies,
        'total_jobs': jobs,
        'total_applications': applications,
        'avg_ctc': round(avg_ctc, 2),
        'highest_ctc': highest_ctc,
        'pending_applications': pending
    })
