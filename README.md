# Event Management System

This is an Event Management System built with Flask, MySQL, Jinja2, Bootstrap 5, HTML, CSS, and JavaScript. The application connects to a local MySQL database named `event_management` and provides a web interface for managing students, venues, events, tickets, and payments.

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
├── README.md
└── .gitignore
```

## Installation Instructions

1. Install the required Python packages:

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
## Running the Application

From inside the `Event_management_system` folder, run:

```powershell
python backend/app.py
```

Then open this address in your browser:

```text
http://127.0.0.1:5000
```

## Notes

- The application uses stored procedures for CRUD operations whenever possible.
- List pages and dropdowns use SELECT queries because the provided stored procedures fetch individual records by ID.
