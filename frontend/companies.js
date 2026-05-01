function companyForm(c) {
  return `<form id="company-form" class="form-grid">
    <div class="form-group"><label class="form-label">Company ID</label><input class="form-input" name="comp_id" value="${c?.comp_id||''}" ${c?'readonly':'required'}></div>
    <div class="form-group"><label class="form-label">Company Name</label><input class="form-input" name="comp_name" value="${c?.comp_name||''}" required></div>
    <div class="form-group"><label class="form-label">Industry Type</label><select class="form-select" name="industry_type"><option value="">Select</option>${['IT','Finance','Core Engineering','Consulting'].map(t=>`<option ${c?.industry_type===t?'selected':''}>${t}</option>`).join('')}</select></div>
    <div class="form-group"><label class="form-label">HR Name</label><input class="form-input" name="hr_name" value="${c?.hr_name||''}"></div>
    <div class="form-group"><label class="form-label">HR Email</label><input class="form-input" type="email" name="hr_email" value="${c?.hr_email||''}"></div>
    <div class="form-group"><label class="form-label">HR Phone</label><input class="form-input" name="hr_phone" value="${c?.hr_phone||''}"></div>
    <div class="form-actions"><button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button><button type="submit" class="btn btn-primary">${c?'Update':'Register'}</button></div>
  </form>`;
}
async function renderCompanies() {
  const m = document.getElementById('main-content');
  m.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const data = await api('/companies');
    m.innerHTML = `<div class="page-header"><div><h1>Companies</h1><p>Manage recruiting companies</p></div>
    <button class="btn btn-primary" onclick="showAddCompany()">+ Add Company</button></div>
    <div class="glass-card"><div class="table-wrapper"><table><thead><tr><th>ID</th><th>Company</th><th>Industry</th><th>HR Contact</th><th>Email</th><th>Actions</th></tr></thead>
    <tbody>${data.map(c=>`<tr><td>${c.comp_id}</td><td>${c.comp_name}</td><td>${c.industry_type||'-'}</td><td>${c.hr_name||'-'}</td><td>${c.hr_email||'-'}</td>
    <td><div class="btn-group"><button class="btn btn-secondary btn-sm" onclick="showEditCompany('${c.comp_id}')">Edit</button><button class="btn btn-danger btn-sm" onclick="deleteCompany('${c.comp_id}')">Del</button></div></td></tr>`).join('')}</tbody></table></div></div>`;
  } catch(e) { m.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
function showAddCompany() { openModal('Register Company', companyForm()); bindCompanyForm(); }
async function showEditCompany(id) { const c = await api('/companies/'+id); openModal('Edit Company', companyForm(c)); bindCompanyForm(true, id); }
function bindCompanyForm(isEdit, id) {
  document.getElementById('company-form').onsubmit = async e => {
    e.preventDefault(); const body = Object.fromEntries(new FormData(e.target));
    try { if(isEdit) await api('/companies/'+id,{method:'PUT',body}); else await api('/companies',{method:'POST',body});
      toast(isEdit?'Company updated':'Company registered'); closeModal(); renderCompanies(); } catch(e){toast(e.message,'error');}
  };
}
async function deleteCompany(id) { if(!confirm('Delete this company and all its jobs?')) return;
  try { await api('/companies/'+id,{method:'DELETE'}); toast('Company deleted'); renderCompanies(); } catch(e){toast(e.message,'error');} }
