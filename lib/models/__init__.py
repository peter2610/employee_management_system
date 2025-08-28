# lib/models/__init__.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB lives at lib/company.db
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "company.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    """Import models and create tables."""
    # Import models so metadata knows about them
    from .department import Department  # noqa: F401
    from .employee import Employee      # noqa: F401
    from .project import Project, employee_project  # noqa: F401
    Base.metadata.create_all(bind=engine)
