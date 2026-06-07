# Event Management System

A full-stack Event Management System built with Flask, MySQL, Jinja2, Bootstrap 5, HTML, CSS, and JavaScript. The application connects to a local MySQL database named `event_management` and provides a clean web interface for managing students, venues, events, tickets, and payments.

## Features

- Dashboard with total counts for students, venues, events, tickets, and payments
- Student CRUD with search by name
- Venue CRUD
- Event CRUD with venue dropdown
- Ticket CRUD with student and event dropdowns
- Payment CRUD with ticket dropdown
- Stored procedures used for add, get, update, and delete operations
- Bootstrap success and error alerts
- Delete confirmation popup
- Responsive Bootstrap 5 interface
- User-friendly database error handling

## Technology Stack

- Backend: Python Flask
- Database: MySQL 8.0
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Database Connector: mysql-connector-python
- Template Engine: Jinja2

## Folder Structure

```text
Event_management_system/
├── database/
│   └── event_management.sql
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── routes/
│   │   ├── students.py
│   │   ├── venues.py
│   │   ├── events.py
│   │   ├── tickets.py
│   │   └── payments.py
│   └── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── venues.html
│   ├── events.html
│   ├── tickets.html
│   └── payments.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── README.md
└── .gitignore
```

## Installation Instructions

1. Open the project folder:

```text
C:\Users\mutee\Documents\Codex\2026-06-07\project-event-management-system-flask-mysql\outputs\Event_management_system
```

2. Open PowerShell or Command Prompt in this folder.

3. Install the required Python packages:

```powershell
pip install -r backend/requirements.txt
```

## Database Setup

1. Open MySQL Workbench.

2. Open this file:

```text
database/event_management.sql
```

3. Run the full SQL script.

4. Confirm that the database name is:

```text
event_management
```

5. Open this file:

```text
backend/db.py
```

6. Replace `YOUR_PASSWORD` with your MySQL root password:

```python
"password": os.getenv("DB_PASSWORD", "YOUR_PASSWORD"),
```

Example:

```python
"password": os.getenv("DB_PASSWORD", "12345"),
```

## Running the Application

From inside the `Event_management_system` folder, run:

```powershell
python backend/app.py
```

Then open this address in your browser:

```text
http://127.0.0.1:5000
```

## Recommended Demo Order

1. Add venues first.
2. Add students.
3. Add events and select venues.
4. Add tickets and select students/events.
5. Add payments and select tickets.
6. Show the dashboard count cards.
7. Demonstrate edit and delete operations.

## Screenshots

Add screenshots of the following pages here after running the project:

- Dashboard
- Students page
- Venues page
- Events page
- Tickets page
- Payments page

## Notes

- The application uses stored procedures for CRUD operations whenever possible.
- List pages and dropdowns use SELECT queries because the provided stored procedures fetch individual records by ID.
- If a delete fails, check whether related records exist. For example, a student with tickets cannot be deleted until related tickets are removed.
