# lib/models/employee.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, validates

from . import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_employee_email"),
        CheckConstraint("salary > 0", name="ck_employee_salary_positive"),
    )

    # Many employees -> one department
    department = relationship("Department", back_populates="employees")
    # Many-to-many with projects (declared on Project with secondary table)
    projects = relationship("Project", secondary="employee_project", back_populates="employees")

    # --- Validators ---
    @validates("first_name", "last_name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key.replace('_',' ').title()} must be a non-empty string")
        return value.strip()

    @validates("email")
    def validate_email(self, key, value):
        if not value or "@" not in value or "." not in value:
            raise ValueError("Email must be a valid email address")
        return value.strip().lower()

    @validates("salary")
    def validate_salary(self, key, value):
        try:
            val = float(value)
        except Exception:
            raise ValueError("Salary must be a number")
        if val <= 0:
            raise ValueError("Salary must be greater than 0")
        return val

    # --- Helpers ---
    def __repr__(self):
        return (f"<Employee {self.id}: {self.first_name} {self.last_name}, "
                f"{self.email}, ${self.salary:.2f}, Department ID: {self.department_id}>")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def create(cls, session, **attrs):
        emp = cls(**attrs)
        session.add(emp)
        session.commit()
        session.refresh(emp)
        return emp

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, int(id_)) if str(id_).isdigit() else None

    @classmethod
    def find_by_name(cls, session, name):
        """Simple 'full name' match or first/last match."""
        q = session.query(cls)
        name = (name or "").strip()
        if " " in name:
            first, last = name.split(" ", 1)
            return q.filter(cls.first_name == first, cls.last_name == last).first()
        # fallback: match either first OR last
        return q.filter((cls.first_name == name) | (cls.last_name == name)).first()

    def update(self, session, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
