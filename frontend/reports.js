let currentReport = 'placement';
async function renderReports() {
  const m = document.getElementById('main-content');
  m.innerHTML = `<div class="page-header"><div><h1>Reports</h1><p>Placement analytics &amp; queries</p></div></div>
  <div class="tab-nav">
    <button class="tab-btn ${currentReport==='placement'?'active':''}" onclick="currentReport='placement';renderReports()">Placement Status</button>
    <button class="tab-btn ${currentReport==='eligible'?'active':''}" onclick="currentReport='eligible';renderReports()">Eligible Jobs</button>
    <button class="tab-btn ${currentReport==='unplaced'?'active':''}" onclick="currentReport='unplaced';renderReports()">Unplaced (8+ CGPA)</button>
    <button class="tab-btn ${currentReport==='company'?'active':''}" onclick="currentReport='company';renderReports()">Jobs per Company</button>
    <button class="tab-btn ${currentReport==='upgrade'?'active':''}" onclick="currentReport='upgrade';renderReports()">CTC Upgrade</button>
  </div><div id="report-content"><div class="loading"><div class="spinner"></div></div></div>`;
  const rc = document.getElementById('report-content');
  try {
    if (currentReport==='placement') {
      const d = await api('/reports/placement-status');
      rc.innerHTML = `<div class="stats-grid">
        <div class="stat-card"><div class="stat-label">Total Offers</div><div class="stat-value">${d.total_offers}</div></div>
        <div class="stat-card accent-2"><div class="stat-label">Placed</div><div class="stat-value">${d.placed_count}/${d.total_students}</div><div class="stat-sub">${d.placement_percentage}%</div></div>
        <div class="stat-card accent-3"><div class="stat-label">Unplaced</div><div class="stat-value">${d.unplaced_count}</div></div></div>
      <div class="glass-card"><h2>Placed Students</h2><div class="table-wrapper"><table><thead><tr><th>Roll No</th><th>Name</th><th>Dept</th><th>Company</th><th>Job Title</th><th>CTC</th></tr></thead>
      <tbody>${d.placed_students.map(s=>`<tr><td>${s.roll_no}</td><td>${s.name}</td><td>${s.dept}</td><td>${s.comp_name}</td><td>${s.job_title}</td><td class="ctc-value">${s.ctc} LPA</td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (currentReport==='eligible') {
      rc.innerHTML = `<div class="glass-card"><h2>Check Eligible Jobs for a Student</h2>
        <div class="search-bar"><input class="search-input" id="elig-roll" placeholder="Enter Roll Number (e.g. 23103027)" style="max-width:300px">
        <button class="btn btn-primary" onclick="checkEligible()">Check</button></div><div id="elig-result"></div></div>`;
    } else if (currentReport==='unplaced') {
      const d = await api('/reports/unplaced-eligible');
      rc.innerHTML = `<div class="glass-card"><h2>Unplaced Students with CGPA ≥ 8.0</h2>
      <div class="table-wrapper"><table><thead><tr><th>Roll No</th><th>Name</th><th>Dept</th><th>CGPA</th></tr></thead>
      <tbody>${d.map(s=>`<tr><td>${s.roll_no}</td><td>${s.name}</td><td>${s.dept}</td><td>${s.cgpa}</td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (currentReport==='company') {
      const d = await api('/reports/company-job-counts');
      rc.innerHTML = `<div class="glass-card"><h2>Jobs per Company</h2>
      <div class="table-wrapper"><table><thead><tr><th>Company ID</th><th>Company Name</th><th>Job Count</th></tr></thead>
      <tbody>${d.map(c=>`<tr><td>${c.comp_id}</td><td>${c.comp_name}</td><td><span class="ctc-value">${c.job_count}</span></td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (currentReport==='upgrade') {
      const d = await api('/reports/ctc-upgrade-eligibility');
      rc.innerHTML = `<div class="glass-card"><h2>CTC Upgrade Eligibility (Dream Offer)</h2><p class="text-muted mb-1">Placed students eligible for jobs with CTC ≥ current + 2.5 LPA</p>
      <div class="table-wrapper"><table><thead><tr><th>Roll No</th><th>Name</th><th>Current CTC</th><th>Job</th><th>Company</th><th>New CTC</th></tr></thead>
      <tbody>${d.map(r=>`<tr><td>${r.roll_no}</td><td>${r.name}</td><td>${r.current_highest_ctc} LPA</td><td>${r.job_title} <span class="dream-badge">DREAM</span></td><td>${r.comp_name}</td><td class="ctc-value">${r.new_ctc} LPA</td></tr>`).join('')}</tbody></table></div></div>`;
    }
  } catch(e) { rc.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
async function checkEligible() {
  const roll = document.getElementById('elig-roll').value.trim();
  if (!roll) { toast('Enter a roll number','error'); return; }
  const er = document.getElementById('elig-result');
  try {
    const d = await api('/jobs/eligible/'+roll);
    er.innerHTML = `<p class="mt-1">Showing results for <strong>${d.student.name}</strong> (${d.student.placement_status}, CTC: ${d.student.current_highest_ctc} LPA)</p>
    <div class="table-wrapper mt-1"><table><thead><tr><th>Job ID</th><th>Company</th><th>Title</th><th>CTC</th><th>Type</th></tr></thead>
    <tbody>${d.eligible_jobs.length ? d.eligible_jobs.map(j=>`<tr><td>${j.job_id}</td><td>${j.comp_name}</td><td>${j.job_title}</td><td class="ctc-value">${j.ctc} LPA</td><td>${j.is_dream_offer?'<span class="dream-badge">DREAM</span>':'Regular'}</td></tr>`).join('') : '<tr><td colspan="5" class="text-muted">No eligible jobs found</td></tr>'}</tbody></table></div>`;
  } catch(e) { er.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
