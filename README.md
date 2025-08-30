# employee_management_system

A Python-based Command Line Interface (CLI) application for managing employees, departments, and projects using SQLAlchemy ORM and SQLite.

# 📌 About the Project

This project is designed to demonstrate:

How to use Object-Relational Mapping (ORM) with SQLAlchemy.

How to build a CLI tool for managing a company’s employees, departments, and projects.

How data structures like lists, dictionaries, tuples, and strings are applied in real-world software.

# How to design relationships:

One-to-Many → Department → Employees

Many-to-Many → Employees ↔ Projects

# 🚀 Features

Departments

List all departments

Find by name

Create, update, delete

List employees in a department

Employees

List all employees

Find by name or ID

Create, update, delete

Projects

List all projects

Find by name

Create projects

Assign or remove employees from projects

# 📂 Project Structure

employee_management_system/
│── lib/
│ ├── cli.py # CLI entry point
│ ├── helpers.py # CLI helper functions
│ ├── models/ # SQLAlchemy ORM models
│ │ ├── **init**.py # DB engine + session setup
│ │ ├── department.py
│ │ ├── employee.py
│ │ └── project.py
│── company.db # SQLite database
│── Pipfile # Pipenv dependencies
│── README.md # Project documentation

# ⚙️ Setup

Clone the repository:

git clone <your-repo-url>
cd employee_management_system

# Create virtual environment with Pipenv:

pipenv install
pipenv shell

Run the CLI:

python lib/cli.py

# 🖥️ Usage

When you run the CLI, you’ll see the menu:

Please select an option: 0. Exit
--- Departments ---

1. List all departments
2. Find department by name
3. Create department
4. Update department
5. Delete department
6. List employees in a department
   --- Employees ---
7. List all employees
8. Find employee by name
9. Find employee by id
10. Create employee
11. Update employee
12. Delete employee
    --- Projects ---
13. List all projects
14. Find project by name
15. Create project
16. Assign employee to project
17. Remove employee from project

# 🛠️ Data Structures in This Project

Lists
Used when fetching multiple rows (e.g., session.query(Employee).all() returns a list of employees).
Example:

employees = Employee.get_all(session)
for e in employees:
print(e.first_name, e.last_name)

Dictionaries
Used in the ROUTES map in cli.py to connect menu options to functions.

ROUTES = {
"1": list_departments,
"7": list_employees,
"13": list_projects
}
Tuples
Used when returning query results with multiple values or passing grouped values to functions.
Example: (employee_id, project_id) in the junction table.

Strings
Used throughout for names, emails, department locations, project names, etc.
Example: "Peter Munyambu", "papi@gmail.com", "Cloud Migration".

# 📊 Example Output

Listing projects with employees:

+-------------+----------------+----------------------+-----------------+------------+
| Employee ID | Employee Name | Department | Project Name | Budget |
+-------------+----------------+----------------------+-----------------+------------+
| 1 | Peter Munyambu | IT | Cloud Migration | $200000.00 |
+-------------+----------------+----------------------+-----------------+------------+

# Author

peter NM

# license

MIT peter
