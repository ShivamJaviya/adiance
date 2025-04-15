from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.services.content_service import ContentService

router = APIRouter()

@router.post("/generate", response_model=schemas.GeneratedContentResponse)
async def generate_content(
    content_request: schemas.ContentGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate content based on prompt."""
    content_service = ContentService(db)
    
    try:
        result = await content_service.generate_content(
            prompt_id=content_request.prompt_id,
            content_type=content_request.content_type,
            provider=content_request.provider,
            parameters=content_request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating content: {str(e)}"
        )

@router.get("/content", response_model=List[schemas.GeneratedContent])
async def get_content(prompt_id: int = None, db: Session = Depends(get_db)):
    """Get generated content, optionally filtered by prompt ID."""
    query = db.query(models.GeneratedContent)
    if prompt_id:
        query = query.filter(models.GeneratedContent.prompt_id == prompt_id)
    content = query.all()
    return content

@router.get("/content/{content_id}", response_model=schemas.GeneratedContent)
async def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    """Get a specific generated content."""
    content = db.query(models.GeneratedContent).filter(models.GeneratedContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.delete("/content/{content_id}", response_model=schemas.GeneratedContent)
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    """Delete a specific generated content."""
    content = db.query(models.GeneratedContent).filter(models.GeneratedContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(content)
    db.commit()
    return content
