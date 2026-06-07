from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from db import execute_procedure, fetch_all


venues_bp = Blueprint("venues", __name__, url_prefix="/venues")


@venues_bp.route("/")
def list_venues():
    try:
        venues = fetch_all("SELECT venue_id, venue_name, location, capacity FROM venues ORDER BY venue_id DESC")
    except Exception as error:
        venues = []
        flash(str(error), "danger")

    return render_template("venues.html", venues=venues, venue=None)


@venues_bp.route("/add", methods=["POST"])
def add_venue():
    venue_name = request.form.get("venue_name", "").strip()
    location = request.form.get("location", "").strip()
    capacity = request.form.get("capacity", "").strip()

    if not venue_name or not location or not capacity:
        flash("Venue name, location, and capacity are required.", "danger")
        return redirect(url_for("venues.list_venues"))

    try:
        execute_procedure("add_venue", [venue_name, location, int(capacity)])
        flash("Venue added successfully.", "success")
    except ValueError:
        flash("Capacity must be a valid number.", "danger")
    except Error as error:
        flash(f"Could not add venue: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("venues.list_venues"))


@venues_bp.route("/edit/<int:venue_id>")
def edit_venue(venue_id):
    try:
        venues = fetch_all("SELECT venue_id, venue_name, location, capacity FROM venues ORDER BY venue_id DESC")
        result = execute_procedure("get_venue", [venue_id], fetch=True)
        if not result:
            flash("Venue not found.", "danger")
            return redirect(url_for("venues.list_venues"))
        venue = result[0]
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("venues.list_venues"))

    return render_template("venues.html", venues=venues, venue=venue)


@venues_bp.route("/update/<int:venue_id>", methods=["POST"])
def update_venue(venue_id):
    venue_name = request.form.get("venue_name", "").strip()
    location = request.form.get("location", "").strip()
    capacity = request.form.get("capacity", "").strip()

    if not venue_name or not location or not capacity:
        flash("Venue name, location, and capacity are required.", "danger")
        return redirect(url_for("venues.edit_venue", venue_id=venue_id))

    try:
        execute_procedure("update_venue", [venue_id, venue_name, location, int(capacity)])
        flash("Venue updated successfully.", "success")
    except ValueError:
        flash("Capacity must be a valid number.", "danger")
        return redirect(url_for("venues.edit_venue", venue_id=venue_id))
    except Error as error:
        flash(f"Could not update venue: {error}", "danger")
        return redirect(url_for("venues.edit_venue", venue_id=venue_id))
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("venues.edit_venue", venue_id=venue_id))

    return redirect(url_for("venues.list_venues"))


@venues_bp.route("/delete/<int:venue_id>", methods=["POST"])
def delete_venue(venue_id):
    try:
        execute_procedure("delete_venue", [venue_id])
        flash("Venue deleted successfully.", "success")
    except Error as error:
        flash(f"Could not delete venue: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("venues.list_venues"))
