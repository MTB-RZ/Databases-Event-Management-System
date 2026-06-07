from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from db import execute_procedure, fetch_all


payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


def get_payment_page_data():
    payments = fetch_all(
        """
        SELECT p.payment_id, p.ticket_id, s.name AS student_name, e.title AS event_name,
               p.amount, p.payment_method, p.payment_date
        FROM payments p
        JOIN tickets t ON p.ticket_id = t.ticket_id
        JOIN students s ON t.student_id = s.student_id
        JOIN events e ON t.event_id = e.event_id
        ORDER BY p.payment_id DESC
        """
    )
    tickets = fetch_all(
        """
        SELECT t.ticket_id, s.name AS student_name, e.title AS event_name
        FROM tickets t
        JOIN students s ON t.student_id = s.student_id
        JOIN events e ON t.event_id = e.event_id
        ORDER BY t.ticket_id DESC
        """
    )
    return payments, tickets


@payments_bp.route("/")
def list_payments():
    try:
        payments, tickets = get_payment_page_data()
    except Exception as error:
        payments, tickets = [], []
        flash(str(error), "danger")

    return render_template("payments.html", payments=payments, tickets=tickets, payment=None)


@payments_bp.route("/add", methods=["POST"])
def add_payment():
    ticket_id = request.form.get("ticket_id", "").strip()
    amount = request.form.get("amount", "").strip()
    payment_method = request.form.get("payment_method", "").strip()
    payment_date = request.form.get("payment_date", "").strip()

    if not ticket_id or not amount or not payment_method or not payment_date:
        flash("Ticket, amount, payment method, and payment date are required.", "danger")
        return redirect(url_for("payments.list_payments"))

    try:
        amount_value = float(amount)
        if amount_value <= 0:
            flash("Amount must be greater than zero.", "danger")
            return redirect(url_for("payments.list_payments"))
        execute_procedure("add_payment", [int(ticket_id), amount_value, payment_method, payment_date])
        flash("Payment added successfully.", "success")
    except ValueError:
        flash("Ticket and amount must be valid numbers.", "danger")
    except Error as error:
        flash(f"Could not add payment: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("payments.list_payments"))


@payments_bp.route("/edit/<int:payment_id>")
def edit_payment(payment_id):
    try:
        payments, tickets = get_payment_page_data()
        result = execute_procedure("get_payments", [payment_id], fetch=True)
        if not result:
            flash("Payment not found.", "danger")
            return redirect(url_for("payments.list_payments"))
        payment = result[0]
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("payments.list_payments"))

    return render_template("payments.html", payments=payments, tickets=tickets, payment=payment)


@payments_bp.route("/update/<int:payment_id>", methods=["POST"])
def update_payment(payment_id):
    amount = request.form.get("amount", "").strip()
    payment_method = request.form.get("payment_method", "").strip()

    if not amount or not payment_method:
        flash("Amount and payment method are required.", "danger")
        return redirect(url_for("payments.edit_payment", payment_id=payment_id))

    try:
        amount_value = float(amount)
        if amount_value <= 0:
            flash("Amount must be greater than zero.", "danger")
            return redirect(url_for("payments.edit_payment", payment_id=payment_id))
        execute_procedure("update_payment", [payment_id, amount_value, payment_method])
        flash("Payment updated successfully.", "success")
    except ValueError:
        flash("Amount must be a valid number.", "danger")
        return redirect(url_for("payments.edit_payment", payment_id=payment_id))
    except Error as error:
        flash(f"Could not update payment: {error}", "danger")
        return redirect(url_for("payments.edit_payment", payment_id=payment_id))
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("payments.edit_payment", payment_id=payment_id))

    return redirect(url_for("payments.list_payments"))


@payments_bp.route("/delete/<int:payment_id>", methods=["POST"])
def delete_payment(payment_id):
    try:
        execute_procedure("delete_payment", [payment_id])
        flash("Payment deleted successfully.", "success")
    except Error as error:
        flash(f"Could not delete payment: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("payments.list_payments"))
