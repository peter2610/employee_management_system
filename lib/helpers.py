# lib/helpers.py
from tabulate import tabulate
from models import Session
from models.department import Department
from models.employee import Employee
from models.project import Project

# ---------- Utility ----------
def _get_session():
    return Session()

def _ask(prompt):
    return input(prompt).strip()

# ---------- Department actions ----------
def list_departments():
    with _get_session() as s:
        deps = Department.get_all(s)
        if not deps:
            print("(no records)")
        else:
            table = [(d.id, d.name, d.location) for d in deps]
            print(tabulate(table, headers=["ID", "Name", "Location"], tablefmt="grid"))

def find_department_by_name():
    name = _ask("Enter the department's name: ")
    with _get_session() as s:
        d = Department.find_by_name(s, name)
        if d:
            table = [(d.id, d.name, d.location)]
            print(tabulate(table, headers=["ID", "Name", "Location"], tablefmt="grid"))
        else:
            print(f"Department '{name}' not found")

def create_department():
    name = _ask("Enter the department's name: ")
    location = _ask("Enter the department's location: ")
    with _get_session() as s:
        try:
            d = Department.create(s, name=name, location=location)
            table = [(d.id, d.name, d.location)]
            print(tabulate(table, headers=["ID", "Name", "Location"], tablefmt="grid"))
        except Exception as e:
            s.rollback()
            print("Error creating department:", e)

def update_department():
    id_ = _ask("Enter the department's id: ")
    with _get_session() as s:
        d = Department.find_by_id(s, id_)
        if not d:
            print(f"Department {id_} not found")
            return
        try:
            name = _ask("Enter the department's new name: ")
            location = _ask("Enter the department's new location: ")
            d.update(s, name=name, location=location)
            table = [(d.id, d.name, d.location)]
            print(tabulate(table, headers=["ID", "Name", "Location"], tablefmt="grid"))
        except Exception as e:
            s.rollback()
            print("Error updating department:", e)

def delete_department():
    id_ = _ask("Enter the department's id: ")
    with _get_session() as s:
        d = Department.find_by_id(s, id_)
        if not d:
            print(f"Department {id_} not found")
            return
        d.delete(s)
        print(f"Department {id_} deleted")

def list_department_employees():
    id_ = _ask("Enter the department's id: ")
    with _get_session() as s:
        d = Department.find_by_id(s, id_)
        if not d:
            print(f"Department {id_} not found")
            return
        if not d.employees:
            print("(no employees in this department)")
        else:
            table = [
                (e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}")
                for e in d.employees
            ]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary"], tablefmt="grid"))

# ---------- Employee actions ----------
def list_employees():
    with _get_session() as s:
        emps = Employee.get_all(s)
        if not emps:
            print("(no records)")
        else:
            table = [(e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}", e.department_id) for e in emps]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary", "Dept ID"], tablefmt="grid"))

def find_employee_by_name():
    name = _ask("Enter the employee's name (First Last or either): ")
    with _get_session() as s:
        e = Employee.find_by_name(s, name)
        if e:
            table = [(e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}", e.department_id)]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary", "Dept ID"], tablefmt="grid"))
        else:
            print(f"Employee '{name}' not found")

def find_employee_by_id():
    id_ = _ask("Enter the employee's id: ")
    with _get_session() as s:
        e = Employee.find_by_id(s, id_)
        if e:
            table = [(e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}", e.department_id)]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary", "Dept ID"], tablefmt="grid"))
        else:
            print(f"Employee {id_} not found")

def create_employee():
    first = _ask("Enter the employee's first name: ")
    last = _ask("Enter the employee's last name: ")
    email = _ask("Enter the employee's email: ")
    salary = _ask("Enter the employee's salary: ")
    dept_id = _ask("Enter the employee's department id: ")
    with _get_session() as s:
        try:
            d = Department.find_by_id(s, dept_id)
            if not d:
                print("Error: department_id must reference an existing department")
                return
            e = Employee.create(
                s,
                first_name=first,
                last_name=last,
                email=email,
                salary=salary,
                department_id=d.id,
            )
            table = [(e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}", e.department_id)]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary", "Dept ID"], tablefmt="grid"))
        except Exception as ex:
            s.rollback()
            print("Error creating employee:", ex)

def update_employee():
    id_ = _ask("Enter the employee's id: ")
    with _get_session() as s:
        e = Employee.find_by_id(s, id_)
        if not e:
            print(f"Employee {id_} not found")
            return
        try:
            first = _ask("Enter the employee's new first name: ")
            last = _ask("Enter the employee's new last name: ")
            email = _ask("Enter the employee's new email: ")
            salary = _ask("Enter the employee's new salary: ")
            dept_id = _ask("Enter the employee's new department id: ")
            d = Department.find_by_id(s, dept_id)
            if not d:
                print("Error: department_id must reference an existing department")
                return
            e.update(
                s,
                first_name=first,
                last_name=last,
                email=email,
                salary=salary,
                department_id=d.id,
            )
            table = [(e.id, e.first_name, e.last_name, e.email, f"${e.salary:.2f}", e.department_id)]
            print(tabulate(table, headers=["ID", "First Name", "Last Name", "Email", "Salary", "Dept ID"], tablefmt="grid"))
        except Exception as ex:
            s.rollback()
            print("Error updating employee:", ex)

def delete_employee():
    id_ = _ask("Enter the employee's id: ")
    with _get_session() as s:
        e = Employee.find_by_id(s, id_)
        if not e:
            print(f"Employee {id_} not found")
            return
        e.delete(s)
        print(f"Employee {id_} deleted")

# ---------- Project actions ----------
def list_projects():
    with _get_session() as s:
        projs = Project.get_all(s)
        if not projs:
            print("(no records)")
            return

        rows = []
        for p in projs:
            if p.employees:  # If project has employees
                for e in p.employees:
                    rows.append([
                        e.id,
                        e.full_name,
                        p.name,
                        f"${p.budget:.2f}"
                    ])
            else:
                # Show project even if it has no employees assigned
                rows.append([
                    "-", "No employee assigned", p.name, f"${p.budget:.2f}"
                ])

        print(tabulate(
            rows,
            headers=["Employee ID", "Employee Name", "Project Name", "Budget"],
            tablefmt="grid"
        ))


def find_project_by_name():
    name = _ask("Enter the project's name: ")
    with _get_session() as s:
        p = Project.find_by_name(s, name)
        if p:
            table = [(p.id, p.name, f"${p.budget:.2f}")]
            print(tabulate(table, headers=["ID", "Name", "Budget"], tablefmt="grid"))
        else:
            print(f"Project '{name}' not found")

def create_project():
    name = _ask("Enter the project's name: ")
    budget = _ask("Enter the project's budget: ")
    with _get_session() as s:
        try:
            p = Project.create(s, name=name, budget=budget)
            table = [(p.id, p.name, f"${p.budget:.2f}")]
            print(tabulate(table, headers=["ID", "Name", "Budget"], tablefmt="grid"))
        except Exception as ex:
            s.rollback()
            print("Error creating project:", ex)

def assign_employee_to_project():
    emp_id = _ask("Enter the employee id: ")
    proj_id = _ask("Enter the project id: ")
    with _get_session() as s:
        e = Employee.find_by_id(s, emp_id)
        p = Project.find_by_id(s, proj_id)
        if not e:
            print(f"Employee {emp_id} not found")
            return
        if not p:
            print(f"Project {proj_id} not found")
            return
        if p in e.projects:
            print("Employee already assigned to this project")
            return
        e.projects.append(p)
        s.commit()
        print(f"Assigned {e.full_name} to project '{p.name}'")

def remove_employee_from_project():
    emp_id = _ask("Enter the employee id: ")
    proj_id = _ask("Enter the project id: ")
    with _get_session() as s:
        e = Employee.find_by_id(s, emp_id)
        p = Project.find_by_id(s, proj_id)
        if not e:
            print(f"Employee {emp_id} not found")
            return
        if not p:
            print(f"Project {proj_id} not found")
            return
        if p not in e.projects:
            print("Employee is not assigned to this project")
            return
        e.projects.remove(p)
        s.commit()
        print(f"Removed {e.full_name} from project '{p.name}'")

# ---------- Exit ----------
def exit_program():
    print("Goodbye!")
    raise SystemExit
