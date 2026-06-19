from fastapi import FastAPI
from app.routes import user_routes, device_routes, loan_routes
from app.database.connection import engine, Base

# Crear tablas en la base de datos (solo si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0"
)

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a device_systems API"}