from fastapi import APIRouter

from app.api.endpoints import login, ocr

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])