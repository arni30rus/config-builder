from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models, schemas, crud
from database import engine, SessionLocal
from services.templater import templater_service

# Создаем таблицы в БД при старте (если их еще нет)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Config Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Эндпоинты для Шаблонов ---
@app.get("/api/templates", response_model=list[schemas.TemplateResponse])
def read_templates(db: Session = Depends(get_db)):
    return crud.get_templates(db)

@app.get("/api/templates/{template_id}", response_model=schemas.TemplateResponse)
def read_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud.get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return db_template

@app.post("/api/templates", response_model=schemas.TemplateResponse)
def create_template(template: schemas.TemplateCreate, db: Session = Depends(get_db)):
    return crud.create_template(db=db, template=template)

@app.put("/api/templates/{template_id}", response_model=schemas.TemplateResponse)
def update_template(template_id: int, template: schemas.TemplateCreate, db: Session = Depends(get_db)):
    db_template = crud.update_template(db, template_id, template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return db_template

@app.delete("/api/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    crud.delete_template(db, template_id)
    return {"message": "Шаблон удален"}

# --- Эндпоинты для ОБЩИХ ПЕРЕМЕННЫХ ---
@app.get("/api/global-variables", response_model=list[schemas.GlobalVariableResponse])
def read_global_variables(db: Session = Depends(get_db)):
    return crud.get_global_variables(db)

@app.post("/api/global-variables", response_model=schemas.GlobalVariableResponse)
def create_global_variable(var: schemas.GlobalVariableCreate, db: Session = Depends(get_db)):
    # Проверка на уникальность имени
    existing = db.query(models.GlobalVariable).filter(models.GlobalVariable.name == var.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Переменная с таким именем уже существует")
    return crud.create_global_variable(db=db, var=var)

@app.delete("/api/global-variables/{var_id}")
def delete_global_variable(var_id: int, db: Session = Depends(get_db)):
    crud.delete_global_variable(db, var_id)
    return {"message": "Общая переменная удалена"}

# --- Эндпоинт генерации ---
class GenerateRequest(BaseModel):
    template_id: int
    variables: dict

@app.post("/api/generate")
def generate_config(request: GenerateRequest, db: Session = Depends(get_db)):
    db_template = crud.get_template(db, request.template_id)
    if not db_template:
        raise HTTPException(status_code=404, detail="Шаблон не найден")

    jinja_template = db_template.main_text + "\n"
    if db_template.options:
        for opt in db_template.options:
            jinja_template += f"\n{{% if {opt['id']} %}}\n{opt['code']}\n{{% endif %}}\n"

    # Собираем итоговые переменные: берем переданные с фронта, 
    # и если чего-то не хватает, можно взять дефолтные (пока берем только то, что пришло)
    try:
        result = templater_service.render_config(jinja_template, request.variables)
        return {"rendered_config": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
