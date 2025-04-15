import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.llm.factory import LLMFactory
from app.models import models
from app.services.config_service import ConfigurationService

class AnalysisService:
    """Service for analyzing competitor content and generating prompt ideas."""
    
    def __init__(self, db: Session):
        self.db = db
        self.config_service = ConfigurationService()
    
    async def analyze_competitor(self, url: str, analysis_type: str, provider: str) -> Dict[str, Any]:
        """
        Analyze competitor content using the specified LLM provider.
        
        Args:
            url: URL of the competitor content
            analysis_type: Type of analysis (blog, social, website)
            provider: LLM provider to use
            
        Returns:
            Analysis results
        """
        try:
            # Get API key
            api_key = self.config_service.get_api_key(provider, self.db)
            
            # Get LLM provider
            llm_provider = LLMFactory.get_provider(provider, api_key)
            
            # Analyze competitor
            analysis_result = await llm_provider.analyze_competitor(url, analysis_type)
            
            # Save to database
            db_analysis = models.CompetitorAnalysis(
                competitor_url=url,
                analysis_type=analysis_type,
                provider=provider,
                content_themes=json.dumps(analysis_result.get("content_themes", [])),
                content_strategy=json.dumps(analysis_result.get("content_strategy", [])),
                raw_analysis=json.dumps(analysis_result)
            )
            self.db.add(db_analysis)
            self.db.commit()
            self.db.refresh(db_analysis)
            
            # Format response
            response = {
                "id": db_analysis.id,
                "competitor_url": db_analysis.competitor_url,
                "analysis_type": db_analysis.analysis_type,
                "provider": db_analysis.provider,
                "content_themes": analysis_result.get("content_themes", []),
                "content_strategy": analysis_result.get("content_strategy", []),
                "created_at": db_analysis.created_at
            }
            
            return response
        except Exception as e:
            self.db.rollback()
            raise e
    
    async def generate_prompt_ideas(self, analysis_id: int, provider: str, num_ideas: int = 5) -> List[Dict[str, Any]]:
        """
        Generate prompt ideas based on analysis data.
        
        Args:
            analysis_id: ID of the competitor analysis
            provider: LLM provider to use
            num_ideas: Number of prompt ideas to generate
            
        Returns:
            List of prompt ideas
        """
        try:
            # Get analysis
            analysis = self.db.query(models.CompetitorAnalysis).filter(models.CompetitorAnalysis.id == analysis_id).first()
            if not analysis:
                raise ValueError(f"Analysis not found: {analysis_id}")
            
            # Parse analysis data
            analysis_data = json.loads(analysis.raw_analysis)
            
            # Get API key
            api_key = self.config_service.get_api_key(provider, self.db)
            
            # Get LLM provider
            llm_provider = LLMFactory.get_provider(provider, api_key)
            
            # Generate prompt ideas
            options = {"num_ideas": num_ideas}
            prompt_ideas = await llm_provider.generate_prompt_ideas(analysis_data, options)
            
            # Save to database
            db_prompt_ideas = []
            for idea in prompt_ideas:
                db_prompt_idea = models.PromptIdea(
                    analysis_id=analysis_id,
                    prompt_text=idea.get("prompt_text", ""),
                    provider=provider,
                    confidence_score=idea.get("confidence_score", 0)
                )
                self.db.add(db_prompt_idea)
                self.db.commit()
                self.db.refresh(db_prompt_idea)
                db_prompt_ideas.append(db_prompt_idea)
            
            return db_prompt_ideas
        except Exception as e:
            self.db.rollback()
            raise e
