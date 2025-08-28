# lib/models/department.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates

from . import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    # Unique department names
    __table_args__ = (UniqueConstraint("name", name="uq_department_name"),)

    # Relationship: one Department -> many Employees
    employees = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete-orphan"
    )

    # --- Validators (constraints) ---
    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Department name must be a non-empty string")
        return value.strip()

    @validates("location")
    def validate_location(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Department location must be a non-empty string")
        return value.strip()

    # --- Convenience / CRUD helpers ---
    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create(cls, session, name, location):
        dept = cls(name=name, location=location)
        session.add(dept)
        session.commit()
        session.refresh(dept)
        return dept

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, int(id_)) if str(id_).isdigit() else None

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls.name == name).first()

    def update(self, session, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
