from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    main_text = Column(String)
    variables = Column(JSON) # Храним массив объектов [{name, label}] как JSON
    options = Column(JSON)   # Храним массив объектов [{id, label, code}] как JSON


class GlobalVariable(Base):
    __tablename__ = "global_variables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # Уникальное системное имя (например, hostname)
    label = Column(String) # Понятное описание (например, Имя устройства)
