from sqlalchemy.orm import Session
import models, schemas

def get_template(db: Session, template_id: int):
    return db.query(models.Template).filter(models.Template.id == template_id).first()

def get_templates(db: Session):
    return db.query(models.Template).all()

def create_template(db: Session, template: schemas.TemplateCreate):
    db_template = models.Template(
        name=template.name,
        main_text=template.main_text,
        variables=[v.dict() for v in template.variables],
        options=[o.dict() for o in template.options]
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_template(db: Session, template_id: int, template_data: schemas.TemplateCreate):
    db_template = get_template(db, template_id)
    if not db_template:
        return None
    
    db_template.name = template_data.name
    db_template.main_text = template_data.main_text
    db_template.variables = [v.dict() for v in template_data.variables]
    db_template.options = [o.dict() for o in template_data.options]
    
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_template(db: Session, template_id: int):
    db_template = get_template(db, template_id)
    if db_template:
        db.delete(db_template)
        db.commit()
    return db_template



def get_global_variables(db: Session):
    return db.query(models.GlobalVariable).all()

def create_global_variable(db: Session, var: schemas.GlobalVariableCreate):
    db_var = models.GlobalVariable(name=var.name, label=var.label)
    db.add(db_var)
    db.commit()
    db.refresh(db_var)
    return db_var

def delete_global_variable(db: Session, var_id: int):
    db_var = db.query(models.GlobalVariable).filter(models.GlobalVariable.id == var_id).first()
    if db_var:
        db.delete(db_var)
        db.commit()
    return db_var
