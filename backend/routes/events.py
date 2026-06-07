from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from db import execute_procedure, fetch_all


events_bp = Blueprint("events", __name__, url_prefix="/events")


def get_event_page_data():
    events = fetch_all(
        """
        SELECT e.event_id, e.title, e.event_date, e.ticket_price, e.venue_id, v.venue_name
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        ORDER BY e.event_id DESC
        """
    )
    venues = fetch_all("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
    return events, venues


@events_bp.route("/")
def list_events():
    try:
        events, venues = get_event_page_data()
    except Exception as error:
        events, venues = [], []
        flash(str(error), "danger")

    return render_template("events.html", events=events, venues=venues, event=None)


@events_bp.route("/add", methods=["POST"])
def add_event():
    title = request.form.get("title", "").strip()
    event_date = request.form.get("event_date", "").strip()
    ticket_price = request.form.get("ticket_price", "").strip()
    venue_id = request.form.get("venue_id", "").strip()

    if not title or not event_date or not ticket_price or not venue_id:
        flash("Title, event date, ticket price, and venue are required.", "danger")
        return redirect(url_for("events.list_events"))

    try:
        execute_procedure("add_event", [title, event_date, float(ticket_price), int(venue_id)])
        flash("Event added successfully.", "success")
    except ValueError:
        flash("Ticket price and venue must be valid numbers.", "danger")
    except Error as error:
        flash(f"Could not add event: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("events.list_events"))


@events_bp.route("/edit/<int:event_id>")
def edit_event(event_id):
    try:
        events, venues = get_event_page_data()
        result = execute_procedure("get_event", [event_id], fetch=True)
        if not result:
            flash("Event not found.", "danger")
            return redirect(url_for("events.list_events"))
        event = result[0]
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("events.list_events"))

    return render_template("events.html", events=events, venues=venues, event=event)


@events_bp.route("/update/<int:event_id>", methods=["POST"])
def update_event(event_id):
    title = request.form.get("title", "").strip()
    event_date = request.form.get("event_date", "").strip()
    ticket_price = request.form.get("ticket_price", "").strip()
    venue_id = request.form.get("venue_id", "").strip()

    if not title or not event_date or not ticket_price or not venue_id:
        flash("Title, event date, ticket price, and venue are required.", "danger")
        return redirect(url_for("events.edit_event", event_id=event_id))

    try:
        execute_procedure("update_event", [event_id, title, event_date, float(ticket_price), int(venue_id)])
        flash("Event updated successfully.", "success")
    except ValueError:
        flash("Ticket price and venue must be valid numbers.", "danger")
        return redirect(url_for("events.edit_event", event_id=event_id))
    except Error as error:
        flash(f"Could not update event: {error}", "danger")
        return redirect(url_for("events.edit_event", event_id=event_id))
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("events.edit_event", event_id=event_id))

    return redirect(url_for("events.list_events"))


@events_bp.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    try:
        execute_procedure("delete_event", [event_id])
        flash("Event deleted successfully.", "success")
    except Error as error:
        flash(f"Could not delete event. Remove related tickets first. Details: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("events.list_events"))
