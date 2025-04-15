from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/analyze", response_model=schemas.CompetitorAnalysisResponse)
async def analyze_competitor(
    analysis_request: schemas.CompetitorAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze competitor content."""
    analysis_service = AnalysisService(db)
    
    try:
        result = await analysis_service.analyze_competitor(
            url=analysis_request.competitor_url,
            analysis_type=analysis_request.analysis_type,
            provider=analysis_request.provider
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing competitor: {str(e)}"
        )

@router.get("/analyses", response_model=List[schemas.CompetitorAnalysis])
async def get_analyses(db: Session = Depends(get_db)):
    """Get all competitor analyses."""
    analyses = db.query(models.CompetitorAnalysis).all()
    return analyses

@router.get("/analyses/{analysis_id}", response_model=schemas.CompetitorAnalysis)
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Get a specific competitor analysis."""
    analysis = db.query(models.CompetitorAnalysis).filter(models.CompetitorAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.post("/generate-prompts", response_model=List[schemas.PromptIdea])
async def generate_prompt_ideas(
    prompt_request: schemas.PromptIdeaRequest,
    db: Session = Depends(get_db)
):
    """Generate prompt ideas based on analysis."""
    analysis_service = AnalysisService(db)
    
    try:
        # Get the analysis
        analysis = db.query(models.CompetitorAnalysis).filter(models.CompetitorAnalysis.id == prompt_request.analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Generate prompt ideas
        prompt_ideas = await analysis_service.generate_prompt_ideas(
            analysis_id=prompt_request.analysis_id,
            provider=prompt_request.provider,
            num_ideas=prompt_request.num_ideas
        )
        return prompt_ideas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating prompt ideas: {str(e)}"
        )

@router.get("/prompt-ideas", response_model=List[schemas.PromptIdea])
async def get_prompt_ideas(analysis_id: int = None, db: Session = Depends(get_db)):
    """Get prompt ideas, optionally filtered by analysis ID."""
    query = db.query(models.PromptIdea)
    if analysis_id:
        query = query.filter(models.PromptIdea.analysis_id == analysis_id)
    prompt_ideas = query.all()
    return prompt_ideas

@router.get("/prompt-ideas/{prompt_id}", response_model=schemas.PromptIdea)
async def get_prompt_idea(prompt_id: int, db: Session = Depends(get_db)):
    """Get a specific prompt idea."""
    prompt_idea = db.query(models.PromptIdea).filter(models.PromptIdea.id == prompt_id).first()
    if not prompt_idea:
        raise HTTPException(status_code=404, detail="Prompt idea not found")
    return prompt_idea
