from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from db import execute_procedure, fetch_all


tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")


def get_ticket_page_data():
    tickets = fetch_all(
        """
        SELECT t.ticket_id, t.student_id, t.event_id, s.name AS student_name, e.title AS event_name,
               t.quantity, t.booking_date
        FROM tickets t
        JOIN students s ON t.student_id = s.student_id
        JOIN events e ON t.event_id = e.event_id
        ORDER BY t.ticket_id DESC
        """
    )
    students = fetch_all("SELECT student_id, name FROM students ORDER BY name")
    events = fetch_all("SELECT event_id, title FROM events ORDER BY title")
    return tickets, students, events


@tickets_bp.route("/")
def list_tickets():
    try:
        tickets, students, events = get_ticket_page_data()
    except Exception as error:
        tickets, students, events = [], [], []
        flash(str(error), "danger")

    return render_template("tickets.html", tickets=tickets, students=students, events=events, ticket=None)


@tickets_bp.route("/add", methods=["POST"])
def add_ticket():
    student_id = request.form.get("student_id", "").strip()
    event_id = request.form.get("event_id", "").strip()
    quantity = request.form.get("quantity", "").strip()
    booking_date = request.form.get("booking_date", "").strip()

    if not student_id or not event_id or not quantity or not booking_date:
        flash("Student, event, quantity, and booking date are required.", "danger")
        return redirect(url_for("tickets.list_tickets"))

    try:
        quantity_value = int(quantity)
        if quantity_value <= 0:
            flash("Quantity must be greater than zero.", "danger")
            return redirect(url_for("tickets.list_tickets"))
        execute_procedure("add_ticket", [int(student_id), int(event_id), quantity_value, booking_date])
        flash("Ticket added successfully.", "success")
    except ValueError:
        flash("Student, event, and quantity must be valid numbers.", "danger")
    except Error as error:
        flash(f"Could not add ticket: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("tickets.list_tickets"))


@tickets_bp.route("/edit/<int:ticket_id>")
def edit_ticket(ticket_id):
    try:
        tickets, students, events = get_ticket_page_data()
        result = execute_procedure("get_tickets", [ticket_id], fetch=True)
        if not result:
            flash("Ticket not found.", "danger")
            return redirect(url_for("tickets.list_tickets"))
        ticket = result[0]
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("tickets.list_tickets"))

    return render_template("tickets.html", tickets=tickets, students=students, events=events, ticket=ticket)


@tickets_bp.route("/update/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):
    quantity = request.form.get("quantity", "").strip()

    if not quantity:
        flash("Quantity is required.", "danger")
        return redirect(url_for("tickets.edit_ticket", ticket_id=ticket_id))

    try:
        quantity_value = int(quantity)
        if quantity_value <= 0:
            flash("Quantity must be greater than zero.", "danger")
            return redirect(url_for("tickets.edit_ticket", ticket_id=ticket_id))
        execute_procedure("update_ticket", [ticket_id, quantity_value])
        flash("Ticket updated successfully.", "success")
    except ValueError:
        flash("Quantity must be a valid number.", "danger")
        return redirect(url_for("tickets.edit_ticket", ticket_id=ticket_id))
    except Error as error:
        flash(f"Could not update ticket: {error}", "danger")
        return redirect(url_for("tickets.edit_ticket", ticket_id=ticket_id))
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("tickets.edit_ticket", ticket_id=ticket_id))

    return redirect(url_for("tickets.list_tickets"))


@tickets_bp.route("/delete/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    try:
        execute_procedure("delete_ticket", [ticket_id])
        flash("Ticket deleted successfully.", "success")
    except Error as error:
        flash(f"Could not delete ticket. Remove related payments first. Details: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("tickets.list_tickets"))
