# lib/models/project.py
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, validates

 . import Base

# Association table for many-to-many Employee <-> Project
employee_project = Table(
    "employee_project",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", name="uq_project_name"),
        CheckConstraint("budget > 0", name="ck_project_budget_positive"),
    )

    employees = relationship("Employee", secondary=employee_project, back_populates="projects")

    # --- Validators ---
    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Project name must be a non-empty string")
        return value.strip()

    @validates("budget")
    def validate_budget(self, key, value):
        try:
            val = float(value)
        except Exception:
            raise ValueError("Budget must be a number")
        if val <= 0:
            raise ValueError("Budget must be greater than 0")
        return val

    # --- Helpers / CRUD ---
    def __repr__(self):
        return f"<Project {self.id}: {self.name}, Budget ${self.budget:.2f}>"

    @classmethod
    def create(cls, session, name, budget):
        proj = cls(name=name, budget=budget)
        session.add(proj)
        session.commit()
        session.refresh(proj)
        return proj

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
