from fastapi import FastAPI
from app.routes.user_routes import router
from app.database.connection import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios con persistencia en SQLite",
    version="3.0.0",
    contact={"name": "Simón", "email": "simonuwusierra@gmail.com"},
    license_info={"name": "MIT"}
)

app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a device_systems API"}