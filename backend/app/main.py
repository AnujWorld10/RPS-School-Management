
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.auth import router as auth_router
from app.api.v1.students import router as students_router
from app.api.v1.teachers import router as teachers_router
from app.api.v1.admin import router as admin_router

app = FastAPI(title="School Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add HTTP Bearer security scheme to OpenAPI
security = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API documentation for School Management System",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Add security requirement globally for all endpoints except / and /api/v1/auth/*
    for path, methods in openapi_schema["paths"].items():
        if path.startswith("/api/v1/auth") or path == "/":
            continue
        for method in methods.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(students_router, prefix="/api/v1/students", tags=["students"])
app.include_router(teachers_router, prefix="/api/v1/teachers", tags=["teachers"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "RPS School Management System API"}

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    raise HTTPException(status_code=500, detail="Database error occurred")
