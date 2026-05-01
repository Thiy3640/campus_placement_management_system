function studentForm(s) {
  return `<form id="student-form" class="form-grid">
    <div class="form-group"><label class="form-label">Roll No</label><input class="form-input" name="roll_no" value="${s?.roll_no||''}" ${s?'readonly':'required'}></div>
    <div class="form-group"><label class="form-label">Name</label><input class="form-input" name="name" value="${s?.name||''}" required></div>
    <div class="form-group"><label class="form-label">DOB</label><input class="form-input" type="date" name="dob" value="${s?.dob||''}"></div>
    <div class="form-group"><label class="form-label">Gender</label><select class="form-select" name="gender"><option value="">Select</option><option ${s?.gender==='Male'?'selected':''}>Male</option><option ${s?.gender==='Female'?'selected':''}>Female</option></select></div>
    <div class="form-group"><label class="form-label">Phone</label><input class="form-input" name="phone" value="${s?.phone||''}"></div>
    <div class="form-group"><label class="form-label">Email</label><input class="form-input" type="email" name="email" value="${s?.email||''}"></div>
    <div class="form-group"><label class="form-label">Department</label><select class="form-select" name="dept"><option value="">Select</option>${['CSE','ECE','ME','CE'].map(d=>`<option ${s?.dept===d?'selected':''}>${d}</option>`).join('')}</select></div>
    <div class="form-group"><label class="form-label">CGPA</label><input class="form-input" type="number" step="0.01" name="cgpa" value="${s?.cgpa||''}"></div>
    <div class="form-group"><label class="form-label">10th %</label><input class="form-input" type="number" step="0.1" name="tenth_pct" value="${s?.tenth_pct||''}"></div>
    <div class="form-group"><label class="form-label">12th %</label><input class="form-input" type="number" step="0.1" name="twelfth_pct" value="${s?.twelfth_pct||''}"></div>
    <div class="form-group full-width"><label class="form-label">Core Skills</label><input class="form-input" name="core_skills" value="${s?.core_skills||''}" placeholder="e.g. Python, Java, SQL"></div>
    <div class="form-actions"><button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button><button type="submit" class="btn btn-primary">${s?'Update':'Register'} Student</button></div>
  </form>`;
}

async function renderStudents() {
  const m = document.getElementById('main-content');
  m.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const data = await api('/students');
    m.innerHTML = `
    <div class="page-header"><div><h1>Students</h1><p>Manage student registrations</p></div>
    <button class="btn btn-primary" onclick="showAddStudent()">+ Add Student</button></div>
    <div class="glass-card">
      <div class="search-bar">
        <input class="search-input" id="student-search" placeholder="Search students..." oninput="filterStudentTable()">
        <select class="filter-select" id="student-filter" onchange="filterStudentTable()"><option value="">All Status</option><option>Placed</option><option>Unplaced</option></select>
      </div>
      <div class="table-wrapper"><table><thead><tr><th>Roll No</th><th>Name</th><th>Dept</th><th>CGPA</th><th>Status</th><th>CTC</th><th>Actions</th></tr></thead>
      <tbody id="student-tbody">${data.map(s => `<tr>
        <td>${s.roll_no}</td><td>${s.name}</td><td>${s.dept}</td><td>${s.cgpa}</td>
        <td>${badge(s.placement_status)}</td><td>${s.current_highest_ctc > 0 ? `<span class="ctc-value">${s.current_highest_ctc} LPA</span>` : '-'}</td>
        <td><div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="showEditStudent('${s.roll_no}')">Edit</button><button class="btn btn-danger btn-sm" onclick="deleteStudent('${s.roll_no}')">Del</button></div></td>
      </tr>`).join('')}</tbody></table></div></div>`;
  } catch(e) { m.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}

function filterStudentTable() {
  const q = document.getElementById('student-search').value.toLowerCase();
  const f = document.getElementById('student-filter').value;
  document.querySelectorAll('#student-tbody tr').forEach(r => {
    const text = r.textContent.toLowerCase();
    const statusMatch = !f || r.querySelector('.badge')?.textContent === f;
    r.style.display = text.includes(q) && statusMatch ? '' : 'none';
  });
}

function showAddStudent() { openModal('Register Student', studentForm()); bindStudentForm(); }
async function showEditStudent(id) {
  const s = await api('/students/' + id);
  openModal('Edit Student', studentForm(s));
  bindStudentForm(true, id);
}
function bindStudentForm(isEdit, id) {
  document.getElementById('student-form').onsubmit = async e => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);
    body.cgpa = parseFloat(body.cgpa) || 0;
    body.tenth_pct = parseFloat(body.tenth_pct) || 0;
    body.twelfth_pct = parseFloat(body.twelfth_pct) || 0;
    try {
      if (isEdit) await api('/students/' + id, { method: 'PUT', body });
      else await api('/students', { method: 'POST', body });
      toast(isEdit ? 'Student updated' : 'Student registered');
      closeModal(); renderStudents();
    } catch(e) { toast(e.message, 'error'); }
  };
}
async function deleteStudent(id) {
  if (!confirm('Delete this student?')) return;
  try { await api('/students/' + id, { method: 'DELETE' }); toast('Student deleted'); renderStudents(); }
  catch(e) { toast(e.message, 'error'); }
}
