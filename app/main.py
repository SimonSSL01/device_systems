from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="2.0.0",
    contact={
        "name": "Simon sierra",
        "email": "simonuwusierra@gmail.com"
    },
    license_info={
        "name": "MIT",
    }
)

app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a device_systems API - Versión 2.0"}