from pathlib import Path
from flask import Flask, flash, render_template
from db import fetch_one

from routes.students import students_bp
from routes.venues import venues_bp
from routes.events import events_bp
from routes.tickets import tickets_bp
from routes.payments import payments_bp


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app():
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.secret_key = "event-management-secret-key"

    app.register_blueprint(students_bp)
    app.register_blueprint(venues_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(payments_bp)

    @app.route("/")
    def index():
        counts = {
            "students": 0,
            "venues": 0,
            "events": 0,
            "tickets": 0,
            "payments": 0,
        }

        try:
            counts["students"] = fetch_one("SELECT COUNT(*) AS total FROM students")["total"]
            counts["venues"] = fetch_one("SELECT COUNT(*) AS total FROM venues")["total"]
            counts["events"] = fetch_one("SELECT COUNT(*) AS total FROM events")["total"]
            counts["tickets"] = fetch_one("SELECT COUNT(*) AS total FROM tickets")["total"]
            counts["payments"] = fetch_one("SELECT COUNT(*) AS total FROM payments")["total"]
        except Exception as error:
            flash(str(error), "danger")

        return render_template("index.html", counts=counts)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
