"""
Campus Placement Management System — Flask Application
Main entry point for the REST API server.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from routes.students import students_bp
from routes.companies import companies_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.reports import reports_bp


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend'),
        static_url_path=''
    )
    CORS(app)

    # ── Register Blueprints ──────────────────────────────────────
    app.register_blueprint(students_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(reports_bp)

    # ── Serve Frontend ───────────────────────────────────────────
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')

    return app


if __name__ == '__main__':
    from database import init_db
    init_db()
    app = create_app()
    app.run(debug=True, port=5000)
