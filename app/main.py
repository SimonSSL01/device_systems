from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="Device Systems API",
    description="API para gestión de usuarios del sistema device_systems",
    version="1.0"
)

# Incluir las rutas de usuarios
app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a Device Systems API"}