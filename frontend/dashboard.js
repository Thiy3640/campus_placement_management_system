async function renderDashboard() {
  const m = document.getElementById('main-content');
  m.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
  try {
    const d = await api('/reports/dashboard');
    m.innerHTML = `
    <div class="page-header"><div><h1>Dashboard</h1><p>Campus Placement Overview</p></div></div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-label">Total Students</div><div class="stat-value">${d.total_students}</div></div>
      <div class="stat-card accent-2"><div class="stat-label">Placed</div><div class="stat-value">${d.placed_students}</div><div class="stat-sub">${d.placement_rate}% placement rate</div></div>
      <div class="stat-card accent-3"><div class="stat-label">Companies</div><div class="stat-value">${d.total_companies}</div></div>
      <div class="stat-card"><div class="stat-label">Active Jobs</div><div class="stat-value">${d.total_jobs}</div></div>
      <div class="stat-card accent-2"><div class="stat-label">Applications</div><div class="stat-value">${d.total_applications}</div><div class="stat-sub">${d.pending_applications} pending</div></div>
      <div class="stat-card accent-3"><div class="stat-label">Avg CTC</div><div class="stat-value">${d.avg_ctc}</div><div class="stat-sub">LPA | Highest: ${d.highest_ctc} LPA</div></div>
    </div>`;
  } catch(e) { m.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`; }
}
