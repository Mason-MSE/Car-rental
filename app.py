from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import importlib.util
import sys
from typing import List, Optional

from core.dependencies import get_current_user
from apis.auth import auth_router


app = FastAPI()

app = FastAPI(
    title="Car Rental System",
    description="FastAPI Swagger",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def include_routers_from_folder(folder: str = "api"):
    """
    Automatically discover and include all router modules from the given folder.
    Expects each file to have a variable named 'router' (APIRouter instance).
    """
    routers_path = Path(__file__).parent / folder
    if not routers_path.is_dir():
        print(f"Warning: router folder not found: {routers_path}")
        return

    for file_path in routers_path.glob("*.py"):
        if file_path.name == "__init__.py":
            continue

        module_name = f"app.{folder}.{file_path.stem}"

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Look for 'router' variable (most common convention)
        if hasattr(module, "router"):
            router = getattr(module, "router")
            # Optional: add prefix=/api or prefix=f"/{file_path.stem}" etc.
            app.include_router(router,dependencies=[Depends(get_current_user)])   # or app.include_router(router, prefix=f"/{file_path.stem}")
            print(f"Included router from: {file_path.name}")
        if hasattr(module, "public_router"):
            app.include_router(module.public_router)


app.include_router(auth_router)
# ────────────────────────────────────────────────
# Auto-register all routers
include_routers_from_folder("apis")

@app.get("/")
async def root():
    return {"message": "Welcome to YB-PYTHON Assessment 1 API (FastAPI version)"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)