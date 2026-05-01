# Campus Placement Management System

A full-stack web application for managing campus placements, built as a Database Management System case study. The system handles student registrations, company profiles, job postings, and applications — with enforcement of the institute's **"Dream Offer" (2.5 LPA Upgrade) Rule**.

---

## Features

### Core Operations
- **Student Management** — Register, update, and track students with academic details (CGPA, 10th/12th %, core skills)
- **Company Management** — Maintain recruiting company profiles with HR contact details
- **Job Postings** — Companies post jobs with CTC, minimum CGPA, eligible departments, and interview dates
- **Application System** — Students apply to jobs with real-time eligibility validation

### Business Logic
- **Dream Offer Rule** — A placed student can only apply to a new job if the CTC is ≥ current highest CTC + 2.5 LPA
- **Auto Placement Updates** — Student status and highest CTC are automatically updated when an offer is accepted
- **Eligibility Enforcement** — CGPA, department, and placement status checks on every application
- **Offer Limit** — Maximum 2 offers per student (1 standard + 1 dream)

### Reports & Analytics
- **Dashboard** — Live placement statistics at a glance
- **Placement Status Report** — All placed students with offer details
- **Eligible Jobs Checker** — Find jobs a specific student qualifies for
- **Unplaced High-CGPA Students** — Alphabetical list of unplaced students with CGPA ≥ 8.0
- **Jobs per Company** — Aggregated job count by company
- **CTC Upgrade Eligibility** — Placed students eligible for Dream Offers

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python Flask (REST API) |
| **Database** | SQLite |
| **Design** | Dark-mode glassmorphism, Inter font |

---

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
# Clone the repository
git clone https://github.com/Thiy3640/campus_placement_management_system.git
cd campus_placement_management_system

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The server starts at **http://localhost:5000** and opens automatically in your browser.

---

## 📁 Project Structure

```
campus_placement_management_system/
├── run.py                      # Entry point
├── requirements.txt            # Python dependencies
├── placement.db                # SQLite database (auto-created)
├── backend/
│   ├── app.py                  # Flask application factory
│   ├── database.py             # Schema creation & seed data
│   └── routes/
│       ├── students.py         # Student CRUD endpoints
│       ├── companies.py        # Company CRUD endpoints
│       ├── jobs.py             # Job CRUD + eligibility queries
│       ├── applications.py     # Application logic + Dream Offer validation
│       └── reports.py          # Reports & dashboard statistics
└── frontend/
    ├── index.html              # SPA shell with sidebar navigation
    ├── styles.css              # Dark-mode glassmorphism design system
    ├── api.js                  # API utility layer
    ├── app.js                  # SPA hash-based router
    ├── dashboard.js            # Dashboard page
    ├── students.js             # Students CRUD page
    ├── companies.js            # Companies CRUD page
    ├── jobs.js                 # Jobs CRUD page
    ├── applications.js         # Applications page
    └── reports.js              # Reports with tabbed navigation
```

---

## Database Schema

Based on the ER model with BCNF normalization:

- **STUDENT** — `roll_no` (PK), name, dob, gender, phone, email, dept, cgpa, tenth_pct, twelfth_pct, core_skills, placement_status, current_highest_ctc
- **COMPANY** — `comp_id` (PK), comp_name, industry_type, hr_name, hr_email, hr_phone
- **JOB** — `job_id` (PK), `comp_id` (FK), job_title, job_desc, min_cgpa, ctc, eligible_depts, interview_date
- **APPLICATION** — `app_id` (PK), `roll_no` (FK), `job_id` (FK), app_date, app_status

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | List all students |
| POST | `/api/students` | Register a student |
| GET | `/api/companies` | List all companies |
| POST | `/api/companies` | Register a company |
| GET | `/api/jobs` | List all jobs |
| POST | `/api/jobs` | Post a new job |
| GET | `/api/jobs/eligible/:roll_no` | Eligible jobs for a student |
| GET | `/api/applications` | List all applications |
| POST | `/api/applications` | Submit application (with validation) |
| PUT | `/api/applications/:id/status` | Update application status |
| GET | `/api/reports/dashboard` | Dashboard statistics |
| GET | `/api/reports/placement-status` | Placement report |
| GET | `/api/reports/unplaced-eligible` | Unplaced students (CGPA ≥ 8) |
| GET | `/api/reports/company-job-counts` | Jobs per company |
| GET | `/api/reports/ctc-upgrade-eligibility` | Dream offer eligibility |

---

## Created By

- **Thiyam Chingu Robaartt**
- **Robertson Athokpam**

---

## License

This project is developed as an academic case study for Database Management Systems.
