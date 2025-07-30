from fastapi import FastAPI ,APIRouter, Depends 
import os
from helpers.config import get_settings, Settings


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_seettings: Settings = Depends(get_settings)):
    
    
    app_name = app_seettings.APP_NAME
    app_version = app_seettings.APP_VERSION
    
    return {
        f"Welcome to {app_name} version {app_version}",      
    }
