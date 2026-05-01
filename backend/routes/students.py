"""
Student routes — CRUD operations for the STUDENT table.
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

students_bp = Blueprint('students', __name__)


@students_bp.route('/api/students', methods=['GET'])
def list_students():
    """List all students with optional filters."""
    db = get_db()
    query = "SELECT * FROM STUDENT"
    params = []

    dept = request.args.get('dept')
    status = request.args.get('status')

    conditions = []
    if dept:
        conditions.append("dept = ?")
        params.append(dept)
    if status:
        conditions.append("placement_status = ?")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY name ASC"

    rows = db.execute(query, params).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@students_bp.route('/api/students', methods=['POST'])
def create_student():
    """Register a new student."""
    data = request.get_json()
    required = ['roll_no', 'name']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    db = get_db()
    try:
        db.execute("""
            INSERT INTO STUDENT (roll_no, name, dob, gender, phone, email, dept, cgpa,
                                 tenth_pct, twelfth_pct, core_skills, placement_status, current_highest_ctc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['roll_no'], data['name'],
            data.get('dob', ''), data.get('gender', ''),
            data.get('phone', ''), data.get('email', ''),
            data.get('dept', ''), data.get('cgpa', 0),
            data.get('tenth_pct', 0), data.get('twelfth_pct', 0),
            data.get('core_skills', ''),
            data.get('placement_status', 'Unplaced'),
            data.get('current_highest_ctc', 0.00)
        ))
        db.commit()
        db.close()
        return jsonify({'message': 'Student registered successfully', 'roll_no': data['roll_no']}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400


@students_bp.route('/api/students/<roll_no>', methods=['GET'])
def get_student(roll_no):
    """Get a student by roll number."""
    db = get_db()
    row = db.execute("SELECT * FROM STUDENT WHERE roll_no = ?", (roll_no,)).fetchone()
    db.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Student not found'}), 404


@students_bp.route('/api/students/<roll_no>', methods=['PUT'])
def update_student(roll_no):
    """Update a student's information."""
    data = request.get_json()
    db = get_db()

    # Check existence
    existing = db.execute("SELECT * FROM STUDENT WHERE roll_no = ?", (roll_no,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Student not found'}), 404

    # Build dynamic update
    updatable = ['name', 'dob', 'gender', 'phone', 'email', 'dept', 'cgpa',
                 'tenth_pct', 'twelfth_pct', 'core_skills', 'placement_status', 'current_highest_ctc']
    sets = []
    params = []
    for field in updatable:
        if field in data:
            sets.append(f"{field} = ?")
            params.append(data[field])

    if not sets:
        db.close()
        return jsonify({'error': 'No fields to update'}), 400

    params.append(roll_no)
    db.execute(f"UPDATE STUDENT SET {', '.join(sets)} WHERE roll_no = ?", params)
    db.commit()
    db.close()
    return jsonify({'message': 'Student updated successfully'})


@students_bp.route('/api/students/<roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    """Delete a student."""
    db = get_db()
    existing = db.execute("SELECT * FROM STUDENT WHERE roll_no = ?", (roll_no,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Student not found'}), 404

    db.execute("DELETE FROM APPLICATION WHERE roll_no = ?", (roll_no,))
    db.execute("DELETE FROM STUDENT WHERE roll_no = ?", (roll_no,))
    db.commit()
    db.close()
    return jsonify({'message': 'Student deleted successfully'})
