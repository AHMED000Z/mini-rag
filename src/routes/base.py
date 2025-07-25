from fastapi import FastAPI, APIRouter,Depends
from helpers.config import Settings,get_settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["/api/v1"]
)

@base_router.get('/')
async def welcome(app_settings : Settings=Depends(get_settings)):

    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    return{
        "name":app_name,
        "version":app_version
    }
