/* SPA Router — ties all page modules together */
const pages = { dashboard: renderDashboard, students: renderStudents, companies: renderCompanies, jobs: renderJobs, applications: renderApplications, reports: renderReports };

function navigate(page) {
  document.querySelectorAll('.nav-link').forEach(l => l.classList.toggle('active', l.dataset.page === page));
  if (pages[page]) pages[page]();
}

window.addEventListener('hashchange', () => navigate(location.hash.slice(1) || 'dashboard'));
window.addEventListener('DOMContentLoaded', () => navigate(location.hash.slice(1) || 'dashboard'));
