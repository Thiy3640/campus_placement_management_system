"""
Company routes — CRUD operations for the COMPANY table.
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

companies_bp = Blueprint('companies', __name__)


@companies_bp.route('/api/companies', methods=['GET'])
def list_companies():
    """List all companies."""
    db = get_db()
    rows = db.execute("SELECT * FROM COMPANY ORDER BY comp_name ASC").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@companies_bp.route('/api/companies', methods=['POST'])
def create_company():
    """Register a new company."""
    data = request.get_json()
    required = ['comp_id', 'comp_name']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    db = get_db()
    try:
        db.execute("""
            INSERT INTO COMPANY (comp_id, comp_name, industry_type, hr_name, hr_email, hr_phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['comp_id'], data['comp_name'],
            data.get('industry_type', ''),
            data.get('hr_name', ''),
            data.get('hr_email', ''),
            data.get('hr_phone', '')
        ))
        db.commit()
        db.close()
        return jsonify({'message': 'Company registered successfully', 'comp_id': data['comp_id']}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400


@companies_bp.route('/api/companies/<comp_id>', methods=['GET'])
def get_company(comp_id):
    """Get a company by ID."""
    db = get_db()
    row = db.execute("SELECT * FROM COMPANY WHERE comp_id = ?", (comp_id,)).fetchone()
    db.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Company not found'}), 404


@companies_bp.route('/api/companies/<comp_id>', methods=['PUT'])
def update_company(comp_id):
    """Update a company's information."""
    data = request.get_json()
    db = get_db()

    existing = db.execute("SELECT * FROM COMPANY WHERE comp_id = ?", (comp_id,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Company not found'}), 404

    updatable = ['comp_name', 'industry_type', 'hr_name', 'hr_email', 'hr_phone']
    sets = []
    params = []
    for field in updatable:
        if field in data:
            sets.append(f"{field} = ?")
            params.append(data[field])

    if not sets:
        db.close()
        return jsonify({'error': 'No fields to update'}), 400

    params.append(comp_id)
    db.execute(f"UPDATE COMPANY SET {', '.join(sets)} WHERE comp_id = ?", params)
    db.commit()
    db.close()
    return jsonify({'message': 'Company updated successfully'})


@companies_bp.route('/api/companies/<comp_id>', methods=['DELETE'])
def delete_company(comp_id):
    """Delete a company and cascade to jobs and applications."""
    db = get_db()
    existing = db.execute("SELECT * FROM COMPANY WHERE comp_id = ?", (comp_id,)).fetchone()
    if not existing:
        db.close()
        return jsonify({'error': 'Company not found'}), 404

    # Cascade delete: applications for this company's jobs, then jobs, then company
    jobs = db.execute("SELECT job_id FROM JOB WHERE comp_id = ?", (comp_id,)).fetchall()
    for job in jobs:
        db.execute("DELETE FROM APPLICATION WHERE job_id = ?", (job['job_id'],))
    db.execute("DELETE FROM JOB WHERE comp_id = ?", (comp_id,))
    db.execute("DELETE FROM COMPANY WHERE comp_id = ?", (comp_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Company deleted successfully'})
