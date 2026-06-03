import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Берем URL из переменной окружения DATABASE_URL, если её нет - используем локальную для разработки
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:password@localhost:5432/configdb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
