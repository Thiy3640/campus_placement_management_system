"""
Job routes — CRUD + eligibility queries for the JOB table.
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs with company name join."""
    db = get_db()
    rows = db.execute("""
        SELECT J.*, C.comp_name
        FROM JOB J
        JOIN COMPANY C ON J.comp_id = C.comp_id
        ORDER BY J.interview_date DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@jobs_bp.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job posting."""
    data = request.get_json()
    required = ['job_id', 'comp_id', 'job_title']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    db = get_db()
    # Verify company exists
    comp = db.execute("SELECT * FROM COMPANY WHERE comp_id = ?", (data['comp_id'],)).fetchone()
    if not comp:
        db.close()
        return jsonify({'error': 'Company not found'}), 400

    try:
        db.execute("""
            INSERT INTO JOB (job_id, comp_id, job_title, job_desc, min_cgpa, ctc, eligible_depts, interview_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['job_id'], data['comp_id'], data['job_title'],
            data.get('job_desc', ''),
            data.get('min_cgpa', 0),
            data.get('ctc', 0),
            data.get('eligible_depts', ''),
            data.get('interview_date', '')
        ))
        db.commit()
        db.close()
        return jsonify({'message': 'Job posted successfully', 'job_id': data['job_id']}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400


@jobs_bp.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get a job by ID."""
    db = get_db()
    row = db.execute("""
        SELECT J.*, C.comp_name
        FROM JOB J
        JOIN COMPANY C ON J.comp_id = C.comp_id
        WHERE J.job_id = ?
    """, (job_id,)).fetchone()
    db.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Job not found'}), 404


@jobs_bp.route('/api/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    """Update a job posting."""
    data = request.get_json()
    db = get_db()

    existing = db.execute("SELECT * FROM JOB WHERE job_id = ?", (job_id,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Job not found'}), 404

    updatable = ['comp_id', 'job_title', 'job_desc', 'min_cgpa', 'ctc', 'eligible_depts', 'interview_date']
    sets = []
    params = []
    for field in updatable:
        if field in data:
            sets.append(f"{field} = ?")
            params.append(data[field])

    if not sets:
        db.close()
        return jsonify({'error': 'No fields to update'}), 400

    params.append(job_id)
    db.execute(f"UPDATE JOB SET {', '.join(sets)} WHERE job_id = ?", params)
    db.commit()
    db.close()
    return jsonify({'message': 'Job updated successfully'})


@jobs_bp.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job and its applications."""
    db = get_db()
    existing = db.execute("SELECT * FROM JOB WHERE job_id = ?", (job_id,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Job not found'}), 404

    db.execute("DELETE FROM APPLICATION WHERE job_id = ?", (job_id,))
    db.execute("DELETE FROM JOB WHERE job_id = ?", (job_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Job deleted successfully'})


@jobs_bp.route('/api/jobs/eligible/<roll_no>', methods=['GET'])
def eligible_jobs(roll_no):
    """
    QUERY 1 from Step 13:
    Get all jobs a student is eligible for, including Dream Offer (2.5 LPA rule).
    """
    db = get_db()
    student = db.execute("SELECT * FROM STUDENT WHERE roll_no = ?", (roll_no,)).fetchone()
    if not student:
        db.close()
        return jsonify({'error': 'Student not found'}), 404

    student = dict(student)

    if student['placement_status'] == 'Unplaced':
        # Unplaced: eligible for any job matching CGPA and department
        rows = db.execute("""
            SELECT J.job_id, C.comp_name, J.job_title, J.ctc, J.min_cgpa, J.eligible_depts, J.interview_date
            FROM JOB J
            JOIN COMPANY C ON J.comp_id = C.comp_id
            WHERE J.min_cgpa <= ?
            ORDER BY J.ctc DESC
        """, (student['cgpa'],)).fetchall()
    else:
        # Placed: only eligible under Dream Offer rule (CTC >= current + 2.5)
        rows = db.execute("""
            SELECT J.job_id, C.comp_name, J.job_title, J.ctc, J.min_cgpa, J.eligible_depts, J.interview_date
            FROM JOB J
            JOIN COMPANY C ON J.comp_id = C.comp_id
            WHERE J.min_cgpa <= ?
            AND J.ctc >= (? + 2.50)
            ORDER BY J.ctc DESC
        """, (student['cgpa'], student['current_highest_ctc'])).fetchall()

    # Filter by department eligibility
    result = []
    for row in rows:
        row_dict = dict(row)
        eligible_depts = [d.strip() for d in (row_dict.get('eligible_depts') or '').split(',')]
        if student['dept'] in eligible_depts:
            row_dict['is_dream_offer'] = student['placement_status'] == 'Placed'
            result.append(row_dict)

    db.close()
    return jsonify({
        'student': student,
        'eligible_jobs': result
    })
