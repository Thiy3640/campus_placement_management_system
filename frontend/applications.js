async function appFormHtml() {
  const students = await api('/students');
  const jobs = await api('/jobs');
  return `<form id="app-form" class="form-grid">
    <div class="form-group"><label class="form-label">App ID</label><input class="form-input" name="app_id" required placeholder="e.g. APP011"></div>
    <div class="form-group"><label class="form-label">Student</label><select class="form-select" name="roll_no" required>${students.map(s=>`<option value="${s.roll_no}">${s.roll_no} - ${s.name} (${s.placement_status})</option>`).join('')}</select></div>
    <div class="form-group"><label class="form-label">Job</label><select class="form-select" name="job_id" required>${jobs.map(j=>`<option value="${j.job_id}">${j.job_id} - ${j.job_title} @ ${j.comp_name} (${j.ctc} LPA)</option>`).join('')}</select></div>
    <div class="form-group"><label class="form-label">Date</label><input class="form-input" type="date" name="app_date" value="${new Date().toISOString().split('T')[0]}"></div>
    <div class="form-actions"><button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button><button type="submit" class="btn btn-primary">Submit Application</button></div>
  </form>`;
}
async function renderApplications() {
  const m = document.getElementById('main-content');
  m.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const data = await api('/applications');
    m.innerHTML = `<div class="page-header"><div><h1>Applications</h1><p>Track student applications &amp; Dream Offers</p></div>
    <button class="btn btn-primary" onclick="showAddApp()">+ New Application</button></div>
    <div class="glass-card"><div class="table-wrapper"><table><thead><tr><th>App ID</th><th>Student</th><th>Dept</th><th>Job</th><th>Company</th><th>CTC</th><th>Date</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>${data.map(a=>`<tr><td>${a.app_id}</td><td>${a.student_name}</td><td>${a.dept}</td><td>${a.job_title}</td><td>${a.comp_name}</td><td><span class="ctc-value">${a.ctc} LPA</span></td><td>${a.app_date||'-'}</td><td>${badge(a.app_status)}</td>
    <td><div class="btn-group">
      <select class="filter-select" onchange="updateAppStatus('${a.app_id}',this.value)" style="padding:0.3rem 0.5rem;font-size:0.75rem">
        ${['Pending','Interviewing','Offered','Accepted','Rejected'].map(s=>`<option ${a.app_status===s?'selected':''}>${s}</option>`).join('')}
      </select>
      <button class="btn btn-danger btn-sm" onclick="deleteApp('${a.app_id}')">Del</button>
    </div></td></tr>`).join('')}</tbody></table></div></div>`;
  } catch(e) { m.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
async function showAddApp() { openModal('Submit Application', await appFormHtml()); bindAppForm(); }
function bindAppForm() {
  document.getElementById('app-form').onsubmit = async e => {
    e.preventDefault(); const body = Object.fromEntries(new FormData(e.target));
    try { const r = await api('/applications',{method:'POST',body});
      toast(r.message + (r.is_dream_offer?' 🌟':''));
      closeModal(); renderApplications(); } catch(e){toast(e.message,'error');}
  };
}
async function updateAppStatus(id, status) {
  try { await api('/applications/'+id+'/status',{method:'PUT',body:{app_status:status}});
    toast(`Status updated to ${status}`); renderApplications(); } catch(e){toast(e.message,'error');}
}
async function deleteApp(id) { if(!confirm('Delete?')) return;
  try { await api('/applications/'+id,{method:'DELETE'}); toast('Deleted'); renderApplications(); } catch(e){toast(e.message,'error');} }
