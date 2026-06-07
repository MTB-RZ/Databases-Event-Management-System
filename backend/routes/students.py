from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from db import execute_procedure, fetch_all


students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def list_students():
    search = request.args.get("search", "").strip()
    try:
        if search:
            students = fetch_all(
                "SELECT student_id, name, email, phone FROM students WHERE name LIKE %s ORDER BY student_id DESC",
                (f"%{search}%",),
            )
        else:
            students = fetch_all("SELECT student_id, name, email, phone FROM students ORDER BY student_id DESC")
    except Exception as error:
        students = []
        flash(str(error), "danger")

    return render_template("students.html", students=students, student=None, search=search)


@students_bp.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "").strip()

    if not name or not email or not password:
        flash("Name, email, and password are required.", "danger")
        return redirect(url_for("students.list_students"))

    try:
        execute_procedure("add_student", [name, email, phone, password])
        flash("Student added successfully.", "success")
    except Error as error:
        if error.errno == 1062:
            flash("A student with this email already exists.", "danger")
        else:
            flash(f"Could not add student: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("students.list_students"))


@students_bp.route("/edit/<int:student_id>")
def edit_student(student_id):
    try:
        students = fetch_all("SELECT student_id, name, email, phone FROM students ORDER BY student_id DESC")
        result = execute_procedure("get_student", [student_id], fetch=True)
        if not result:
            flash("Student not found.", "danger")
            return redirect(url_for("students.list_students"))
        student = result[0]
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("students.list_students"))

    return render_template("students.html", students=students, student=student, search="")


@students_bp.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "").strip()

    if not name or not email or not password:
        flash("Name, email, and password are required.", "danger")
        return redirect(url_for("students.edit_student", student_id=student_id))

    try:
        execute_procedure("update_student", [student_id, name, email, phone, password])
        flash("Student updated successfully.", "success")
    except Error as error:
        if error.errno == 1062:
            flash("A student with this email already exists.", "danger")
        else:
            flash(f"Could not update student: {error}", "danger")
        return redirect(url_for("students.edit_student", student_id=student_id))
    except Exception as error:
        flash(str(error), "danger")
        return redirect(url_for("students.edit_student", student_id=student_id))

    return redirect(url_for("students.list_students"))


@students_bp.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        execute_procedure("delete_student", [student_id])
        flash("Student deleted successfully.", "success")
    except Error as error:
        flash(f"Could not delete student. Remove related tickets first. Details: {error}", "danger")
    except Exception as error:
        flash(str(error), "danger")

    return redirect(url_for("students.list_students"))
