
import os
import re
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
# Base class for SQLAlchemy models
Base = declarative_base()

DB_HOST = "127.0.0.1"
DB_NAME = "rental"
DB_USER = "root"
DB_PASS = "rootpassword"
# ==================================
# CONFIG — output folders
# ==================================
PROJECT_NAME = "rental"
MODELS_DIR = f"./{PROJECT_NAME}/models"
SCHEMAS_DIR = f"./{PROJECT_NAME}/schemas"
CRUD_DIR = f"./{PROJECT_NAME}/cruds"
API_DIR = f"./{PROJECT_NAME}/apis"
# ==================================
# SETUP — create SQLAlchemy engine
# ==================================
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)
inspector = inspect(engine)
# Create folders if not exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SCHEMAS_DIR, exist_ok=True)
os.makedirs(CRUD_DIR, exist_ok=True)
os.makedirs(API_DIR, exist_ok=True)
# ==================================
# TYPE MAPPING — MySQL → SQLAlchemy
# ==================================
def map_sql_to_sqla(sql_type: str):
    s = sql_type.lower()
    if "int" in s:
        return "Integer()"
    if "decimal" in s or "float" in s or "double" in s:
        m = re.search(r"\((\d+),(\d+)\)", s)
        if m:
            return f"Numeric({m.group(1)},{m.group(2)})"
        return "Float()"
    if "char" in s or "text" in s:
        return "String()"
    if "datetime" in s:
        return "DateTime()"
    if "date" in s:
        return "Date()"
    if "time" in s:
        return "Time()"
    if "bool" in s or s.startswith("tinyint(1)"):
        return "Boolean()"
    return "String()"
# ==================================
# TYPE MAPPING — MySQL → Python types for Pydantic
# ==================================
def map_sql_to_py(sql_type: str):
    s = sql_type.lower()
    if "int" in s:
        return "int", None
    if "decimal" in s or "float" in s or "double" in s:
        return "float", None
    if "char" in s or "text" in s:
        m = re.search(r"\((\d+)\)", s)
        if m:
            return "str", int(m.group(1))
        return "str", None
    if "datetime" in s:
        return "datetime", None
    if "date" in s:
        return "date", None
    if "time" in s:
        return "time", None
    if "bool" in s or s.startswith("tinyint(1)"):
        return "bool", None
    return "str", None
# ==================================
# MAIN LOOP — generate files for each table
# ==================================
tables = inspector.get_table_names()
for table in tables:
    columns = inspector.get_columns(table)
    # Convert table_name → TableName
    class_name = "".join(x.capitalize() for x in table.split("_"))
    model_file = f"{MODELS_DIR}/{table}.py"
    schema_file = f"{SCHEMAS_DIR}/{table}.py"
    crud_file = f"{CRUD_DIR}/{table}.py"
    api_file = f"{API_DIR}/{table}.py"
    # ==================================
    # MODEL
    # ==================================
    model_lines = []
    model_class = f"{class_name}Model"
    model_lines.append("from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Numeric, event,Date,Time\n")
    model_lines.append("from sqlalchemy.ext.declarative import declarative_base\n")
    model_lines.append("from datetime import datetime\n\n")
    model_lines.append("Base = declarative_base()\n\n")
    model_lines.append(f"class {model_class}(Base):\n")
    model_lines.append(f"    __tablename__ = '{table}'\n\n")
    # Detect primary keys (works for composite PK)
    pk_list = inspector.get_pk_constraint(table).get("constrained_columns", [])
    # Add all columns
    for col in columns:
        col_name = col["name"]
        col_type = map_sql_to_sqla(str(col["type"]))
        is_pk = col_name in pk_list
        if is_pk:
            model_lines.append(f"    {col_name} = Column({col_type}, primary_key=True)\n")
        else:
            model_lines.append(f"    {col_name} = Column({col_type}, nullable=True)\n")
    # Auto update updateddatetime
    if any(col["name"].lower() == "updateddatetime" for col in columns):
        model_lines.append("\n\n")
        model_lines.append(f"@event.listens_for({model_class}, 'before_update')\n")
        model_lines.append(f"@event.listens_for({model_class}, 'before_insert')\n")
        model_lines.append("def update_updateddatetime(mapper, connection, target):\n")
        model_lines.append("    target.updateddatetime = datetime.now()\n")
    with open(model_file, "w") as f:
        f.write("".join(model_lines))
    # ==================================
    # SCHEMAS
    # ==================================
    schema_lines = []
    schema_class = f"{class_name}Schema"
    create_schema_class = f"{class_name}CreateSchema"
    update_schema_class = f"{class_name}UpdateSchema"
    schema_lines.append("from pydantic import BaseModel,Field, constr\n")
    schema_lines.append("from datetime import datetime, date, time\n")
    schema_lines.append("from typing import Optional\n\n")
    skip_create = {"updateddatetime"}
    skip_update = {"updateddatetime"}
    # GET schema
    schema_lines.append(f"class {schema_class}(BaseModel):\n")
    for col in columns:
        col_name = col["name"]
        py_type, max_length = map_sql_to_py(str(col["type"]))
        field_type = f"str" if py_type == "str" and max_length else py_type
        if py_type == "str" and max_length is not None:
            line = f"    {col_name}: Optional[str] = Field(None, max_length={max_length})"
        else:
            line = f"    {col_name}: Optional[{field_type}] = None"
        schema_lines.append(line+"\n")
    schema_lines.append("\n    class Config:\n")
    schema_lines.append("        from_attributes = True\n")
    schema_lines.append("        json_encoders = {\n")
    schema_lines.append("            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None,\n")
    schema_lines.append("            date: lambda v: v.strftime('%Y-%m-%d') if v else None,\n")
    schema_lines.append("            time: lambda v: v.strftime('%H:%M:%S') if v else None,\n")
    schema_lines.append("        }\n\n")
    # POST schema
    schema_lines.append(f"class {create_schema_class}(BaseModel):\n")
    for col in columns:
        col_name = col["name"]
        if col_name in skip_create:
            continue
        py_type, max_length = map_sql_to_py(str(col["type"]))
        is_pk = col_name in pk_list
        field_type = f"str" if py_type == "str" and max_length else py_type
        if is_pk:
            schema_lines.append(f"    {col_name}: {field_type}\n")
        else:
            if py_type == "str" and max_length is not None:
                line = f"    {col_name}: Optional[str] = Field(None, max_length={max_length})"
            else:
                line = f"    {col_name}: Optional[{field_type}] = None"
            schema_lines.append(line+"\n")
    schema_lines.append("\n    class Config:\n")
    schema_lines.append("        from_attributes = True\n\n")
    # PUT schema
    schema_lines.append(f"class {update_schema_class}(BaseModel):\n")
    for col in columns:
        col_name = col["name"]
        if col_name in skip_update or col_name in pk_list:
            continue
        py_type, max_length = map_sql_to_py(str(col["type"]))
        field_type = f"str" if py_type == "str" and max_length else py_type
        if py_type == "str" and max_length is not None:
            line = f"    {col_name}: Optional[str] = Field(None, max_length={max_length})"
        else:
            line = f"    {col_name}: Optional[{field_type}] = None"
    schema_lines.append(line+"\n")
    schema_lines.append("\n    class Config:\n")
    schema_lines.append("        from_attributes = True\n")
    with open(schema_file, "w") as f:
        f.write("".join(schema_lines))
    # ==================================
    # CRUD
    # ==================================
    crud_lines = []
    crud_lines.append("from sqlalchemy.orm import Session\n")
    crud_lines.append(f"from models.{table} import {model_class}\n")
    crud_lines.append(f"from schemas.{table} import {schema_class},{create_schema_class},{update_schema_class}\n\n")
    crud_lines.append("# CRUD Functions\n\n")
    crud_lines.append("def get_all(session: Session):\n")
    crud_lines.append(f"    return session.query({model_class}).all()\n\n")
    crud_lines.append(f"def get(session: Session, {', '.join(pk_list)}):\n")
    crud_lines.append(f"    return session.query({model_class}).filter_by({', '.join(f'{pk}={pk}' for pk in pk_list)}).first()\n\n")
    crud_lines.append(f"def create(session: Session, obj_in: {create_schema_class}):\n")
    crud_lines.append(f"    obj = {model_class}(**obj_in.dict())\n")
    crud_lines.append("    session.add(obj)\n")
    crud_lines.append("    session.commit()\n")
    crud_lines.append("    session.refresh(obj)\n")
    crud_lines.append("    return obj\n\n")
    crud_lines.append(f"def update(session: Session, db_obj: {model_class}, obj_in: {update_schema_class}):\n")
    crud_lines.append("    for field, value in obj_in.dict(exclude_unset=True).items():\n")
    crud_lines.append("        setattr(db_obj, field, value)\n")
    crud_lines.append("    session.commit()\n")
    crud_lines.append("    session.refresh(db_obj)\n")
    crud_lines.append("    return db_obj\n\n")
    crud_lines.append(f"def delete(session: Session, db_obj: {model_class}):\n")
    crud_lines.append("    session.delete(db_obj)\n")
    crud_lines.append("    session.commit()\n")
    crud_lines.append("    return True\n")
    with open(crud_file, "w") as f:
        f.write("".join(crud_lines))
    # ==================================
    # API ROUTER
    # ==================================
    api_lines = []
    api_lines.append("from fastapi import APIRouter, Depends, HTTPException\n")
    api_lines.append("from sqlalchemy.orm import Session\n")
    api_lines.append("from typing import List\n")
    api_lines.append("from database import get_db\n")
    api_lines.append(f"from schemas.{table} import {schema_class},{create_schema_class},{update_schema_class}\n")
    api_lines.append(f"from cruds.{table} import get, get_all, create, update, delete\n\n")
    api_lines.append(f"router = APIRouter(prefix='/{table}', tags=['{table}'])\n\n")
    api_lines.append(f"@router.get('/', response_model=List[{schema_class}])\n")
    api_lines.append("def read_all(db: Session = Depends(get_db)):\n")
    api_lines.append("    return get_all(db)\n\n")
    pk_params = "/".join(f"{{{pk}}}" for pk in pk_list)
    api_lines.append(f"@router.get('/{pk_params}', response_model={schema_class})\n")
    api_lines.append(f"def read_item({', '.join(pk_list)}, db: Session = Depends(get_db)):\n")
    api_lines.append(f"    db_obj = get(db, {', '.join(pk_list)})\n")
    api_lines.append("    if not db_obj:\n")
    api_lines.append("        raise HTTPException(status_code=404, detail='Item not found')\n")
    api_lines.append("    return db_obj\n\n")
    api_lines.append(f"@router.post('/', response_model={schema_class})\n")
    api_lines.append(f"def create_item(item_in: {create_schema_class}, db: Session = Depends(get_db)):\n")
    api_lines.append("    return create(db, item_in)\n\n")
    api_lines.append(f"@router.put('/{pk_params}', response_model={schema_class})\n")
    api_lines.append(f"def update_item({', '.join(pk_list)}, item_in: {update_schema_class}, db: Session = Depends(get_db)):\n")
    api_lines.append(f"    db_obj = get(db, {', '.join(pk_list)})\n")
    api_lines.append("    if not db_obj:\n")
    api_lines.append("        raise HTTPException(status_code=404, detail='Item not found')\n")
    api_lines.append("    return update(db, db_obj, item_in)\n\n")
    api_lines.append(f"@router.delete('/{pk_params}')\n")
    api_lines.append(f"def delete_item({', '.join(pk_list)}, db: Session = Depends(get_db)):\n")
    api_lines.append(f"    db_obj = get(db, {', '.join(pk_list)})\n")
    api_lines.append("    if not db_obj:\n")
    api_lines.append("        raise HTTPException(status_code=404, detail='Item not found')\n")
    api_lines.append("    delete(db, db_obj)\n")
    api_lines.append("    return {'ok': True}\n")
    with open(api_file, "w") as f:
        f.write("".join(api_lines))
print("✔ All model & schema files generated successfully!")