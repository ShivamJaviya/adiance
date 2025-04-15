from fastapi import APIRouter

from app.api.endpoints import config, analysis, content

api_router = APIRouter()
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
