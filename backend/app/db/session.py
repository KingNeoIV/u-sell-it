from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# Base class for all SQLAlchemy ORM models.
# All models in the application should inherit from this.
class Base(DeclarativeBase):
    pass


# Create the database engine using the configured DATABASE_URL.
# pool_pre_ping ensures stale connections are detected and refreshed.
# SQLite requires a special argument; PostgreSQL does not.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)
# engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Session factory used to create database sessions.
# autocommit and autoflush are disabled for explicit transaction control.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency used by FastAPI routes to provide a database session.
# Ensures each request gets its own session and closes it afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
