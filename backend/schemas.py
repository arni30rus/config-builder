from pydantic import BaseModel
from typing import List, Optional

class VariableSchema(BaseModel):
    name: str
    label: str

class OptionSchema(BaseModel):
    id: str
    label: str
    code: str

# Данные, которые мы ожидаем при создании/обновлении шаблона
class TemplateCreate(BaseModel):
    name: str
    main_text: str
    variables: List[VariableSchema]
    options: List[OptionSchema]

# Данные, которые мы отдаем на фронтенд (с id)
class TemplateResponse(TemplateCreate):
    id: int

    class Config:
        from_attributes = True

class GlobalVariableCreate(BaseModel):
    name: str
    label: str

class GlobalVariableResponse(GlobalVariableCreate):
    id: int
    class Config:
        from_attributes = True

