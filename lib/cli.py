# lib/cli.py
from helpers import (
    exit_program,

    # Departments
    list_departments, find_department_by_name, create_department,
    update_department, delete_department, list_department_employees,

    # Employees
    list_employees, find_employee_by_name, find_employee_by_id,
    create_employee, update_employee, delete_employee,

    # Projects
    list_projects, find_project_by_name, create_project,
    assign_employee_to_project, remove_employee_from_project,
)
from models import init_db

MENU = """
Please select an option:
0. Exit
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
"""

ROUTES = {
    "0": exit_program,

    "1": list_departments,
    "2": find_department_by_name,
    "3": create_department,
    "4": update_department,
    "5": delete_department,
    "6": list_department_employees,

    "7": list_employees,
    "8": find_employee_by_name,
    "9": find_employee_by_id,
    "10": create_employee,
    "11": update_employee,
    "12": delete_employee,

    "13": list_projects,
    "14": find_project_by_name,
    "15": create_project,
    "16": assign_employee_to_project,
    "17": remove_employee_from_project,
}

def main():
    init_db()
    print("Welcome to the Employee Management System (EMS)")
    while True:
        print(MENU)
        choice = input("> ").strip()
        action = ROUTES.get(choice)
        if action:
            try:
                action()
            except SystemExit:
                print("Exited.")
                break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
