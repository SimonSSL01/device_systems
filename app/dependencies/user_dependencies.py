from fastapi import Header, HTTPException

def verify_headers(
    x_app_name: str = Header(..., alias="X-App-Name"),
    x_api_version: str = Header(..., alias="X-API-Version")
):
    if x_app_name != "device_systems":
        raise HTTPException(status_code=400, detail="X-App-Name inválido")
    if x_api_version not in ["1.0", "2.0"]:
        raise HTTPException(status_code=400, detail="Versión no soportada")
    return {"app_name": x_app_name, "api_version": x_api_version}
