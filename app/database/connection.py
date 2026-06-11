from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos SQLite (se creará un archivo device_systems.db)
DATABASE_URL = "sqlite:///./device_systems.db"

# engine: es el motor que conecta SQLAlchemy con la BD
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

# SessionLocal: fábrica de sesiones (cada sesión es una transacción)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base para todos los modelos ORM
Base = declarative_base()

# Dependencia para obtener la sesión de BD en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()