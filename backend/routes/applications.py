"""Application routes — CRUD + Dream Offer logic."""
from flask import Blueprint, request, jsonify
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/api/applications', methods=['GET'])
def list_applications():
    db = get_db()
    rows = db.execute("""
        SELECT A.*, S.name as student_name, S.dept, J.job_title, J.ctc, C.comp_name
        FROM APPLICATION A JOIN STUDENT S ON A.roll_no = S.roll_no
        JOIN JOB J ON A.job_id = J.job_id JOIN COMPANY C ON J.comp_id = C.comp_id
        ORDER BY A.app_date DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])

@applications_bp.route('/api/applications', methods=['POST'])
def create_application():
    data = request.get_json()
    for f in ['app_id','roll_no','job_id']:
        if f not in data or not data[f]:
            return jsonify({'error': f'Missing: {f}'}), 400
    db = get_db()
    student = db.execute("SELECT * FROM STUDENT WHERE roll_no=?", (data['roll_no'],)).fetchone()
    if not student: db.close(); return jsonify({'error':'Student not found'}), 404
    student = dict(student)
    job = db.execute("SELECT J.*,C.comp_name FROM JOB J JOIN COMPANY C ON J.comp_id=C.comp_id WHERE J.job_id=?", (data['job_id'],)).fetchone()
    if not job: db.close(); return jsonify({'error':'Job not found'}), 404
    job = dict(job)
    dup = db.execute("SELECT * FROM APPLICATION WHERE roll_no=? AND job_id=?", (data['roll_no'],data['job_id'])).fetchone()
    if dup: db.close(); return jsonify({'error':'Already applied'}), 400
    eligible = [d.strip() for d in (job.get('eligible_depts') or '').split(',')]
    if student['dept'] not in eligible:
        db.close(); return jsonify({'error':f"Dept {student['dept']} not eligible"}), 400
    if student['cgpa'] < job['min_cgpa']:
        db.close(); return jsonify({'error':f"CGPA {student['cgpa']} below min {job['min_cgpa']}"}), 400
    if student['placement_status'] == 'Placed':
        acc = db.execute("SELECT COUNT(*) FROM APPLICATION WHERE roll_no=? AND app_status='Accepted'", (data['roll_no'],)).fetchone()[0]
        if acc >= 2: db.close(); return jsonify({'error':'Max 2 offers reached'}), 400
        if job['ctc'] < student['current_highest_ctc'] + 2.5:
            db.close(); return jsonify({'error':f"Dream rule: need {student['current_highest_ctc']+2.5:.2f} LPA, job offers {job['ctc']}"}), 400
    try:
        db.execute("INSERT INTO APPLICATION VALUES(?,?,?,?,?)", (data['app_id'],data['roll_no'],data['job_id'],data.get('app_date',date.today().isoformat()),'Pending'))
        db.commit(); db.close()
        dream = student['placement_status']=='Placed'
        return jsonify({'message':'Application submitted' + (' (Dream Offer!)' if dream else ''),'app_id':data['app_id'],'is_dream_offer':dream}), 201
    except Exception as e: db.close(); return jsonify({'error':str(e)}), 400

@applications_bp.route('/api/applications/<app_id>/status', methods=['PUT'])
def update_status(app_id):
    data = request.get_json()
    ns = data.get('app_status')
    if ns not in ['Pending','Interviewing','Offered','Accepted','Rejected']:
        return jsonify({'error':'Invalid status'}), 400
    db = get_db()
    a = db.execute("SELECT A.*,J.ctc FROM APPLICATION A JOIN JOB J ON A.job_id=J.job_id WHERE A.app_id=?", (app_id,)).fetchone()
    if not a: db.close(); return jsonify({'error':'Not found'}), 404
    a = dict(a)
    db.execute("UPDATE APPLICATION SET app_status=? WHERE app_id=?", (ns, app_id))
    if ns == 'Accepted':
        s = dict(db.execute("SELECT * FROM STUDENT WHERE roll_no=?", (a['roll_no'],)).fetchone())
        db.execute("UPDATE STUDENT SET placement_status='Placed', current_highest_ctc=? WHERE roll_no=?",
                   (max(s['current_highest_ctc'], a['ctc']), a['roll_no']))
    db.commit(); db.close()
    return jsonify({'message':f'Status updated to {ns}'})

@applications_bp.route('/api/applications/<app_id>', methods=['DELETE'])
def delete_application(app_id):
    db = get_db()
    if not db.execute("SELECT * FROM APPLICATION WHERE app_id=?", (app_id,)).fetchone():
        db.close(); return jsonify({'error':'Not found'}), 404
    db.execute("DELETE FROM APPLICATION WHERE app_id=?", (app_id,))
    db.commit(); db.close()
    return jsonify({'message':'Deleted'})

@applications_bp.route('/api/applications/dream-upgrades', methods=['GET'])
def dream_upgrades():
    db = get_db()
    rows = db.execute("""
        SELECT S.roll_no,S.name,S.current_highest_ctc,J.job_title,J.ctc,C.comp_name
        FROM STUDENT S JOIN APPLICATION A ON S.roll_no=A.roll_no
        JOIN JOB J ON A.job_id=J.job_id JOIN COMPANY C ON J.comp_id=C.comp_id
        WHERE A.app_status='Accepted' ORDER BY J.ctc DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])
