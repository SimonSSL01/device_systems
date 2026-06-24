from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.routes import user_routes, device_routes, loan_routes
from app.auth import auth_routes
from app.database.connection import engine, Base
from app.middlewares.request_middleware import request_middleware
from app.limiter import limiter  # <--- Importar desde aquí

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0"
)

app.middleware("http")(request_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Demasiadas peticiones. Por favor, espera un momento."},
    )

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a device_systems API - Versión 3.0 (con seguridad)"}