async function jobFormHtml(j) {
  const companies = await api('/companies');
  return `<form id="job-form" class="form-grid">
    <div class="form-group"><label class="form-label">Job ID</label><input class="form-input" name="job_id" value="${j?.job_id||''}" ${j?'readonly':'required'}></div>
    <div class="form-group"><label class="form-label">Company</label><select class="form-select" name="comp_id" ${j?'disabled':'required'}>${companies.map(c=>`<option value="${c.comp_id}" ${j?.comp_id===c.comp_id?'selected':''}>${c.comp_name}</option>`).join('')}</select></div>
    <div class="form-group"><label class="form-label">Job Title</label><input class="form-input" name="job_title" value="${j?.job_title||''}" required></div>
    <div class="form-group full-width"><label class="form-label">Description</label><input class="form-input" name="job_desc" value="${j?.job_desc||''}"></div>
    <div class="form-group"><label class="form-label">Min CGPA</label><input class="form-input" type="number" step="0.01" name="min_cgpa" value="${j?.min_cgpa||''}"></div>
    <div class="form-group"><label class="form-label">CTC (LPA)</label><input class="form-input" type="number" step="0.01" name="ctc" value="${j?.ctc||''}" required></div>
    <div class="form-group"><label class="form-label">Eligible Depts</label><input class="form-input" name="eligible_depts" value="${j?.eligible_depts||''}" placeholder="CSE,ECE,ME"></div>
    <div class="form-group"><label class="form-label">Interview Date</label><input class="form-input" type="date" name="interview_date" value="${j?.interview_date||''}"></div>
    <div class="form-actions"><button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button><button type="submit" class="btn btn-primary">${j?'Update':'Post'} Job</button></div>
  </form>`;
}
async function renderJobs() {
  const m = document.getElementById('main-content');
  m.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const data = await api('/jobs');
    m.innerHTML = `<div class="page-header"><div><h1>Job Postings</h1><p>Manage job opportunities</p></div>
    <button class="btn btn-primary" onclick="showAddJob()">+ Post Job</button></div>
    <div class="glass-card"><div class="table-wrapper"><table><thead><tr><th>ID</th><th>Company</th><th>Title</th><th>CTC</th><th>Min CGPA</th><th>Depts</th><th>Interview</th><th>Actions</th></tr></thead>
    <tbody>${data.map(j=>`<tr><td>${j.job_id}</td><td>${j.comp_name}</td><td>${j.job_title}</td><td><span class="ctc-value">${j.ctc} LPA</span></td><td>${j.min_cgpa}</td><td>${j.eligible_depts||'-'}</td><td>${j.interview_date||'-'}</td>
    <td><div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="showEditJob('${j.job_id}')">Edit</button><button class="btn btn-danger btn-sm" onclick="deleteJob('${j.job_id}')">Del</button></div></td></tr>`).join('')}</tbody></table></div></div>`;
  } catch(e) { m.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
async function showAddJob() { openModal('Post New Job', await jobFormHtml()); bindJobForm(); }
async function showEditJob(id) { const j = await api('/jobs/'+id); openModal('Edit Job', await jobFormHtml(j)); bindJobForm(true,id); }
function bindJobForm(isEdit, id) {
  document.getElementById('job-form').onsubmit = async e => {
    e.preventDefault(); const body = Object.fromEntries(new FormData(e.target));
    body.min_cgpa = parseFloat(body.min_cgpa)||0; body.ctc = parseFloat(body.ctc)||0;
    try { if(isEdit) await api('/jobs/'+id,{method:'PUT',body}); else await api('/jobs',{method:'POST',body});
      toast(isEdit?'Job updated':'Job posted'); closeModal(); renderJobs(); } catch(e){toast(e.message,'error');}
  };
}
async function deleteJob(id) { if(!confirm('Delete this job?')) return;
  try { await api('/jobs/'+id,{method:'DELETE'}); toast('Job deleted'); renderJobs(); } catch(e){toast(e.message,'error');} }
